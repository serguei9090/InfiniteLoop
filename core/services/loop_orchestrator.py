import logging
import time
import os
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
        os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
        prompt = f"""You are the IMMUTABLE CORE Orchestrator. 
Your primary directive is to expand the system's capabilities through autonomous coding while respecting the integrity of core services.

Environment:
- Operating System: {os_info}
- Shell Capability: {"PowerShell/CMD" if platform.system() == "Windows" else "Bash/Sh"}

Project Structure:
- core/ : InfiniteLoop Backend logic (IMMUTABLE, READ-ONLY). 
- ui/   : InfiniteLoop Frontend (IMMUTABLE, READ-ONLY).
- workspace/ : YOUR EXCLUSIVE WORKSPACE (READ-WRITE). All code development happens here.
  - Paths should be relative to workspace root (e.g., 'test_feature/readme.md').
  - The orchestrator runner will automatically resolve these paths.

Current Task: {self.current_task}

You are IMMUTABLE CORE, an autonomous mission-critical orchestrator. 
Your goal is to complete the assigned MISSION with zero hesitation and absolute technical precision.

REASONING PROTOCOL:
1. Always start your response with a <|think|> block.
2. Inside <|think|>, break down the mission into surgical steps.
3. Critically evaluate if you need to read files before making changes.

TOOL CALL PROTOCOL:
- You MUST output tool calls in a single JSON block.
- DO NOT use pseudo-tags like <|write_file|>. 
- Use the following format:
```json
{{
  "tool": "tool_name",
  "args": {{
    "arg1": "value1"
  }}
}}
```

AVAILABLE BASE TOOLS:
- read_file(path, mode='skeleton'): Returns file content. Use 'skeleton' for high-level overview or 'full' for exact code.
- write_file(path, content): Creates or overwrites a file. Ensure parent directories exist.
- delete_file(path): Moves a file to the .trash folder.
- create_folder(path): Creates a directory (and parents) if it doesn't exist.
- execute_cmd(command): Runs a shell command in the workspace. Use for build, test, and lint.
- create_new_tool(name, code, schema): Permanent capability evolution.

EVOLVED TOOLS:
{dynamic_tools if dynamic_tools else "No custom tools registered yet."}

TERMINATION:
- When the MISSION is complete, output "TASK_COMPLETE".
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
            self._stream_adapter(self.llm_bridge.chat_stream(self.context.get_messages()))
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

        print(f"\n--- MISSION OUTPUT ---\n{full_response}\n--- Step Complete ---")

        # Add response to history
        if not full_response.strip():
            self.silent_retries += 1
            logger.warning(f"⚠️ Empty LLM response (Retry {self.silent_retries}/3)")
            if self.silent_retries >= 3:
                logger.error("🛑 Stopping loop: LLM is repeatedly returning empty responses.")
                self.stop_task()
                return
            return # Skip tool handling and try again

        self.silent_retries = 0 # Reset on valid response
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
        print(f"--- TOOL RESULT ---\n{result}\n-------------------")

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
                    "user", f"CRITICAL: Tool failed 3 times. {error_msg}. Aborting."
                )
                await self._emit(
                    "status", {"state": "Failed", "retry": self.retry_count}
                )
            else:
                self.context.add_message(
                    "user",
                    f"Tool Failed: {result['error']}\n"
                    "PLEASE ANALYZE THE FAILURE: Why did this fail? Is a file missing? Is the command syntax wrong?\n"
                    "If you need to create a directory before writing a file, do it now. Then retry the mission."
                )

    def _calculate_input_tokens(self) -> int:
        # Simplified tokenization: ~4 chars per token
        total_chars = sum(len(m["content"]) for m in self.context.get_messages())
        return int(total_chars / 4)

    async def _stream_adapter(self, stream: AsyncGenerator[Dict, None]) -> AsyncGenerator[str, None]:
        """Convert LLM delta dicts to plain strings for the parser."""
        async for delta in stream:
            content = delta.get("content")
            if content:
                yield content

    def stop_task(self):
        self.task_active = False
