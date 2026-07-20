from uuid import uuid4

from app.core.logging import get_logger
from app.models.agent_state import AgentStep
from app.services.action_processing_service import (
    ActionProcessingService,
)
from app.services.agent_memory_service import (
    AgentMemoryService,
)
from app.services.retrieval_service import (
    RetrievalService,
)
from app.services.reasoning_service import (
    ReasoningService,
)
from app.services.planner_service import (
    PlannerService,
)
from app.services.replanning_service import (
    ReplanningService,
)
from app.services.tool_selection_service import (
    ToolSelectionService,
)

logger = get_logger(__name__)


class AgentLoopService:
    """
    Executes an autonomous multi-step AI task.

    User
        ↓
    Retrieval
        ↓
    Reasoning
        ↓
    Tool Selection
        ↓
    Planner (optional)
        ↓
    Action Processing
        ↓
    Memory
        ↓
    Repeat
    """

    MAX_ITERATIONS = 10

    def __init__(
        self,
        retrieval: RetrievalService,
        processor: ActionProcessingService,
        memory: AgentMemoryService,
        reasoning: ReasoningService,
        planner: PlannerService,
        replanning: ReplanningService,
        tool_selector: ToolSelectionService,
    ):

        self.retrieval = retrieval
        self.processor = processor
        self.memory = memory
        self.reasoning = reasoning
        self.planner = planner
        self.replanning = replanning
        self.tool_selector = tool_selector

    async def execute(
        self,
        prompt: str,
        editor_context: dict | None = None,
        conversation: str | None = None,
    ):

        task_id = str(uuid4())

        state = self.memory.create(
            task_id,
            prompt,
        )

        current_prompt = prompt

        final_result = None

        logger.info(
            "Starting autonomous task %s",
            task_id,
        )

        for iteration in range(
            1,
            self.MAX_ITERATIONS + 1,
        ):

            logger.info(
                "Iteration %d",
                iteration,
            )

            state.current_iteration = iteration

            # -----------------------------------
            # Build Repository Context
            # -----------------------------------

            context = self.retrieval.build_context(
                current_prompt,
                editor_context,
                conversation,
            )

            # -----------------------------------
            # Reasoning
            # -----------------------------------

            decision = await self.reasoning.decide(
                goal=current_prompt,
                context=context,
                history=[
                    step.model_dump()
                    for step in state.steps
                ],
                latest_result=final_result,
            )

            logger.info(
                "Decision: %s",
                decision.get("decision"),
            )

            if not decision.get(
                "continue",
                True,
            ):
                state.completed = True
                break

            # -----------------------------------
            # Tool Selection
            # -----------------------------------

            tool = await self.tool_selector.choose(
                instruction=current_prompt,
                context=context,
            )

            logger.info(
                "Selected Tool: %s",
                tool.tool,
            )

            # -----------------------------------
            # Planner (Optional)
            # -----------------------------------

            if decision.get("decision", "").lower() == "plan":

                plan = await self.planner.create_plan(
                    goal=current_prompt,
                    context=context,
                )

                state.plan = plan.model_dump()

                logger.info(
                    "Execution plan contains %d steps.",
                    len(plan.steps),
                )

            # ---------- PART 2 STARTS HERE ----------
            # -----------------------------------
            # Execute Action
            # -----------------------------------

            try:

                result = await self.processor.process(
                    context,
                )

            except Exception as e:

                logger.exception(
                    "Iteration %d failed.",
                    iteration,
                )

                recovery = await self.replanning.replan(
                    goal=current_prompt,
                    previous_steps=[
                        step.model_dump()
                        for step in state.steps
                    ],
                    failure_reason=str(e),
                )

                state.steps.append(
                    AgentStep(
                        iteration=iteration,
                        decision=decision.get(
                            "decision",
                            "",
                        ),
                        tool=tool.tool,
                        action="error",
                        success=False,
                        summary=str(e),
                    )
                )

                state.metadata["recovery_plan"] = recovery

                self.memory.update(
                    task_id,
                    state,
                )

                break

            final_result = result

            action = ""

            success = True

            summary = ""

            if isinstance(
                result,
                dict,
            ):

                action = result.get(
                    "action",
                    "",
                )

                summary = str(
                    result.get(
                        "message",
                        result.get(
                            "result",
                            "",
                        ),
                    )
                )
                state.steps.append(
                AgentStep(
                    iteration=iteration,
                    decision=decision.get(
                        "decision",
                        "",
                    ),
                    tool=tool.tool,
                    action=action,
                    success=success,
                    summary=str(summary),
                )
            )

            if (
                state.current_iteration
                >= self.MAX_ITERATIONS
            ):

                logger.warning(
                    "Maximum iterations reached."
                )

                state.completed = True

            self.memory.update(
                task_id,
                state,
            )

            # -----------------------------------
            # Stop Conditions
            # -----------------------------------

            if not isinstance(
                result,
                dict,
            ):

                logger.warning(
                    "Result is not a dictionary. Stopping."
                )

                break

            if action in {

                "respond",

                "complete",

                "finish",

            }:

                logger.info(
                    "Task completed."
                )

                state.completed = True

                break

            if not result.get(
                "continue",
                False,
            ):

                logger.info(
                    "Agent decided to stop."
                )

                break

            current_prompt = (
                "Continue solving the remaining task "
                "using the latest repository state."
            )

        self.memory.update(
            task_id,
            state,
        )

        logger.info(
            "Task %s finished after %d iterations.",
            task_id,
            state.current_iteration,
        )

        return {

            "task_id": task_id,

            "iterations": state.current_iteration,

            "completed": state.completed,

            "history": [

                step.model_dump()

                for step in state.steps

            ],

            "plan": state.plan,

            "result": final_result,

        }