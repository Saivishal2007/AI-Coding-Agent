from pydantic import BaseModel


class PlanStep(BaseModel):

    step: int

    title: str

    description: str


class ExecutionPlan(BaseModel):

    objective: str

    steps: list[PlanStep]