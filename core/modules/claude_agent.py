"""
Claude Orchestrator - Agent SDK based Autonomous Agent
PURPOSE: Drive the InfiniteLoop mission using standardized Claude Agent workflows.
CONTRACT:
- initialize(): Builds the Claude SDK client with the Immutable Core v4 toolset.
- start_mission(mission_text): Executes a mission via the Claude Agent SDK query.
- run_self_improvement_loop(): Triggers the auto-adaptation engine.
"""

import logging
import asyncio
import time
import os
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

from claude_agent_sdk import query, create_sdk_mcp_server, tool
from claude_agent_sdk.types import ClaudeAgentOptions, AssistantMessage, StreamEvent

from modules.base_tools import BaseTools
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.auto_adaptation import AutoAdaptationEngine

logger = logging.getLogger(__name__)


class ClaudeOrchestrator:
    def __init__(self, workspace_root: str = ".", target_workspace: str = "workspace"):
        self.project_root = Path(workspace_root).resolve()
        
        # Allows routing between 'workspace' (autoevolve) and 'UserWorkspace/AppX' (user apps)
        self.workspace_dir_name = target_workspace
        self.workspace_root = (self.project_root / self.workspace_dir_name).resolve()

        # Initialize dependencies
        self.guard = WorkspaceGuard(str(self.workspace_root))
        self.context_engine = ContextEngine()
        self.evolution = EvolutionEngine(
            str(self.workspace_root / ".agents" / "dynamic_tools")
        )
        self.auto_adaptation = AutoAdaptationEngine(str(self.workspace_root))

        # Internal tools
        self.base_tools = BaseTools(self.guard, self.context_engine, self.evolution)

        # State
        self.task_active = False
        self.current_task: Optional[str] = None

        # Callbacks
        self.status_callback: Optional[Callable] = None
        self.thought_callback: Optional[Callable] = None
        self.action_callback: Optional[Callable] = None

        # Telemetry
        self.tool_metrics: Dict[str, Dict[str, int]] = {}
        self.event_history: List[Any] = []
        self.start_time = time.time()

        self.custom_mcp_server = None

    async def initialize(self) -> Dict[str, Any]:
        """Build the Claude Agent dependencies with the v4 toolset."""
        logger.info("Initializing Claude Orchestrator [IMMUTABLE CORE v4]...")

        # Configure defaults for LM Studio
        os.environ.setdefault("ANTHROPIC_BASE_URL", "http://127.0.0.1:1234/v1")
        os.environ.setdefault("ANTHROPIC_API_KEY", "lm-studio")

        # Create MCP server for custom tools
        @tool("create_new_tool", "Creates and registers a new dynamic tool.", {"name": str, "code": str, "schema": str})
        async def sdk_create_new_tool(args):
            result = await self.base_tools.create_new_tool(args["name"], args["code"], args["schema"])
            is_error = not result["success"]
            return {"content": [{"type": "text", "text": str(result)}], "is_error": is_error}

        self.custom_mcp_server = create_sdk_mcp_server(
            name="core_custom",
            version="1.0.0",
            tools=[sdk_create_new_tool]
        )

        logger.info("Claude Agent initialized with v4 boundaries.")
        return {"success": True, "message": "Claude Orchestrator v4 ready"}

    async def start_mission(self, mission_text: str) -> Dict[str, Any]:
        """Run the Claude SDK mission loop."""
        if not self.custom_mcp_server:
            await self.initialize()

        self.task_active = True
        self.current_task = mission_text

        try:
            logger.info(f"Starting mission: {mission_text}")

            options = ClaudeAgentOptions(
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "WebSearch", "AskUserQuestion", "Monitor"],
                mcp_servers={"core_custom": self.custom_mcp_server},
                system_prompt=self._get_base_instructions(),
                cwd=self.workspace_root
            )

            async for message in query(prompt=mission_text, options=options):
                self.event_history.append(message)
                if len(self.event_history) > 100:
                    self.event_history.pop(0)

                # Output processing
                if isinstance(message, AssistantMessage):
                    if hasattr(message, "content") and isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, "type"):
                                if block.type == "text" and hasattr(block, "text"):
                                    await self._emit_thought(block.text)
                                elif block.type == "thinking" and hasattr(block, "thinking"):
                                    await self._emit_thought(block.thinking)

                elif isinstance(message, StreamEvent):
                    if hasattr(message, "delta") and hasattr(message.delta, "type"):
                        if message.delta.type == "text_delta" and hasattr(message.delta, "text"):
                            await self._emit_thought(message.delta.text)
                    if hasattr(message, "event_type") and message.event_type == "tool_use":
                        await self._emit_action({"tool": getattr(message, "tool_name", "unknown")})

                # Check for ToolUseBlock in AssistantMessage
                if isinstance(message, AssistantMessage) and hasattr(message, "content") and isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, "type") and block.type == "tool_use":
                            await self._emit_action({"name": block.name, "input": block.input})

            logger.info("Claude Mission Complete.")
            return {"success": True, "message": "Mission ended successfully"}

        except Exception as e:
            logger.exception(f"Claude Execution Error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.task_active = False

    def _get_base_instructions(self) -> str:
        return f"""[IMMUTABLE CORE v4]
ENVIRONMENT: Windows (PowerShell). 
- COMMANDS: Use 'dir', 'type', 'Get-ChildItem'.
- DIRECTORIES: Use 'Bash' tool to execute PowerShell commands.
- SYNTAX: Avoid Linux-style chaining (&&, ||, 2>&1). PowerShell uses ';' for chaining and 'Test-Path' for checks.
- PATHS: All paths MUST be relative to {self.workspace_dir_name}/ root. Use forward slashes '/' for compatibility.

DIRECTIVE: Complete the MISSION with absolute precision.
BOUNDARIES:
- core/ & ui/ : READ-ONLY. 
- {self.workspace_dir_name}/  : READ-WRITE. Your sandbox.

REASONING:
1. <|think|> block mandatory. 
2. Read/Verify before acting.

TERMINATION: Output "TASK_COMPLETE" when finished.
"""

    async def register_tool(
        self,
        name: str,
        description: str,
        code: str,
        schema: Optional[dict] = None,
        category: str = "backend",
    ) -> Dict[str, Any]:
        """Register dynamic tool."""
        return await self.base_tools.create_new_tool(name, code, str(schema))

    async def hot_load_tool(self, name: str, category: str = "backend") -> Dict[str, Any]:
        """Hot-load a tool from the workspace."""
        tool_path = self.workspace_root / ".agents" / "dynamic_tools" / name / "src" / f"{name}.py"
        return await self.auto_adaptation.hot_load_module(name, category, tool_path)

    async def remove_tool(self, name: str, category: str = "backend") -> Dict[str, Any]:
        """Remove a tool from the registry."""
        if category in self.auto_adaptation.modules and name in self.auto_adaptation.modules[category]:
            del self.auto_adaptation.modules[category][name]
            return {"success": True, "message": f"Tool {name} removed from registry"}
        return {"success": False, "error": f"Tool {name} not found"}

    async def run_self_improvement_loop(self) -> Dict[str, Any]:
        """Trigger the auto-adaptation process."""
        return await self.auto_adaptation.run_self_improvement_loop()

    async def get_adaptation_stats(self) -> Dict[str, Any]:
        """Get adaptation engine statistics."""
        return self.auto_adaptation.get_adaptation_stats()

    async def list_adaptation_modules(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all managed modules."""
        return self.auto_adaptation.get_all_modules()

    async def test_adaptation_module(self, name: str, category: str) -> Dict[str, Any]:
        """Test a specific adaptation module."""
        return await self.auto_adaptation.test_module(name, category)

    async def get_status(self) -> Dict[str, Any]:
        return {
            "status": "online",
            "task_active": self.task_active,
            "current_task": self.current_task,
            "tools_count": 11,  # Approximate base count
            "uptime": int(time.time() - self.start_time),
        }

    async def _emit_thought(self, thought: str):
        if self.thought_callback:
            if asyncio.iscoroutinefunction(self.thought_callback):
                await self.thought_callback(thought)
            else:
                await asyncio.to_thread(self.thought_callback, thought)

    async def _emit_action(self, action: Dict):
        if self.action_callback:
            if asyncio.iscoroutinefunction(self.action_callback):
                await self.action_callback(action)
            else:
                await asyncio.to_thread(self.action_callback, action)
