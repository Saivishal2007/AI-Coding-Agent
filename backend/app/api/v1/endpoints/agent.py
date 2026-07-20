from fastapi import APIRouter

from app.api.deps import AgentServiceDep
from app.models.schemas import (
    AgentRequest,
    AgentResponse,
    ApplyEditRequest,
)

router = APIRouter()

@router.post("/run", response_model=AgentResponse)
async def run_agent(
    payload: AgentRequest,
    agent_service: AgentServiceDep,
) -> AgentResponse:

    return await agent_service.run(payload)


@router.post("/apply")
async def apply_edit(
    payload: ApplyEditRequest,
    agent_service: AgentServiceDep,
):

    return agent_service.apply_edit(payload.edit_id)