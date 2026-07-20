from pydantic import BaseModel


class Dependency(BaseModel):
    source: str
    target: str


class DependencyGraph(BaseModel):
    dependencies: list[Dependency] = []