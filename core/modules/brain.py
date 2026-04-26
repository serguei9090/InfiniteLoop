import logging
from typing import Dict, Any

from modules.base_tools import BaseTools
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.auto_adaptation import AutoAdaptationEngine
from modules.architect import architect_agent, MissionPlan
from modules.coder import SmolAgentWrapper
from modules.beads_tracker import BeadsTracker
import asyncio

logger = logging.getLogger(__name__)


class BrainOrchestrator:
    """The central intelligence hub implementing the Hybrid Vibe-Coding Stack."""

    def __init__(self, workspace_root: str = ".", target_workspace: str = "workspace"):
        self.workspace_root = workspace_root
        self.target_workspace = target_workspace

        # Initialize Base Environment
        self.guard = WorkspaceGuard(str(self.workspace_root))
        self.context_engine = ContextEngine()
        self.evolution = EvolutionEngine(
            str(self.workspace_root + "/.agents/dynamic_tools")
        )
        self.auto_adaptation = AutoAdaptationEngine(str(self.workspace_root))
        self.base_tools = BaseTools(self.guard, self.context_engine, self.evolution)

        # Initialize the 'Hands' (SmolAgents execution loop)
        self.coder = SmolAgentWrapper(self.base_tools, str(self.workspace_root))
        self.beads_tracker = BeadsTracker(str(self.workspace_root))

        self.task_active = False
        self.autonomous_loop_active = False

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

            # Phase B: Planning to Beads Database
            for task in plan.tasks:
                desc = f"Target: {task.target_file}\nVerification: {task.verification_step}\nDescription: {task.description}"
                issue_id = self.beads_tracker.add_issue(
                    title=f"Task: {task.task_id}", description=desc
                )
                logger.info(f"Added task {task.task_id} as Bead issue {issue_id}")

            return {
                "success": True,
                "message": f"Mission planned. {len(plan.tasks)} tasks added to Beads tracker.",
            }

        except Exception as e:
            logger.exception(f"Mission failed with error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.task_active = False
        self.autonomous_loop_active = False

    async def run_autonomous_loop(self):
        """Continuously poll Beads issues and execute them."""
        if self.autonomous_loop_active:
            logger.info("Autonomous loop already running.")
            return

        self.autonomous_loop_active = True
        logger.info("Starting Autonomous Infinite Loop (Beads Tracker)...")

        try:
            while self.autonomous_loop_active:
                open_issues = self.beads_tracker.get_open_issues()

                if not open_issues:
                    # No tasks, wait and poll again
                    await asyncio.sleep(5)
                    continue

                # Get the first open issue
                issue = open_issues[0]
                issue_id = issue["id"]

                logger.info(f"Picked up issue {issue_id}: {issue['title']}")

                # Try to parse the description back into parts if possible
                desc = issue.get("description", "")
                target_file = ""
                verification = ""
                task_desc = desc

                lines = desc.split("\n")
                for line in lines:
                    if line.startswith("Target: "):
                        target_file = line.replace("Target: ", "")
                    elif line.startswith("Verification: "):
                        verification = line.replace("Verification: ", "")
                    elif line.startswith("Description: "):
                        task_desc = line.replace("Description: ", "")

                # Execute via Coder
                self.beads_tracker.update_status(issue_id, "in_progress")

                coder_result = await self.coder.run_task(
                    task_description=task_desc,
                    target_file=target_file,
                    verification=verification,
                )

                if coder_result["success"]:
                    logger.info(f"Issue {issue_id} completed successfully.")
                    self.beads_tracker.update_status(
                        issue_id, "closed", "Completed via SmolAgent"
                    )
                else:
                    logger.error(
                        f"Issue {issue_id} failed: {coder_result.get('error')}"
                    )
                    self.beads_tracker.update_status(
                        issue_id, "failed", str(coder_result.get("error"))[:200]
                    )

                # Short pause before next task
                await asyncio.sleep(2)

        except Exception as e:
            logger.exception(f"Autonomous loop crashed: {e}")
            self.autonomous_loop_active = False

    def stop_autonomous_loop(self):
        """Stop the autonomous polling loop."""
        self.autonomous_loop_active = False
        logger.info("Stopping Autonomous Infinite Loop...")
