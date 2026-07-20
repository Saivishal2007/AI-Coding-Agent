from pathlib import Path
from datetime import datetime
import shutil

from app.core.logging import get_logger

logger = get_logger(__name__)


class FileWriterService:
    """
    Safely writes files into the repository.

    Features:
    - Auto-create directories
    - Backup existing files
    - Prevent unnecessary writes
    """

    def __init__(self, root_path: str):

        self.root = Path(root_path)

        self.backup_dir = self.root / ".ai_backups"

        self.backup_dir.mkdir(
            exist_ok=True,
        )

    def _backup(self, path: Path):

        if not path.exists():
            return None

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_name = (
            f"{path.name}.{timestamp}.bak"
        )

        backup_path = self.backup_dir / backup_name

        shutil.copy2(
            path,
            backup_path,
        )

        logger.info(
            "Backup created: %s",
            backup_name,
        )

        return backup_path

    def write(
        self,
        relative_path: str,
        content: str,
    ) -> dict:

        path = self.root / relative_path

        status = "updated" if path.exists() else "created"

        # -----------------------------
        # Create parent folders
        # -----------------------------

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -----------------------------
        # Backup old file
        # -----------------------------

        backup = self._backup(path)

        # -----------------------------
        # Skip identical writes
        # -----------------------------

        if path.exists():

            old = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            if old == content:

                logger.info(
                    "Skipped identical file: %s",
                    relative_path,
                )

                return {
                    "path": relative_path,
                    "status": "unchanged",
                    "backup": None,
                }

        # -----------------------------
        # Write file
        # -----------------------------

        path.write_text(
            content,
            encoding="utf-8",
        )

        logger.info(
            "%s %s",
            status.capitalize(),
            relative_path,
        )

        return {
            "path": relative_path,
            "status": status,
            "backup": (
                str(backup.relative_to(self.root))
                if backup
                else None
            ),
        }