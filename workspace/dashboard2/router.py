from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Dashboard API", version="1.0.0")


class DashboardData(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Welcome to Dashboard 2"}


@app.get("/dashboard/data")
async def get_dashboard_data() -> DashboardData:
    """Returns dashboard data."""
    return DashboardData(title="Dashboard", content="This is the main dashboard view.")


@app.post("/dashboard/update")
async def update_dashboard(data: DashboardData):
    """Updates dashboard with new data."""
    if not data.title or not data.content:
        raise HTTPException(status_code=400, detail="Title and content are required.")
    return {"status": "success", "message": f"Updated {data.title}"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
