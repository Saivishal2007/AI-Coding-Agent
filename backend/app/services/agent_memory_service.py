from app.core.logging import get_logger
from app.models.agent_state import AgentState

logger = get_logger(__name__)


class AgentMemoryService:
    """
    Stores the execution state of active AI tasks.

    This is in-memory for Version 1.0.
    Later it can be replaced with Redis or a database.
    """

    def __init__(self):

        self._memory: dict[str, AgentState] = {}

    def create(
        self,
        task_id: str,
        goal: str,
    ) -> AgentState:

        state = AgentState(
            goal=goal,
        )

        self._memory[task_id] = state

        logger.info(
            "Created agent state: %s",
            task_id,
        )

        return state

    def get(
        self,
        task_id: str,
    ) -> AgentState | None:

        return self._memory.get(task_id)

    def update(
        self,
        task_id: str,
        state: AgentState,
    ) -> None:

        self._memory[task_id] = state

        logger.info(
            "Updated agent state: %s",
            task_id,
        )

    def remove(
        self,
        task_id: str,
    ) -> None:

        if task_id in self._memory:

            del self._memory[task_id]

            logger.info(
                "Removed agent state: %s",
                task_id,
            )

    def exists(
        self,
        task_id: str,
    ) -> bool:

        return task_id in self._memory

    def clear(self) -> None:

        self._memory.clear()

        logger.info(
            "Cleared all agent states."
        )

    def active_tasks(self) -> list[str]:

        return list(
            self._memory.keys()
        )