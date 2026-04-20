from fastapi import APIRouter
from typing import Any, Dict, List

router = APIRouter()

# Define system architecture as skill tree structure
SYSTEM_SKILL_TREE = {
    "root": "IMMUTABLE CORE",
    "version": "1.0.0",
    "modules": [
        {
            "name": "dashboard",
            "path": "core.modules.dashboard_router",
            "endpoint": "/dashboard",
            "method": "GET",
            "capabilities": ["metrics", "status", "connections"],
            "dependencies": [],
        },
        {
            "name": "services.llm_bridge",
            "path": "services.llm_bridge",
            "endpoint": "/api/llm/*",
            "method": "POST",
            "capabilities": ["llm_calls", "context_management"],
            "dependencies": [],
        },
        {
            "name": "services.loop_orchestrator",
            "path": "services.loop_orchestrator",
            "endpoint": "/task/*",
            "method": "POST",
            "capabilities": ["task_execution", "background_processing"],
            "dependencies": ["llm_bridge"],
        },
    ],
    "endpoints": [
        {"path": "/", "method": "GET", "description": "UI Home"},
        {"path": "/health", "method": "GET", "description": "Health Check"},
        {"path": "/task/start", "method": "POST", "description": "Start Task"},
        {"path": "/task/stop", "method": "POST", "description": "Stop Task"},
        {"path": "/ws", "method": "GET", "description": "WebSocket Connection"},
    ],
}


@router.get("/skill-tree")
async def get_skill_tree() -> Dict[str, Any]:
    """Returns the system skill tree showing all modules and their relationships."""
    return SYSTEM_SKILL_TREE


@router.get("/skill-tree/modules")
async def get_modules_tree() -> List[Dict[str, Any]]:
    """Returns just the modules section of the skill tree."""
    return SYSTEM_SKILL_TREE["modules"]


@router.get("/skill-tree/endpoints")
async def get_endpoints_tree() -> List[Dict[str, Any]]:
    """Returns the endpoints section of the skill tree."""
    return SYSTEM_SKILL_TREE["endpoints"]
