from pathlib import Path

from app.core.logging import get_logger
from app.intelligence.intelligence_utils import should_ignore

logger = get_logger(__name__)


class RepositoryIndexService:
    """
    Build a lightweight index of the repository.
    """

    SUPPORTED_EXTENSIONS = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "React",
        ".tsx": "React TypeScript",
        ".json": "JSON",
        ".md": "Markdown",
        ".yml": "YAML",
        ".yaml": "YAML",
        ".toml": "TOML",
    }

    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def build_index(self) -> dict:

        logger.info("Building repository index...")

        files = []
        total_size = 0

        for path in self.root.rglob("*"):

            if should_ignore(path):
                continue

            if not path.is_file():
                continue

            extension = path.suffix.lower()

            # Ignore unsupported file types
            if extension not in self.SUPPORTED_EXTENSIONS:
                continue

            language = self.SUPPORTED_EXTENSIONS[extension]

            size = path.stat().st_size
            total_size += size

            files.append(
                {
                    "path": str(path.relative_to(self.root)),
                    "name": path.name,
                    "extension": extension,
                    "language": language,
                    "size": size,
                }
            )

        logger.info("Indexed %d files.", len(files))

        return {
            "summary": {
                "total_files": len(files),
                "total_size": total_size,
            },
            "files": files,
        }