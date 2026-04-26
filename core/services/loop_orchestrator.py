import logging
import time
import platform
from typing import Optional, Any, AsyncGenerator, Dict
from services.llm_bridge import LLMBridge
from services.stream_parser import StreamParser
from services.context_manager import ContextManager
from services.tool_engine import ToolEngine
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.base_tools import BaseTools
from typing import Callable, Coroutine

logger = logging.getLogger(__name__)


class LoopOrchestrator:
    def __init__(self, llm_bridge: LLMBridge, workspace_root: str = "./workspace"):
        self.llm_bridge = llm_bridge
        self.guard = WorkspaceGuard(workspace_root)
        self.context = ContextManager(max_tokens=8192)
        self.context_engine = ContextEngine()
        self.evolution = EvolutionEngine(workspace_root + "/.agents/dynamic_tools")
        self.tools = BaseTools(self.guard, self.context_engine, self.evolution)
        self.tool_engine = ToolEngine(self.tools)

        self.task_active = False
        self.current_task: Optional[str] = None
        self.max_retries = 3
        self.retry_count = 0
        self.silent_retries = 0
        self.event_callback: Optional[Callable[[str, Any], Coroutine]] = None

        # Token metrics tracking
        self.input_tokens = 0
        self.output_tokens = 0

    async def start_task(self, task: str):
        self.context.reset()
        self.current_task = task
        self.task_active = True
        self._set_dynamic_system_prompt()
        self.context.add_message("user", task)

        while self.task_active:
            await self._loop_step()

        await self._emit("status", {"state": "Idle", "retry": 0})

    def _set_dynamic_system_prompt(self):
        dynamic_tools = self.evolution.get_tool_descriptions()
        f"{platform.system()} {platform.release()} ({platform.machine()})"
        prompt = f"""[IMMUTABLE CORE v4]
DIRECTIVE: Complete MISSION with absolute technical precision.
BOUNDARIES:
- core/ & ui/ : READ-ONLY. Internal logic. Do not attempt to modify.
- workspace/  : READ-WRITE. Your exclusive development sandbox. All work happens here.
- Pathing: All paths MUST be relative to workspace/ root. The runner handles resolution.

MULTI-AGENT ORCHESTRATION:
- We operate a multi-AI orchestrator (GeminiAI, Codex, Qwen, Jules, Local AI).
- Task routing is automatic via the backend for coding, chat, and handoff categories.
- Fallback/mock AIs are in place for validation and fault tolerance.
- Context truncation from the left is enabled to maintain token bounds.
- All dynamic tools and skill modules operate in HOT MODE (can be enabled/disabled at runtime).

REASONING & VALIDATION CRITERIA:
1. <|think|> block mandatory. Surgical step-by-step breakdown. Review requirements deeply.
2. Read before Write. Verify assumptions with tools before acting.
3. Validate your logic before answering. Ensure no syntax errors or breaking changes are introduced.

PROTOCOL:
- Output tool calls in a single JSON block.
- Format: {{"tool": "tool_name", "args": {{"arg": "val"}}}}

TOOLS:
- read_file(path, mode='skeleton'|'full')
- write_file(path, content)
- delete_file(path)
- create_folder(path)
- execute_cmd(command)
- create_new_tool(name, code, schema)

EVOLVED TOOLS:
{dynamic_tools if dynamic_tools else "None."}

MISSION: {self.current_task}
TERMINATION: Output "TASK_COMPLETE" when finished.
"""
        self.context.set_system_prompt(prompt)

    async def _emit(self, event_type: str, data: Any):
        if self.event_callback:
            await self.event_callback(event_type, data)

    async def _loop_step(self):
        logger.info("Starting loop step...")
        await self._emit("status", {"state": "Thinking", "retry": self.retry_count})

        parser = StreamParser()
        full_response = ""
        thought_buffer = ""
        content_buffer = ""

        start_time = time.time()
        token_count = 0

        self.input_tokens = self._calculate_input_tokens()

        async for chunk, is_thinking in parser.parse(
            self._stream_adapter(
                self.llm_bridge.chat_stream(self.context.get_messages())
            )
        ):
            # Approx tokens: 4 chars per token
            chunk_tokens = len(chunk) / 4
            token_count += chunk_tokens
            self.output_tokens += chunk_tokens

            elapsed = time.time() - start_time
            if elapsed > 0.5:  # Emit metrics every 0.5s
                tps = token_count / elapsed
                await self._emit(
                    "metrics",
                    {
                        "tps": round(tps, 1),
                        "input_tokens": int(self.input_tokens),
                        "output_tokens": int(self.output_tokens),
                        "total_tokens": int(self.input_tokens + self.output_tokens),
                    },
                )

            if is_thinking:
                thought_buffer += chunk
                await self._emit("thought", chunk)
            else:
                if "{" in chunk or "tool" in chunk:
                    await self._emit(
                        "status", {"state": "Coding", "retry": self.retry_count}
                    )
                content_buffer += chunk
                await self._emit("act", chunk)

            full_response += chunk

        # Add response to history
        if not full_response.strip():
            self.silent_retries += 1
            logger.warning(f"⚠️ Empty LLM response (Retry {self.silent_retries}/3)")
            if self.silent_retries >= 3:
                logger.error(
                    "🛑 Stopping loop: LLM is repeatedly returning empty responses."
                )
                self.stop_task()
                return
            return  # Skip tool handling and try again

        self.silent_retries = 0  # Reset on valid response
        self.context.add_message("assistant", full_response)

        # Detect tool call
        if "{" in content_buffer and "tool" in content_buffer:
            await self._handle_tool_call(content_buffer)
        elif "TASK_COMPLETE" in content_buffer:
            self.task_active = False
            logger.info("Task finished.")
            await self._emit("status", {"state": "Idle", "retry": 0})
        else:
            # If no tool call and not complete, maybe it's a clarification or summary
            await self._emit(
                "status", {"state": "Reviewing Result", "retry": self.retry_count}
            )

    async def _handle_tool_call(self, content: str):
        logger.info("Executing tool call...")
        await self._emit(
            "status", {"state": "Executing Tool", "retry": self.retry_count}
        )
        result = await self.tool_engine.execute(content)

        if result["success"]:
            self.retry_count = 0  # Reset retry on success
            self.context.add_message("user", f"Tool Output: {result['data']}")
            await self._emit("tool_result", {"success": True, "output": result["data"]})
            # Refresh prompt in case a new tool was added
            self._set_dynamic_system_prompt()
            await self._emit("status", {"state": "Validating Result", "retry": 0})
        else:
            self.retry_count += 1
            error_msg = f"Tool Failed: {result['error']}"
            if result.get("data"):
                error_msg += f"\nPartial Output: {result['data']}"

            await self._emit("tool_result", {"success": False, "error": error_msg})
            await self._emit(
                "status", {"state": "Handling Error", "retry": self.retry_count}
            )

            logger.warning(
                f"Tool failure (Retry {self.retry_count}/{self.max_retries}): {error_msg}"
            )

            if self.retry_count >= self.max_retries:
                self.task_active = False
                self.context.add_message(
                    "user",
                    f"CRITICAL: Tool failed 3 times. {error_msg}. Aborting mission.",
                )
                await self._emit(
                    "status", {"state": "Failed", "retry": self.retry_count}
                )
            else:
                self.context.add_message(
                    "user",
                    f"TOOL_ERROR: {result['error']}\n"
                    "ACTION REQUIRED:\n"
                    "1. Analyze the root cause of this failure in your next <|think|> block.\n"
                    "2. Propose a corrective action (e.g., creating missing directories, fixing syntax).\n"
                    "3. Retry the tool call with corrected arguments or perform the fix first.",
                )

    def _calculate_input_tokens(self) -> int:
        # Simplified tokenization: ~4 chars per token
        total_chars = sum(len(m["content"]) for m in self.context.get_messages())
        return int(total_chars / 4)

    async def _stream_adapter(
        self, stream: AsyncGenerator[Dict, None]
    ) -> AsyncGenerator[str, None]:
        """Convert LLM delta dicts to plain strings for the parser."""
        async for delta in stream:
            content = delta.get("content")
            if content:
                yield content

    def stop_task(self):
        self.task_active = False
