from pathlib import Path

from app.core.logging import get_logger

logger = get_logger(__name__)


class FileReaderService:
    """
    Reads files safely from the project directory.
    """

    def __init__(self, root_path: str):
        self.root = Path(root_path)

    def read(self, relative_path: str) -> dict:
        file_path = self.root / relative_path

        if not file_path.exists():
            raise FileNotFoundError(f"{relative_path} does not exist.")

        if not file_path.is_file():
            raise ValueError(f"{relative_path} is not a file.")

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        logger.info("Read file %s", relative_path)

        return {
            "path": relative_path,
            "content": content
        }