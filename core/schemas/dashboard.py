from pydantic import BaseModel
from typing import Dict, Any, Optional

class DashboardStats(BaseModel):
    status: str
    active_task: Optional[str] = None
    metrics: Dict[str, Any]
    connections: int
    system_info: Dict[str, str]
