import re
from pathlib import Path

from app.core.logging import get_logger

logger = get_logger(__name__)


class DependencyService:
    """
    Finds imported project files.
    """

    IMPORT_PATTERN = re.compile(
        r"from\s+([\w\.]+)\s+import|import\s+([\w\.]+)"
    )

    def __init__(self, root_path: str):
        self.root = Path(root_path)

    def find_dependencies(
        self,
        file_path: str,
    ) -> list[str]:

        path = self.root / file_path

        if not path.exists():
            return []

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception:
            return []

        dependencies = []

        for match in self.IMPORT_PATTERN.finditer(content):

            module = match.group(1) or match.group(2)

            module_path = (
                module.replace(".", "/") + ".py"
            )

            full_path = self.root / module_path

            if full_path.exists():

                dependencies.append(module_path)

        logger.info(
            "Found %d dependencies.",
            len(dependencies),
        )

        return dependencies