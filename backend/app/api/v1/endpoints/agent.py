from fastapi import APIRouter

from app.api.deps import AgentServiceDep
from app.models.schemas import AgentRequest, AgentResponse

router = APIRouter()


@router.post("/run", response_model=AgentResponse)
async def run_agent(payload: AgentRequest, agent_service: AgentServiceDep) -> AgentResponse:
    return await agent_service.run(payload)
