from app.core.logging import get_logger
from app.models.agent_state import AgentState
from app.services.agent_memory_service import AgentMemoryService

logger = get_logger(__name__)


class TaskRecoveryService:
    """
    Handles recovery of interrupted or failed agent tasks.

    Responsibilities
    ----------------
    - Resume unfinished tasks
    - Retry failed tasks
    - Inspect task state
    """

    def __init__(
        self,
        memory: AgentMemoryService,
    ):

        self.memory = memory

    def recover(
        self,
        task_id: str,
    ) -> AgentState | None:

        logger.info(
            "Recovering task %s",
            task_id,
        )

        state = self.memory.get(task_id)

        if state is None:

            logger.warning(
                "Task %s not found.",
                task_id,
            )

            return None

        if state.completed:

            logger.info(
                "Task already completed."
            )

            return state

        logger.info(
            "Recovered task at iteration %d",
            state.current_iteration,
        )

        return state

    def retry(
        self,
        task_id: str,
    ) -> AgentState | None:

        state = self.memory.get(task_id)

        if state is None:

            return None

        logger.info(
            "Retrying task %s",
            task_id,
        )

        state.completed = False

        return state

    def cancel(
        self,
        task_id: str,
    ) -> bool:

        if not self.memory.exists(task_id):

            return False

        self.memory.remove(task_id)

        logger.info(
            "Cancelled task %s",
            task_id,
        )

        return True

    def status(
        self,
        task_id: str,
    ) -> dict | None:

        state = self.memory.get(task_id)

        if state is None:

            return None

        return {
            "goal": state.goal,
            "iteration": state.current_iteration,
            "completed": state.completed,
            "steps": len(state.steps),
        }

    def active_tasks(self) -> list[str]:

        return self.memory.active_tasks()