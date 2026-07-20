from datetime import datetime

from pydantic import BaseModel, Field


class AgentStep(BaseModel):
    """
    Represents one iteration of the autonomous agent.
    """

    iteration: int

    # Decision made by the ReasoningService
    decision: str = ""

    # Tool selected by the ToolSelectionService
    tool: str = ""

    # Action executed by the ActionProcessor
    action: str = ""

    # Whether the step succeeded
    success: bool = True

    # Human-readable summary
    summary: str = ""

    # Timestamp for debugging/history
    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


class AgentState(BaseModel):
    """
    Stores the complete state of an autonomous task.
    """

    # Original user request
    goal: str

    # Current loop iteration
    current_iteration: int = 0

    # Whether the task has finished
    completed: bool = False

    # History of all agent iterations
    steps: list[AgentStep] = Field(
        default_factory=list
    )

    # Dynamic context updates during execution
    context_updates: list[str] = Field(
        default_factory=list
    )

    # Planner output (optional)
    plan: dict = Field(
        default_factory=dict
    )

    # Additional metadata
    metadata: dict = Field(
        default_factory=dict
    )