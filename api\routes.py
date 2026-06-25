from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.orchestrator import run_agent

router = APIRouter(prefix="/api/v1", tags=["agents"])


class TaskRequest(BaseModel):
    task: str
    session_id: str = "default"


class TaskResponse(BaseModel):
    task: str
    task_type: str
    answer: str
    success: bool


@router.post("/run", response_model=TaskResponse)
async def run_task(request: TaskRequest):
    """Submit a task to the multi-agent system."""
    try:
        result = run_agent(request.task)
        return TaskResponse(
            task=result["task"],
            task_type=result["task_type"],
            answer=result["answer"],
            success=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    return {"status": "ok", "service": "llm-agent-system"}
