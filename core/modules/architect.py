from config import settings
from pydantic import BaseModel, Field
from typing import List
from pydantic_ai import Agent
import os


class AtomicTask(BaseModel):
    task_id: str = Field(description="A unique identifier for the task, e.g., 'task_1'")
    description: str = Field(
        description="A detailed description of the task to perform"
    )
    target_file: str = Field(description="The primary file to modify or read")
    verification_step: str = Field(
        description="The command or step to run to verify the task succeeded"
    )


class MissionPlan(BaseModel):
    mission_objective: str = Field(description="The overall goal of the mission")
    tasks: List[AtomicTask] = Field(
        description="The sequence of tasks to complete the mission"
    )


os.environ["OPENAI_API_KEY"] = settings.architect_api_key
os.environ["OPENAI_BASE_URL"] = settings.architect_base_url

# In pydantic_ai 0.18.5+ result_type is passed as a type hint or parameter to run()
architect_agent = Agent(
    "openai:gemma-3-27b-it",
    system_prompt="""You are the Architect. Your job is to break down complex software engineering missions into
atomic, deterministic tasks. Each task must have a clear target file and a verification step (like running a test or linter).
Do not attempt to execute the code. Only produce the plan.""",
)
