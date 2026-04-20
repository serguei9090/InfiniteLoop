"""
Orchestrator Brain Core - The Central Intelligence
Integrates all tools, auto-adaptation, and provides the main orchestration loop.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.base_tools import BaseTools
from pathlib import Path
import sys

from modules.tool_registry import ToolRegistry
from modules.auto_adaptation import AutoAdaptationEngine, ModuleInfo
from services.context_manager import ContextManager
from services.llm_bridge import LLMBridge
from services.tool_engine import ToolEngine
from modules.base_tools import BaseTools
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.thinking import ThinkingEngine

logger = logging.getLogger(__name__)


class OrchestratorBrain:
    """
    The Orchestrator Brain - Central intelligence for the IMMUTABLE CORE system.

    Capabilities:
    - Manages all tools and their lifecycle
    - Auto-adaptation with hot-loading modules
    - Self-improvement loops
    - Frontend connection for status updates
    - Agent instructions management

    This is the "brain" that can create and add new tools to itself.
    """

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()

        # Initialize core components
        self.llm_bridge = LLMBridge()
        self.guard = WorkspaceGuard(str(self.workspace_root))
        self.context_engine = ContextEngine()
        self.evolution = EvolutionEngine(
            str(self.workspace_root / ".agents" / "dynamic_tools")
        )
        self.context_manager = ContextManager(max_tokens=8192)
        self.thinking_engine = ThinkingEngine()

        # Initialize tool registry (the brain's tool collection)
        self.tool_registry = ToolRegistry(str(self.workspace_root))

        # Initialize auto-adaptation engine
        self.auto_adaptation = AutoAdaptationEngine(str(self.workspace_root))

        # Initialize base tools
        self.base_tools = BaseTools(self.guard, self.context_engine, self.evolution)

        # Pre-register base_tools in auto-adaptation modules for testing
        self.auto_adaptation.modules["backend"]["base_tools"] = ModuleInfo(
            name="base_tools",
            path=str(self.base_tools),
            category="backend",
            status="loaded",
            last_tested=time.time(),
            test_result="passed",
        )
        self.tool_engine = ToolEngine(self.base_tools)

        # State tracking
        self.task_active = False
        self.current_task: Optional[str] = None
        self.status_state = "idle"
        self.metrics_tps = 0.0

        # Event callbacks for frontend
        self.status_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self.thought_callback: Optional[Callable[[str], None]] = None
        self.action_callback: Optional[Callable[[Dict[str, Any]], None]] = None

        # Agent instructions
        self.agent_instructions: List[Dict[str, Any]] = []

        # File operations wrapper (for testing) - async methods returning dict
        class FileOperationsWrapper:
            """Wrapper for file operations that returns dict format with success/data/error keys."""

            def __init__(self, orchestrator):
                self._orchestrator = orchestrator

            async def read_file(
                self, path: str, mode: str = "skeleton"
            ) -> Dict[str, Any]:
                """Read file content."""
                result = self._orchestrator.base_tools.read_file(path, mode)
                return {
                    "success": result.success,
                    "data": result.output,
                    "error": result.error,
                }

            async def write_file(self, path: str, content: str) -> Dict[str, Any]:
                """Write file content."""
                result = self._orchestrator.base_tools.write_file(path, content)
                return {
                    "success": result.success,
                    "data": result.output,
                    "error": result.error,
                }

            async def create_folder(self, path: str) -> Dict[str, Any]:
                """Create a folder."""
                result = self._orchestrator.base_tools.create_folder(path)
                return {
                    "success": result.success,
                    "data": result.output,
                    "error": result.error,
                }

            async def edit_file(
                self, path: str, edits: List[Dict[str, Any]]
            ) -> Dict[str, Any]:
                """Edit file with multiple edits."""
                try:
                    # Read current content
                    read_result = self._orchestrator.base_tools.read_file(path)
                    if not read_result.success:
                        return {"success": False, "error": read_result.error}

                    content = read_result.output

                    # Apply edits
                    for edit in edits:
                        op = edit.get("op", "replace")
                        path_key = edit.get("path", "")
                        value = edit.get("value", "")

                        if op == "replace":
                            content = content.replace(path_key, value)
                        elif op == "insert":
                            insert_pos = edit.get("insert", 0)
                            content = (
                                content[:insert_pos] + value + content[insert_pos:]
                            )
                        elif op == "delete":
                            delete_start = edit.get("start", 0)
                            delete_end = edit.get("end", len(value))
                            content = content[:delete_start] + content[delete_end:]

                    # Write back
                    write_result = self._orchestrator.base_tools.write_file(
                        path, content
                    )
                    return {
                        "success": write_result.success,
                        "data": write_result.output,
                        "error": write_result.error,
                    }
                except Exception as e:
                    return {"success": False, "error": str(e)}

        self.file_operations = FileOperationsWrapper(self)

    async def initialize(self):
        """Initialize the orchestrator brain."""
        logger.info("Initializing Orchestrator Brain...")

        # Load agent instructions
        self.agent_instructions = self.tool_registry.get_instructions()

        # Set up callbacks (will be set by frontend)
        await self._setup_callbacks()

        logger.info(
            f"Orchestrator Brain initialized with {len(self.tool_registry._tools)} tools"
        )

        return {
            "success": True,
            "message": "Orchestrator Brain initialized successfully",
            "tools_count": len(self.tool_registry._tools),
        }

    async def _setup_callbacks(self):
        """Set up event callbacks for frontend communication."""
        # These will be overridden when frontend connects
        pass

    async def connect_frontend(self, status_cb, thought_cb, action_cb):
        """Connect to frontend and set up callbacks."""
        self.status_callback = status_cb
        self.thought_callback = thought_cb
        self.action_callback = action_cb

        # Emit initial status
        await self._emit_status(
            "connected",
            {
                "tools_count": len(self.tool_registry._tools),
                "agent_instructions_count": len(self.agent_instructions),
            },
        )

        logger.info("Frontend connected")

    async def _emit_status(self, state: str, data: Dict[str, Any]):
        """Emit status update to frontend."""
        self.status_state = state

        if self.status_callback:
            await asyncio.to_thread(self.status_callback, {"state": state, **data})

    async def _emit_thought(self, thought: str):
        """Emit thought to frontend."""
        if self.thought_callback:
            await asyncio.to_thread(self.thought_callback, thought)

    async def _emit_action(self, action: Dict[str, Any]):
        """Emit action result to frontend."""
        if self.action_callback:
            await asyncio.to_thread(self.action_callback, action)

    async def start_mission(self, task: str) -> Dict[str, Any]:
        """
        Start a new mission/task.

        Args:
            task: The mission description

        Returns:
            Mission start result
        """
        self.current_task = task
        self.task_active = True
        self.status_state = "running"

        logger.info(f"Starting mission: {task}")

        # Set dynamic system prompt with available tools
        await self._update_system_prompt()

        # Add initial message to context
        self.context_manager.add_message("user", task)

        # Emit status
        await self._emit_status(
            "running", {"task": task, "tools_available": len(self.tool_registry._tools)}
        )

        # Run the main loop
        try:
            await self._run_orchestration_loop()
        finally:
            self.task_active = False
            self.status_state = "idle"

        return {"success": True, "message": "Mission complete", "task": task}

    def _get_openai_tools(self) -> List[Dict]:
        """Convert internal tools to OpenAI function schema."""
        openai_tools = []
        for name, tool in self.tool_registry._tools.items():
            # Basic parameter schema if not defined
            parameters = {"type": "object", "properties": {}, "required": []}

            # If tool has args_schema, try to use it
            if hasattr(tool, "args_schema") and tool.args_schema:
                parameters = tool.args_schema
            elif hasattr(tool, "args"):
                # Fallback for simple tools
                for arg_name in tool.args:
                    parameters["properties"][arg_name] = {"type": "string"}
                    parameters["required"].append(arg_name)

            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool.description,
                        "parameters": parameters,
                    },
                }
            )
        return openai_tools

    async def _update_system_prompt(self):
        """Update system prompt with current mission and instructions."""
        os_info = f"{sys.platform} {sys.version}"
        prompt = f"""You are the IMMUTABLE CORE Orchestrator Brain.
