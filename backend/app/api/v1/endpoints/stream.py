from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.api.deps import AgentServiceDep
from app.models.schemas import AgentRequest

router = APIRouter()


@router.post("/stream")
async def stream_agent(
    payload: AgentRequest,
    agent_service: AgentServiceDep,
):

    async def event_generator():

        async for chunk in agent_service.stream(payload):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )