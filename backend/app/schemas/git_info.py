from pydantic import BaseModel


class GitInfo(BaseModel):
    git_enabled: bool = False

    current_branch: str | None = None

    modified_files: list[str] = []

    staged_files: list[str] = []

    recent_commits: list[str] = []