from typing import Annotated

from fastapi import Depends

from app.services.agent_service import AgentService


def get_agent_service() -> AgentService:
    return AgentService()


AgentServiceDep = Annotated[AgentService, Depends(get_agent_service)]
