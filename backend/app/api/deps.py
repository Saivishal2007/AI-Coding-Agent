from typing import Annotated

from fastapi import Depends

from app.services.agent_service import AgentService

agent_service = AgentService()


def get_agent_service():
    return agent_service

AgentServiceDep = Annotated[AgentService, Depends(get_agent_service)]
