import pytest
from pydantic import ValidationError
from modules.architect import AtomicTask, MissionPlan


def test_atomic_task_validation():
    # Valid
    task = AtomicTask(
        task_id="t1",
        description="Fix the bug",
        target_file="app.py",
        verification_step="pytest",
    )
    assert task.task_id == "t1"

    # Missing required fields
    with pytest.raises(ValidationError):
        AtomicTask(task_id="t1", description="Fix the bug")


def test_mission_plan_validation():
    # Valid
    plan = MissionPlan(
        mission_objective="Refactor app",
        tasks=[
            AtomicTask(
                task_id="t1",
                description="Fix the bug",
                target_file="app.py",
                verification_step="pytest",
            )
        ],
    )
    assert len(plan.tasks) == 1

    # Missing required fields
    with pytest.raises(ValidationError):
        MissionPlan(mission_objective="Refactor app")
