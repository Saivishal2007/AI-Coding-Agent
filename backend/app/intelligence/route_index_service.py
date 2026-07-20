import ast
from pathlib import Path

from app.intelligence.intelligence_utils import should_ignore
from app.core.logging import get_logger

logger = get_logger(__name__)


class RouteIndexService:
    """
    Index FastAPI route definitions.
    """

    HTTP_METHODS = {
        "get",
        "post",
        "put",
        "delete",
        "patch",
        "options",
        "head",
    }

    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def build_index(self) -> list[dict]:

        logger.info("Building route index...")

        routes = []

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

                if not isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                ):
                    continue

                for decorator in node.decorator_list:

                    if not isinstance(decorator, ast.Call):
                        continue

                    if not isinstance(decorator.func, ast.Attribute):
                        continue

                    method = decorator.func.attr.lower()

                    if method not in self.HTTP_METHODS:
                        continue

                    path = ""

                    if decorator.args:
                        arg = decorator.args[0]

                        if isinstance(arg, ast.Constant):
                            path = str(arg.value)

                    routes.append(
                        {
                            "method": method.upper(),
                            "path": path,
                            "function": node.name,
                            "file": str(file.relative_to(self.root)),
                            "line": node.lineno,
                            "async": isinstance(node, ast.AsyncFunctionDef),
                        }
                    )

        logger.info(
            "Indexed %d routes.",
            len(routes),
        )

        return routes