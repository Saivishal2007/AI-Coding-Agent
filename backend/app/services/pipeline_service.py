from app.models.schemas import AgentRequest


class PipelineService:
    """
    Coordinates the complete AI coding workflow.

    This service orchestrates the existing components
    without implementing their internal logic.
    """

    def __init__(self, agent_service):
        self.agent = agent_service

    async def execute(self, request: AgentRequest):
        return await self.agent.run_pipeline(request)