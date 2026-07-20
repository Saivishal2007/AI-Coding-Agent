import ast
from pathlib import Path

from app.schemas.cross_reference import (
    CrossReference,
    CrossReferenceIndex,
)


class CrossReferenceService:

    def build_index(self, project_path: str) -> CrossReferenceIndex:

        index = CrossReferenceIndex()

        project = Path(project_path)

        for file in project.rglob("*.py"):
            self._scan_file(file, index)

        return index

    def _scan_file(
        self,
        file: Path,
        index: CrossReferenceIndex,
    ) -> None:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        index.references.append(
                            CrossReference(
                                source_file=str(file),
                                imported_module=alias.name,
                            )
                        )

                elif isinstance(node, ast.ImportFrom):

                    module = node.module or ""

                    index.references.append(
                        CrossReference(
                            source_file=str(file),
                            imported_module=module,
                        )
                    )

        except Exception:
            pass