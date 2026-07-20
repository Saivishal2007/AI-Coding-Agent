import os
import logging
from pathlib import Path
from typing import List
from app.core.logging import get_logger

logger = get_logger(__name__)


class LoggingService:
    """
    LoggingService manages log generation, structured diagnostic logging,
    and log file retrieval across the workspace.
    """

    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.log_dir = self.root / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "app.log"
        self._setup_file_handler()

    def _setup_file_handler(self):
        """
        Registers a file handler for the root logger if not already present,
        ensuring log outputs are persisted to the log directory.
        """
        root_logger = logging.getLogger()
        
        # Check if file logging is already configured to avoid double writing
        has_file_handler = any(
            isinstance(h, logging.FileHandler) and h.baseFilename == str(self.log_file.resolve())
            for h in root_logger.handlers
        )

        if not has_file_handler:
            try:
                file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
                formatter = logging.Formatter(
                    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
                file_handler.setFormatter(formatter)
                file_handler.setLevel(logging.INFO)
                root_logger.addHandler(file_handler)
                logger.info("File logging handler registered at: %s", self.log_file)
            except Exception as e:
                logger.error("Failed to setup file logging handler: %s", str(e))

    def log_info(self, message: str, module: str = "app"):
        """Logs info messages using the configured module logger name."""
        logging.getLogger(module).info(message)

    def log_warning(self, message: str, module: str = "app"):
        """Logs warning messages using the configured module logger name."""
        logging.getLogger(module).warning(message)

    def log_error(self, message: str, module: str = "app", exc_info: bool = False):
        """Logs error messages with optional stack trace."""
        logging.getLogger(module).error(message, exc_info=exc_info)

    def get_recent_logs(self, limit: int = 100) -> List[str]:
        """
        Retrieves the last N log lines from the log file.
        """
        if not self.log_file.exists():
            logger.warning("Attempted to read non-existent log file: %s", self.log_file)
            return []

        try:
            with open(self.log_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                return [line.strip() for line in lines[-limit:]]
        except Exception as e:
            logger.error("Failed to read log file: %s", str(e))
            return [f"ERROR: Failed to retrieve log history: {str(e)}"]

    def clear_logs(self) -> bool:
        """
        Clears/truncates the log file to free space or reset state.
        """
        if not self.log_file.exists():
            return True

        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.truncate(0)
            logger.info("Application log file cleared successfully.")
            return True
        except Exception as e:
            logger.error("Failed to clear log file: %s", str(e))
            return False
