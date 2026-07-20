from pydantic import BaseModel


class WorkspaceFolder(BaseModel):
    name: str
    path: str


class Workspace(BaseModel):
    root: str
    folders: list[WorkspaceFolder] = []