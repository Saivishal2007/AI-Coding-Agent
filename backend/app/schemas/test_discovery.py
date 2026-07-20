from pydantic import BaseModel


class TestFramework(BaseModel):
    name: str
    detected_by: str


class TestDiscovery(BaseModel):
    frameworks: list[TestFramework] = []