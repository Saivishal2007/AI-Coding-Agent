from pathlib import Path

from app.core.logging import get_logger

IGNORE_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "node_modules",
}

IGNORE_EXTENSIONS = {
    ".pyc",
    ".pyo",
}

logger = get_logger(__name__)


class RepositoryService:
    """
    Service responsible for scanning a repository
    and collecting basic project information.
    """

    def __init__(self, root_path: str):
        self.root = Path(root_path)

    def scan(self) -> dict:
        logger.info("Starting repository scan at %s", self.root)
        files = []
        python_files = 0
        directories = 0
        total_items_processed = 0

        for item in self.root.rglob("*"):
            total_items_processed += 1
            relative = item.relative_to(self.root)
            relative_str = str(relative)

            if any(part in IGNORE_DIRS for part in relative.parts):
                logger.debug("Ignoring %s (due to ignored directory part)", relative_str)
                continue

            if item.is_dir():
                directories += 1
                logger.debug("Counting directory: %s", relative_str)
                continue

            if item.suffix in IGNORE_EXTENSIONS:
                logger.debug("Ignoring %s (due to ignored extension %s)", relative_str, item.suffix)
                continue

            files.append(relative_str)
            logger.debug("Counting file: %s", relative_str)

            if item.suffix == ".py":
                python_files += 1

        logger.info(
            "Repository scan finished for '%s'. Processed %d items: %d directories, %d Python files, %d total files.",
            self.root.name,
            total_items_processed,
            directories,
            python_files,
            len(files),
        )

        return {
            "root": self.root.name,
            "directories": directories,
            "python_files": python_files,
            "files": files,
        }