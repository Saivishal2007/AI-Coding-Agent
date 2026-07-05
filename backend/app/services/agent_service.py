from uuid import uuid4

from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import AgentRequest, AgentResponse
from app.utils.exceptions import ValidationAppError
from app.utils.helpers import compact_whitespace

logger = get_logger(__name__)


class AgentService:
    async def run(self, request: AgentRequest) -> AgentResponse:
        prompt = compact_whitespace(request.prompt)
        if not prompt:
            raise ValidationAppError("Prompt cannot be empty.")

        session_id = request.session_id or uuid4()
        logger.info("Processing agent request for session %s", session_id)

        output = self._build_response(prompt)
        return AgentResponse(
            session_id=session_id,
            status="completed",
            output=output,
            metadata={
                "engine": "local-placeholder",
                "timeout_seconds": str(settings.AGENT_TIMEOUT_SECONDS),
            },
        )

    def _build_response(self, prompt: str) -> str:
        return (
            "Agent service is running. "
            "Connect your model/provider implementation in AgentService._build_response. "
            f"Received prompt: {prompt}"
        )
