import ast
from pathlib import Path

from app.schemas.symbol_index import Symbol
from app.schemas.symbol_index import SymbolIndex


class SymbolIndexService:

    def build_index(self, project_path: str) -> SymbolIndex:

        index = SymbolIndex()

        project = Path(project_path)

        for file in project.rglob("*.py"):

            self._index_python_file(file, index)

        return index

    def _index_python_file(
        self,
        file: Path,
        index: SymbolIndex,
    ) -> None:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    index.symbols.append(
                        Symbol(
                            name=node.name,
                            symbol_type="class",
                            file=str(file),
                            line=node.lineno,
                        )
                    )

                elif isinstance(node, ast.FunctionDef):

                    index.symbols.append(
                        Symbol(
                            name=node.name,
                            symbol_type="function",
                            file=str(file),
                            line=node.lineno,
                        )
                    )

                elif isinstance(node, ast.AsyncFunctionDef):

                    index.symbols.append(
                        Symbol(
                            name=node.name,
                            symbol_type="async_function",
                            file=str(file),
                            line=node.lineno,
                        )
                    )

        except Exception:
            pass