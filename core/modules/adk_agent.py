import logging
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import InMemoryRunner
from modules.base_tools import BaseTools
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.auto_adaptation import AutoAdaptationEngine

logger = logging.getLogger(__name__)

class ADKOrchestrator:
    """
    Orchestrator powered by Google ADK 2.0.
    Replaces the legacy OrchestratorBrain with a modern Runner.
    """
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        
        # Initialize dependencies
        self.guard = WorkspaceGuard(str(self.workspace_root))
        self.context_engine = ContextEngine()
        self.evolution = EvolutionEngine(str(self.workspace_root / ".agents" / "dynamic_tools"))
        self.auto_adaptation = AutoAdaptationEngine(str(self.workspace_root))
        
        # Initialize internal tools
        self.base_tools = BaseTools(self.guard, self.context_engine, self.evolution)
        
        # State tracking
        self.task_active = False
        self.current_task: Optional[str] = None
        
        # ADK Components (Agents are LlmAgent in this version)
        self.agent: Optional[LlmAgent] = None
        self.runner: Optional[InMemoryRunner] = None
        
        # Callbacks (for UI)
        self.status_callback = None
        self.thought_callback = None
        self.action_callback = None

    async def initialize(self):
        """Build the ADK Agent with our toolset."""
        logger.info("Initializing ADK Orchestrator...")
        
        # Define the agent
        self.agent = LlmAgent(
            name="IMMUTABLE_CORE_AGENT",
            description="Autonomous orchestrator for the InfiniteLoop environment.",
            instruction=self._get_base_instructions(),
            tools=[
                self.base_tools.read_file,
                self.base_tools.write_file,
                self.base_tools.delete_file,
                self.base_tools.create_folder,
                self.base_tools.execute_cmd,
                self.base_tools.create_new_tool
            ],
            model="local-model" 
        )
        
        # Setup the runner
        self.runner = InMemoryRunner(agent=self.agent, app_name="InfiniteLoop")
        
        logger.info("ADK Agent and Runner defined with native tools.")
        return {"success": True, "message": "ADK Orchestrator ready"}

    async def get_status(self) -> Dict[str, Any]:
        """Proxy for health/status checks."""
        return {
            "status": "online",
            "task_active": self.task_active,
            "current_task": self.current_task,
            "tools_count": 6, # Base tools
            "agent_instructions_count": 0
        }

    async def list_tools(self, category: Optional[str] = None) -> List[Dict]:
        """List registered tools."""
        # For ADK, we'd list agent.tools.
        # Placeholder for compatibility.
        return [{"name": tool.__name__, "description": tool.__doc__} for tool in self.agent.tools] if self.agent else []

    async def register_tool(self, name: str, description: str, code: str, schema: Optional[dict] = None, category: str = "backend"):
        """Register dynamic tool."""
        return await self.base_tools.create_new_tool(name, code, str(schema))

    async def run_self_improvement_loop(self) -> Dict[str, Any]:
        """Proxy for self-improvement loop."""
        return await self.auto_adaptation.run_self_improvement_loop()

    def _get_base_instructions(self) -> str:
        return """
        You are the IMMUTABLE CORE Brain.
        Your goal is to complete missions with technical precision.
        
        REASONING:
        1. Always start your response with <|think|> blocks.
        2. Break down the task into small, verifiable steps.
        3. Use tools to verify your assumptions before editing.
        
        You have full access to the workspace.
        """

    async def start_mission(self, mission_text: str):
        """Run the ADK mission loop via run_async generator."""
        if not self.runner:
            await self.initialize()
            
        self.task_active = True
        self.current_task = mission_text
        
        try:
            logger.info(f"Starting mission via ADK Runner: {mission_text}")
            
            # ADK 2.0 expects a Content object for new_message
            from google.genai import types
            new_message = types.Content(parts=[types.Part(text=mission_text)])
            
            # Run the agent mission (async generator)
            async for event in self.runner.run_async(
                user_id="default_user",
                session_id="default_session",
                new_message=new_message
            ):
                # Process ADK Events and emit to UI
                if event.content and event.content.parts:
                    content_str = "".join([p.text for p in event.content.parts if p.text])
                    if event.author == "model":
                        await self._emit_thought(content_str)
                
                if event.actions:
                    await self._emit_action(event.actions.to_dict() if hasattr(event.actions, 'to_dict') else str(event.actions))

            logger.info("ADK Mission Complete.")
            return {"success": True, "message": "Mission ended successfully"}
            
        except Exception as e:
            logger.exception(f"ADK Execution Error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.task_active = False

    async def _emit_status(self, state: str, data: Dict):
        if self.status_callback:
            await asyncio.to_thread(self.status_callback, {"state": state, **data})

    async def _emit_thought(self, thought: str):
        if self.thought_callback:
            await asyncio.to_thread(self.thought_callback, thought)

    async def _emit_action(self, action: Dict):
        if self.action_callback:
            await asyncio.to_thread(self.action_callback, action)
