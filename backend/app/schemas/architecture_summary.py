from pydantic import BaseModel


class ArchitectureSummary(BaseModel):
    languages: list[str] = []

    frameworks: list[str] = []

    workspace_folders: list[str] = []

    total_symbols: int = 0

    total_dependencies: int = 0

    test_frameworks: list[str] = []

    git_enabled: bool = False