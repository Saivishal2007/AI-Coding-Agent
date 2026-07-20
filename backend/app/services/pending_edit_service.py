from uuid import uuid4
from datetime import datetime
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class PendingEditService:
    """
    Stores pending edit previews until the user approves them.

    Supports:
    - Single file edits
    - Multi-file edits
    - Timestamps
    - Status tracking
    """

    def __init__(self):

        self._pending: dict[str, dict] = {}

    def create(
        self,
        preview: Any,
    ) -> str:

        edit_id = str(uuid4())

        self._pending[edit_id] = {

            "id": edit_id,

            "created_at": datetime.now(),

            "status": "pending",

            "preview": preview,

        }

        logger.info(
            "Created pending edit %s",
            edit_id,
        )

        return edit_id

    def get(
        self,
        edit_id: str,
    ) -> dict | None:

        return self._pending.get(edit_id)

    def exists(
        self,
        edit_id: str,
    ) -> bool:

        return edit_id in self._pending

    def mark_applied(
        self,
        edit_id: str,
    ) -> None:

        if edit_id in self._pending:

            self._pending[edit_id]["status"] = "applied"

            logger.info(
                "Applied pending edit %s",
                edit_id,
            )

    def remove(
        self,
        edit_id: str,
    ) -> None:

        self._pending.pop(
            edit_id,
            None,
        )

        logger.info(
            "Removed pending edit %s",
            edit_id,
        )

    def list_pending(
        self,
    ) -> list[dict]:

        return list(self._pending.values())

    def clear(self) -> None:

        self._pending.clear()

        logger.info("Cleared all pending edits.")