from pathlib import Path


IGNORE_DIRS = {
    ".venv",
    "__pycache__",
    ".git",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
}


def should_ignore(path: Path) -> bool:
    return any(
        part in IGNORE_DIRS
        for part in path.parts
    )