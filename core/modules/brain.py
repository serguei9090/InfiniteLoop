import logging
from typing import Dict, Any, Optional

from modules.base_tools import BaseTools
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.auto_adaptation import AutoAdaptationEngine
from modules.architect import architect_agent, MissionPlan
from modules.coder import SmolAgentWrapper

logger = logging.getLogger(__name__)

class BrainOrchestrator:
    """The central intelligence hub implementing the Hybrid Vibe-Coding Stack."""
    def __init__(self, workspace_root: str = ".", target_workspace: str = "workspace"):
        self.workspace_root = workspace_root
        self.target_workspace = target_workspace

        # Initialize Base Environment
        self.guard = WorkspaceGuard(str(self.workspace_root))
        self.context_engine = ContextEngine()
        self.evolution = EvolutionEngine(str(self.workspace_root + "/.agents/dynamic_tools"))
        self.auto_adaptation = AutoAdaptationEngine(str(self.workspace_root))
        self.base_tools = BaseTools(self.guard, self.context_engine, self.evolution)

        # Initialize the 'Hands' (SmolAgents execution loop)
        self.coder = SmolAgentWrapper(self.base_tools, str(self.workspace_root))

        self.task_active = False

    async def initialize(self) -> Dict[str, Any]:
        """Setup environments and verify proxy connection."""
        logger.info("Initializing Hybrid Brain Orchestrator...")
        return {"success": True, "message": "Brain ready."}

    async def start_mission(self, mission_text: str) -> Dict[str, Any]:
        """
        Execute the hybrid workflow:
        1. Architect (PydanticAI) breaks down the mission into a deterministic MissionPlan.
        2. Coder (SmolAgents) executes the atomic tasks.
        """
        self.task_active = True
        logger.info(f"Starting Mission: {mission_text}")

        try:
            # Phase A: Planning (The Architect)
            logger.info("Phase A: Architecting Plan...")
            # We use an async call to PydanticAI
            result = await architect_agent.run(mission_text)
            plan: MissionPlan = result.data

            logger.info(f"Plan created with {len(plan.tasks)} atomic tasks.")

            # Phase B: Execution (The Surgical Coder)
            for i, task in enumerate(plan.tasks):
                logger.info(f"Executing Task {i+1}/{len(plan.tasks)}: {task.task_id}")

                # Hand off to SmolAgents for execution and verification
                coder_result = await self.coder.run_task(
                    task_description=task.description,
                    target_file=task.target_file,
                    verification=task.verification_step
                )

                if not coder_result["success"]:
                    logger.error(f"Task {task.task_id} failed: {coder_result.get('error')}")
                    return {"success": False, "error": f"Failed at task {task.task_id}"}

                logger.info(f"Task {task.task_id} completed successfully.")

            return {"success": True, "message": "Mission accomplished."}

        except Exception as e:
            logger.exception(f"Mission failed with error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.task_active = False
