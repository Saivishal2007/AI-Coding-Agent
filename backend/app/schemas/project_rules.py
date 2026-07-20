from pydantic import BaseModel


class ProjectRule(BaseModel):
    key: str
    value: str


class ProjectRules(BaseModel):
    rules: list[ProjectRule] = []