Your primary directive is to complete missions while expanding system capabilities autonomously.

Environment:
- Operating System: {os_info}
- Shell Capability: {"PowerShell/CMD" if sys.platform == "win32" else "Bash"}

Project Structure:
- core/ : Backend (FastAPI) - Immutable services and modules
- ui/ : Frontend (React) - Observer dashboard
- workspace/ : General sandbox for AI operations
- .agents/tools/ : Dynamic tool registry (backend, ui, scripts, api categories)
- .agents/dynamic_tools/ : Self-generated tools via evolution

Current Mission: {self.current_task}

You are IMMUTABLE CORE Brain, an autonomous mission-critical orchestrator.
Your goal is to complete the assigned MISSION with zero hesitation and absolute technical precision.

REASONING PROTOCOL:
1. Always start your response with a <|think|> block.
2. Inside <|think|>, break down the mission into surgical steps.
3. Use available tools natively to explore and modify the codebase.
"""
        self.system_prompt = prompt
        self.context_manager.set_system_prompt(prompt)

    async def _run_orchestration_loop(self):
        """Main orchestration loop with native tool calling."""
        loop_count = 0
        max_loops = 20

        while self.task_active and loop_count < max_loops:
            loop_count += 1
            logger.info(f"Loop cycle {loop_count}...")

            full_response_content = ""
            tool_calls = []  # To accumulate tool calls from stream

            # Reset thinking engine for new stream
            self.thinking_engine.reset()

            # Prepare tools for LLM
            openai_tools = self._get_openai_tools()

            messages = self.context_manager.get_messages()
            # Ensure the system prompt is fresh
            if not any(m.get("role") == "system" for m in messages):
                messages = [
                    {"role": "system", "content": self.system_prompt}
                ] + messages

            await self._emit_status("thinking", {"loop": loop_count})

            async for chunk in self.llm_bridge.chat_stream(
                messages, tools=openai_tools
            ):
                # Check for content
                content = chunk.get("content")
                if content:
                    # Process via thinking engine to extract <|think|> blocks
                    clean_chunk, thought = self.thinking_engine.process_chunk(content)
                    if thought:
                        await self._emit_thought(thought)

                    if clean_chunk:
                        full_response_content += clean_chunk

                # Check for native tool calls
                delta_tool_calls = chunk.get("tool_calls")
                if delta_tool_calls:
                    for tc in delta_tool_calls:
                        idx = tc.get("index", 0)
                        while len(tool_calls) <= idx:
                            tool_calls.append(
                                {
                                    "id": "",
                                    "type": "function",
                                    "function": {"name": "", "arguments": ""},
                                }
                            )

                        if tc.get("id"):
                            tool_calls[idx]["id"] += tc["id"]

                        fn = tc.get("function", {})
                        if fn.get("name"):
                            tool_calls[idx]["function"]["name"] += fn["name"]
                        if fn.get("arguments"):
                            tool_calls[idx]["function"]["arguments"] += fn["arguments"]

            # Finalize assistant message
            assistant_msg = {"role": "assistant"}
            if full_response_content:
                assistant_msg["content"] = full_response_content
            if tool_calls:
                # Filter out incomplete tool calls
                tool_calls = [tc for tc in tool_calls if tc["function"]["name"]]
                if tool_calls:
                    assistant_msg["tool_calls"] = tool_calls

            self.context_manager.add_message("assistant", assistant_msg)

            # Handle tool calls if any
            if not tool_calls:
                if not full_response_content:
                    logger.warning("Empty response from LLM, ending loop.")
                    break

                # Check for conclusion markers
                conclusions = ["MISSION COMPLETE", "DONE", "TASK FINISHED"]
                if any(c in full_response_content.upper() for c in conclusions):
                    logger.info("Mission concluded by LLM.")
                    break
                continue

            # Execute actions
            await self._emit_status("executing", {"actions": len(tool_calls)})

            for tc in tool_calls:
                tool_id = tc.get("id", "call_" + str(int(time.time())))
                tool_name = tc["function"]["name"]
                args_str = tc["function"]["arguments"]

                try:
                    args = json.loads(args_str) if args_str else {}
                except Exception as e:
                    logger.error(f"Failed to parse tool arguments for {tool_name}: {e}")
                    self.context_manager.add_message(
                        "tool",
                        f"Error: Invalid JSON arguments: {str(e)}",
                        tool_call_id=tool_id,
                    )
                    continue

                logger.info(f"Executing native action: {tool_name}({args})")
                await self._emit_action({"tool": tool_name, "args": args})

                try:
                    result = await self.tool_registry.execute_tool(tool_name, args)
                    # Add result to context with tool_call_id
                    self.context_manager.add_message(
                        "tool", json.dumps(result), tool_call_id=tool_id
                    )
                except Exception as e:
                    logger.exception(f"Exception during tool execution: {e}")
                    self.context_manager.add_message(
                        "tool", f"Runtime Error: {str(e)}", tool_call_id=tool_id
                    )

    async def run_self_improvement_loop(self, mission: str = None) -> Dict[str, Any]:
        """
        Run the self-improvement loop for admin mode.

        This method:
        1. Tests all loaded modules
        2. Analyzes errors
        3. Attempts auto-fixes
        4. Registers new tools if beneficial

        Args:
            mission: Optional directive to focus the evolution cycle.

        Returns:
            Loop result dict with errors_fixed and total_errors at top level
        """
        logger.info("Running self-improvement loop...")

        # Test all modules
        for category, modules in self.auto_adaptation.modules.items():
            for name, info in modules.items():
                await self.auto_adaptation.test_module(name, category)

        # Run auto-fix loop and extract errors_fixed/total_errors directly
        inner_result = await self.auto_adaptation.run_self_improvement_loop(mission)

        # MISSION EXECUTION: If a mission is provided, run the orchestration loop to fulfill it
        if mission:
            logger.info(f"Fulfilling mission directive: {mission}")
            self.current_task = mission
            self.task_active = True
            await self._update_system_prompt()
            self.context_manager.add_message("user", f"Mission Directive: {mission}")

            # Run one cycle of the orchestration loop
            await self._run_orchestration_loop()

        # Save adaptation log
        await self.tool_registry.save_adaptation_log()

        return {
            "success": True,
            "message": "Evolution cycle completed"
            if mission
            else "Self-improvement loop completed",
            "errors_fixed": inner_result.get("errors_fixed", 0),
            "total_errors": inner_result.get("total_errors", 0),
        }

    async def load_agent_instructions(
        self, instructions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Load agent instructions from a list."""
        self.agent_instructions = instructions
        self.tool_registry.save_instructions(instructions)

        # Update system prompt
        await self._update_system_prompt()

        logger.info(f"Loaded {len(instructions)} agent instructions")

        return {
            "success": True,
            "count": len(instructions),
            "message": f"Loaded {len(instructions)} agent instructions",
        }

    async def load_instructions_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load agent instructions from a JSON file."""
        import json

        try:
            with open(file_path, "r") as f:
                instructions = json.load(f)

            self.agent_instructions = instructions
            self.tool_registry.save_instructions(instructions)

            # Update system prompt
            await self._update_system_prompt()

            logger.info(f"Loaded {len(instructions)} agent instructions from file")

            return {
                "success": True,
                "count": len(instructions),
                "file_path": file_path,
                "message": f"Loaded {len(instructions)} agent instructions from {file_path}",
            }
        except Exception as e:
            logger.error(f"Failed to load instructions from file {file_path}: {e}")
            return {"success": False, "error": str(e), "file_path": file_path}

    async def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status."""
        return {
            "state": self.status_state,
            "task_active": self.task_active,
            "current_task": self.current_task,
            "tools_count": len(self.tool_registry._tools),
            "modules_count": sum(len(m) for m in self.auto_adaptation.modules.values()),
            "agent_instructions_count": len(self.agent_instructions),
            "adaptation_stats": self.tool_registry.get_adaptation_stats(),
            "auto_adaptation_stats": self.auto_adaptation.get_adaptation_stats(),
        }

    async def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered tools."""
        return await self.tool_registry.list_tools(category)

    async def register_tool(
        self,
        name: str,
        description: str,
        code: str,
        schema: Optional[Dict[str, Any]] = None,
        category: str = "backend",
    ) -> Dict[str, Any]:
        """Register a new tool."""
        return await self.tool_registry.register_tool(
            name=name,
            description=description,
            code=code,
            schema=schema,
            category=category,
        )

    async def hot_load_tool(self, name: str) -> Dict[str, Any]:
        """Hot-load a tool."""
        return await self.tool_registry.hot_load_tool(name)

    async def remove_tool(self, name: str) -> Dict[str, Any]:
        """Remove a tool."""
        return await self.tool_registry.remove_tool(name)
