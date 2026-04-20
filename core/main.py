"""
IMMUTABLE CORE API - Main FastAPI Application
Provides REST and WebSocket endpoints for orchestrator brain communication.
"""

from typing import List, Any, Optional
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import importlib.util
import sys
import asyncio
from pathlib import Path

# Import ADK orchestrator
from modules.adk_agent import ADKOrchestrator

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = (BASE_DIR / "../ui").resolve()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(
                    {"success": True, "data": message, "error": None}
                )
            except Exception as e:
                logger.error(f"Broadcast error: {e}")

    async def send_personal(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json({"success": True, "data": message, "error": None})
        except Exception as e:
            logger.error(f"Personal send error: {e}")


manager = ConnectionManager()

# Mount UI static files
app = FastAPI(title="IMMUTABLE CORE API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if UI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(UI_DIR)), name="static")

# ==================== DYNAMIC APP DISCOVERY ====================


def discover_plugins():
    """Scan workspace/ for router.py files and include them."""
    project_root = BASE_DIR.parent.resolve()
    workspace_path = project_root / "workspace"

    if not workspace_path.exists():
        logger.warning(f"⚠️ Workspace path does not exist: {workspace_path}")
        return

    sys.path.insert(0, str(workspace_path))

    for item in workspace_path.iterdir():
        if item.is_dir():
            router_file = item / "router.py"
            if router_file.exists():
                try:
                    module_name = f"workspace.{item.name}.router"
                    spec = importlib.util.spec_from_file_location(
                        module_name, router_file
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "router"):
                        logger.info(
                            f"🔌 [PLUGIN] Including router from workspace/{item.name}"
                        )
                        # Include with prefix or use the router's own prefix
                        app.include_router(module.router)
                except Exception as e:
                    logger.error(
                        f"❌ [PLUGIN] Failed to load workspace/{item.name}: {e}"
                    )


discover_plugins()


# ==================== ORCHESTRATOR BRAIN ====================


class TaskRequest(BaseModel):
    task: str


class ToolRequest(BaseModel):
    name: str
    description: str
    code: str
    schema: Optional[dict] = None
    category: str = "backend"


class InstructionsRequest(BaseModel):
    instructions: List[dict]


# Import ADK orchestrator

orchestrator = ADKOrchestrator(workspace_root=BASE_DIR / "..")


# Initialize orchestrator on startup
@app.on_event("startup")
async def startup_event():
    await orchestrator.initialize()
    logger.info("ADK Orchestrator initialized")


# Event broadcaster for orchestrator
async def ui_callback(event_type: str, data: Any):
    await manager.broadcast({"type": event_type, "data": data})


orchestrator.status_callback = lambda d: asyncio.create_task(ui_callback("status", d))
orchestrator.thought_callback = lambda t: asyncio.create_task(ui_callback("thought", t))
orchestrator.action_callback = lambda a: asyncio.create_task(ui_callback("action", a))


# ==================== HEALTH & STATUS ====================


@app.get("/")
async def get_ui():
    index_path = UI_DIR / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(
        content="<h1>IMMUTABLE CORE API</h1><p>UI directory not found.</p>"
    )


@app.get("/health")
async def health():
    return {
        "success": True,
        "data": {"status": "healthy", "project": "IMMUTABLE CORE"},
        "error": None,
    }


@app.get("/api/status")
async def get_status():
    """Get current orchestrator brain status."""
    try:
        status = await orchestrator.get_status()
        return {"success": True, "data": status, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ==================== MISSION EXECUTION ====================


@app.post("/task/start")
async def start_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Start a new mission/task via ADK."""
    if orchestrator.task_active:
        return {"success": False, "data": None, "error": "A task is already running"}

    # Emit status start
    await ui_callback(
        "running",
        {
            "task": request.task,
        },
    )

    # Run mission in background
    background_tasks.add_task(orchestrator.start_mission, request.task)

    return {
        "success": True,
        "data": {"message": "Mission started via ADK"},
        "error": None,
    }


@app.post("/task/stop")
async def stop_task():
    """Stop the current task."""
    orchestrator.task_active = False
    return {
        "success": True,
        "data": {"message": "Task stopping requested"},
        "error": None,
    }


# ==================== TOOL MANAGEMENT ====================


@app.get("/api/tools")
async def list_tools(category: Optional[str] = Query(None)):
    """List all registered tools."""
    try:
        tools = await orchestrator.list_tools(category)
        return {"success": True, "data": {"tools": tools}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.post("/api/tools/register")
async def register_tool(request: ToolRequest):
    """Register a new tool."""
    try:
        result = await orchestrator.register_tool(
            name=request.name,
            description=request.description,
            code=request.code,
            schema=request.schema,
            category=request.category,
        )
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.post("/api/tools/hot-load")
async def hot_load_tool(name: str):
    """Hot-load a tool without restarting."""
    try:
        result = await orchestrator.hot_load_tool(name)
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.delete("/api/tools/remove")
async def remove_tool(name: str):
    """Remove a tool."""
    try:
        result = await orchestrator.remove_tool(name)
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ==================== AGENT INSTRUCTIONS ====================


@app.post("/api/instructions/load")
async def load_instructions(request: InstructionsRequest):
    """Load agent instructions."""
    try:
        await orchestrator.load_agent_instructions(request.instructions)
        return {
            "success": True,
            "data": {
                "message": f"Loaded {len(request.instructions)} agent instructions",
                "count": len(request.instructions),
            },
            "error": None,
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.get("/api/instructions")
async def get_instructions():
    """Get loaded agent instructions."""
    try:
        return {
            "success": True,
            "data": {
                "instructions": orchestrator.agent_instructions,
                "count": len(orchestrator.agent_instructions),
            },
            "error": None,
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ==================== AUTO-ADAPTATION ====================


@app.post("/api/adaptation/self-improve")
async def run_self_improvement():
    """Run the self-improvement loop."""
    try:
        result = await orchestrator.run_self_improvement_loop()
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.get("/api/adaptation/stats")
async def get_adaptation_stats():
    """Get auto-adaptation statistics."""
    try:
        stats = orchestrator.auto_adaptation.get_adaptation_stats()
        return {"success": True, "data": stats, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.get("/api/adaptation/modules")
async def list_modules():
    """List all loaded modules."""
    try:
        modules = orchestrator.auto_adaptation.get_all_modules()
        return {"success": True, "data": {"modules": modules}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.post("/api/adaptation/test-module")
async def test_module(name: str, category: str):
    """Test a specific module."""
    try:
        result = await orchestrator.auto_adaptation.test_module(name, category)
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.post("/api/adaptation/fix-module")
async def fix_module(name: str, category: str):
    """Attempt to auto-fix a module."""
    try:
        result = await orchestrator.auto_adaptation.run_auto_fix(name, category)
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ==================== ADAPTATION LOG ====================


@app.get("/api/adaptation/log")
async def get_adaptation_log():
    """Get adaptation log."""
    try:
        log_path = orchestrator.workspace_root / ".agents" / "adaptation_log.json"

        if log_path.exists():
            import json

            with open(log_path, "r") as f:
                log = json.load(f)

            return {"success": True, "data": {"log": log}, "error": None}
        else:
            return {"success": True, "data": {"log": []}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ==================== WEBSOCKET ENDPOINT ====================


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time status updates."""
    await manager.connect(websocket)

    try:
        # Send initial status
        status = await orchestrator.get_status()
        await manager.send_personal(
            websocket,
            {
                "type": "connected",
                "data": {
                    "tools_count": status["tools_count"],
                    "agent_instructions_count": status["agent_instructions_count"],
                },
            },
        )

        # Listen for messages from frontend
        while True:
            try:
                data = await websocket.receive_json()

                # Handle incoming messages from frontend
                msg_type = data.get("type")

                if msg_type == "status":
                    state = data.get("state", "unknown")
                    await orchestrator._emit_status(state, data.get("data", {}))
                elif msg_type == "thought":
                    thought = data.get("content", "")
                    await orchestrator._emit_thought(thought)
                elif msg_type == "action":
                    action = data.get("action", {})
                    await orchestrator._emit_action(action)

            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket disconnected")


# ==================== DASHBOARD ROUTER ====================

from modules.dashboard_router import router as dashboard_router

app.include_router(dashboard_router)


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn

    # Initialize app.state before running
    app.state.dashboard_status = "idle"
    app.state.dashboard_active_task = None
    app.state.dashboard_metrics = {"tokens": 0}
    app.state.connection_manager = manager

    uvicorn.run(app, host="0.0.0.0", port=8000)
