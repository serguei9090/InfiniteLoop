"""
ADK Orchestrator - Google ADK 2.0 based Autonomous Agent
PURPOSE: Drive the InfiniteLoop mission using standardized ADK workflows.
CONTRACT:
- initialize(): Builds the LlmAgent with the Immutable Core v4 toolset.
- start_mission(mission_text): Executes a mission via the ADK runner.
- run_self_improvement_loop(): Triggers the auto-adaptation engine.
"""

import logging
import asyncio
import time
import os
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
from modules.base_tools import BaseTools
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.auto_adaptation import AutoAdaptationEngine

logger = logging.getLogger(__name__)


class ADKOrchestrator:
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

        # ADK Components
        self.agent: Optional[LlmAgent] = None
        self.runner: Optional[InMemoryRunner] = None

        # Callbacks
        self.status_callback: Optional[Callable] = None
        self.thought_callback: Optional[Callable] = None
        self.action_callback: Optional[Callable] = None

        # Telemetry
        self.tool_metrics: Dict[str, Dict[str, int]] = {}
        self.event_history: List[Any] = []
        self.start_time = time.time()

    async def initialize(self) -> Dict[str, Any]:
        """Build the ADK Agent with the v4 toolset."""
        if not self.runner:
            logger.info("Initializing ADK Orchestrator [IMMUTABLE CORE v4]...")

            # Configure LiteLLM (defaults for LM Studio)
            os.environ.setdefault("OPENAI_API_BASE", "http://127.0.0.1:1234/v1")
            os.environ.setdefault("OPENAI_API_KEY", "lm-studio")

            self.agent = LlmAgent(
                name="IMMUTABLE_CORE_ORCHESTRATOR",
                description="Autonomous mission-critical orchestrator for InfiniteLoop.",
                instruction=self._get_base_instructions(),
                tools=[
                    self.base_tools.read_file,
                    self.base_tools.write_file,
                    self.base_tools.delete_file,
                    self.base_tools.create_folder,
                    self.base_tools.execute_cmd,
                    self.base_tools.glob_search,
                    self.base_tools.grep_search,
                    self.base_tools.web_fetch,
                    self.base_tools.create_new_tool,
                ],
                model=LiteLlm(model="openai/qwen3.5-9b"),
            )

            self.runner = InMemoryRunner(agent=self.agent, app_name="InfiniteLoop")
            logger.info("ADK Agent initialized with v4 boundaries.")

        return {"success": True, "message": "ADK Orchestrator v4 ready"}

    async def start_mission(self, mission_text: str) -> Dict[str, Any]:
        """Run the ADK mission loop."""
        if not self.runner:
            await self.initialize()

        self.task_active = True
        self.current_task = mission_text

        try:
            logger.info(f"Starting mission: {mission_text}")

            new_message = types.Content(
                role="user", parts=[types.Part(text=mission_text)]
            )

            session_id = "default_session"
            user_id = "default_user"

            # Check/Create session
            session = await self.runner.session_service.get_session(
                app_name=self.runner.app_name, user_id=user_id, session_id=session_id
            )
            if not session:
                await self.runner.session_service.create_session(
                    app_name=self.runner.app_name,
                    user_id=user_id,
                    session_id=session_id,
                )

            async for event in self.runner.run_async(
                user_id=user_id, session_id=session_id, new_message=new_message
            ):
                self.event_history.append(event)
                if len(self.event_history) > 100:
                    self.event_history.pop(0)

                # Output processing
                if event.content and event.content.parts:
                    content_str = "".join(
                        [p.text for p in event.content.parts if p.text]
                    )
                    if content_str and event.author == "model":
                        await self._emit_thought(content_str)

                # Tool call processing
                if event.actions:
                    await self._emit_action(
                        event.actions.to_dict()
                        if hasattr(event.actions, "to_dict")
                        else str(event.actions)
                    )

            logger.info("ADK Mission Complete.")
            return {"success": True, "message": "Mission ended successfully"}

        except Exception as e:
            logger.exception(f"ADK Execution Error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.task_active = False

    def _get_base_instructions(self) -> str:
        return f"""[IMMUTABLE CORE v4]
ENVIRONMENT: Windows (PowerShell). 
- COMMANDS: Use 'dir', 'type', 'Get-ChildItem'.
- DIRECTORIES: Use 'create_folder' tool before writing files to new paths.
- SYNTAX: Avoid Linux-style chaining (&&, ||, 2>&1). PowerShell uses ';' for chaining and 'Test-Path' for checks.
- PATHS: All paths MUST be relative to {self.workspace_dir_name}/ root. Use forward slashes '/' for compatibility.

DIRECTIVE: Complete the MISSION with absolute precision.
BOUNDARIES:
- core/ & ui/ : READ-ONLY. 
- {self.workspace_dir_name}/  : READ-WRITE. Your sandbox.

REASONING:
1. <|think|> block mandatory. 
2. Read/Verify before acting.
3. Use 'compressed' mode for large files.

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
            "tools_count": len(self.agent.tools) if self.agent else 0,
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
