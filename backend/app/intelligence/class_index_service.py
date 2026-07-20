import ast
from pathlib import Path
from app.intelligence.intelligence_utils import should_ignore
from app.core.logging import get_logger

logger = get_logger(__name__)


class ClassIndexService:
    """
    Build an index of all Python classes.
    """

    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def build_index(self) -> list[dict]:

        logger.info("Building class index...")

        classes = []

        for file in self.root.rglob("*.py"):
            if should_ignore(file):
                continue
            try:
                tree = ast.parse(
                    file.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )

            except Exception:
                continue

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    bases = []

                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            bases.append(base.id)
                        elif isinstance(base, ast.Attribute):
                            bases.append(base.attr)

                    classes.append(
                        {
                            "name": node.name,
                            "file": str(
                                file.relative_to(self.root)
                            ),
                            "line": node.lineno,
                            "base_classes": bases,
                        }
                    )

        logger.info(
            "Indexed %d classes.",
            len(classes),
        )

        return classes