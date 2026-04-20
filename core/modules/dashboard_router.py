from fastapi import APIRouter, HTTPException, Request
from typing import Any

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_metrics(request: Request) -> dict[str, Any]:
    """Dashboard endpoint returning system metrics."""
    try:
        # Access app state directly from the request object
        app = request.app
        
        # Access state attributes with defaults
        status = getattr(app.state, 'dashboard_status', 'unknown')
        active_task = getattr(app.state, 'dashboard_active_task', None)
        metrics = getattr(app.state, 'dashboard_metrics', {'tokens': 0})
        connection_manager = getattr(app.state, 'connection_manager', None)
        
        # Get active WebSocket connections count
        connections = 0
        if connection_manager and hasattr(connection_manager, 'active_connections'):
            connections = len(connection_manager.active_connections)
        
        return {
            "status": status,
            "active_task": active_task,
            "metrics": metrics,
            "connections": connections
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")