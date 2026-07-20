from app.core.logging import get_logger
from app.services.file_reader_service import FileReaderService
from app.services.diff_service import DiffService

logger = get_logger(__name__)


class FileEditorService:

    def __init__(self, reader: FileReaderService):

        self.reader = reader

        self.diff = DiffService()

    def prepare_edit(
        self,
        relative_path: str,
        new_content: str,
    ) -> dict:

        logger.info(
            "Preparing edit for %s",
            relative_path,
        )

        current = self.reader.read(
            relative_path
        )

        old_content = current["content"]

        if old_content == new_content:

            logger.info(
                "No changes detected."
            )

            return {
                "path": relative_path,
                "old_content": old_content,
                "new_content": new_content,
                "diff": "",
                "changed": False,
            }

        diff = self.diff.generate(
            old_content,
            new_content,
        )

        logger.info(
            "Diff generated successfully."
        )

        return {
            "path": relative_path,
            "old_content": old_content,
            "new_content": new_content,
            "diff": diff,
            "changed": True,
        }