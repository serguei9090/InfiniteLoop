import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from modules.brain import BrainOrchestrator
from modules.architect import MissionPlan, AtomicTask


@pytest.fixture
def mock_dependencies():
    with (
        patch("modules.brain.WorkspaceGuard"),
        patch("modules.brain.ContextEngine"),
        patch("modules.brain.EvolutionEngine"),
        patch("modules.brain.AutoAdaptationEngine"),
        patch("modules.brain.BaseTools"),
        patch("modules.brain.SmolAgentWrapper"),
        patch("modules.brain.BeadsTracker"),
    ):
        yield


@pytest.mark.asyncio
async def test_brain_initialization(mock_dependencies):
    brain = BrainOrchestrator("/fake/root")
    assert brain.workspace_root == "/fake/root"
    assert brain.task_active is False

    result = await brain.initialize()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_start_mission_success(mock_dependencies):
    brain = BrainOrchestrator("/fake/root")

    # Mock Architect result
    fake_plan = MissionPlan(
        mission_objective="Test",
        tasks=[
            AtomicTask(
                task_id="t1",
                description="desc",
                target_file="f1",
                verification_step="v1",
            )
        ],
    )
    fake_result = MagicMock()
    fake_result.data = fake_plan

    with patch(
        "modules.brain.architect_agent.run", new_callable=AsyncMock
    ) as mock_architect_run:
        mock_architect_run.return_value = fake_result

        result = await brain.start_mission("Do something")

        assert result["success"] is True
        mock_architect_run.assert_called_once()
        brain.beads_tracker.add_issue.assert_called_once()


@pytest.mark.asyncio
async def test_start_mission_coder_failure(mock_dependencies):
    # This test is no longer testing coder failure during start_mission
    # It instead tests exception handling during start_mission
    brain = BrainOrchestrator("/fake/root")

    with patch(
        "modules.brain.architect_agent.run", new_callable=AsyncMock
    ) as mock_architect_run:
        mock_architect_run.side_effect = Exception("Planning failed")

        result = await brain.start_mission("Do something")

        assert result["success"] is False
        assert "Planning failed" in result["error"]
