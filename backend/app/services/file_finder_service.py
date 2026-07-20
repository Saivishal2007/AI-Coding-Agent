from pathlib import Path

from app.core.logging import get_logger

logger = get_logger(__name__)


class FileFinderService:
    """
    Finds files inside the repository using
    filename matching.
    """

    def __init__(self, root_path: str):
        self.root = Path(root_path)

    def find(self, filename: str) -> str | None:

        logger.info("Searching for %s", filename)

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            if file.name.lower() == filename.lower():
                return str(file.relative_to(self.root))

        return None