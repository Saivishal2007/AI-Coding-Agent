from app.core.logging import get_logger
from app.services.file_writer_service import FileWriterService
from app.services.pending_edit_service import PendingEditService

logger = get_logger(__name__)


class ApplyEditService:
    """
    Applies approved pending edits.

    Supports:
    - Single-file edits
    - Multi-file edits
    - Status tracking
    - Validation
    """

    def __init__(
        self,
        writer: FileWriterService,
        pending: PendingEditService,
    ):
        self.writer = writer
        self.pending = pending

    def apply(self, edit_id: str):

        if not self.pending.exists(edit_id):
            raise ValueError("Pending edit not found.")

        pending = self.pending.get(edit_id)

        preview = pending["preview"]

        results = []

        # -----------------------------
        # Single File
        # -----------------------------

        if isinstance(preview, dict):

            logger.info(
                "Applying edit to %s",
                preview["path"],
            )

            result = self.writer.write(
                relative_path=preview["path"],
                content=preview["new_content"],
            )

            results.append(result)

        # -----------------------------
        # Multiple Files
        # -----------------------------

        else:

            logger.info(
                "Applying %d file edits",
                len(preview),
            )

            for file in preview:

                result = self.writer.write(
                    relative_path=file["path"],
                    content=file["new_content"],
                )

                results.append(result)

        self.pending.mark_applied(edit_id)

        self.pending.remove(edit_id)

        logger.info(
            "Successfully applied edit %s",
            edit_id,
        )

        return {
            "success": True,
            "files": results,
            "count": len(results),
        }