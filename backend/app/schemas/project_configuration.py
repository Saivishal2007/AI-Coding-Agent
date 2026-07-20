from pydantic import BaseModel


class ProjectConfiguration(BaseModel):
    languages: list[str] = []
    frameworks: list[str] = []
    package_managers: list[str] = []
    dependencies: list[str] = []

    entry_points: list[str] = []

    test_frameworks: list[str] = []

    config_files: list[str] = []

    build_system: str | None = None

    docker_enabled: bool = False
    git_enabled: bool = False