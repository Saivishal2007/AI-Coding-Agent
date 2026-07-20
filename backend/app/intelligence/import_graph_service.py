import ast
from pathlib import Path
from app.intelligence.intelligence_utils import should_ignore
from app.core.logging import get_logger

logger = get_logger(__name__)


class ImportGraphService:
    """
    Build an import graph for the repository.
    """

    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def build_graph(self) -> list[dict]:

        logger.info("Building import graph...")

        graph = []

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

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:
                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    module = node.module or ""

                    imports.append(module)

            graph.append(
                {
                    "file": str(file.relative_to(self.root)),
                    "imports": sorted(set(imports)),
                }
            )

        logger.info(
            "Indexed imports for %d files.",
            len(graph),
        )

        return graph