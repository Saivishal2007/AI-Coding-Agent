from pathlib import Path

from app.schemas.workspace import (
    Workspace,
    WorkspaceFolder,
)


class WorkspaceService:

    def scan_workspace(
        self,
        project_path: str,
    ) -> Workspace:

        root = Path(project_path)

        workspace = Workspace(
            root=str(root)
        )

        for item in root.iterdir():

            if not item.is_dir():
                continue

            if item.name.startswith("."):
                continue

            workspace.folders.append(
                WorkspaceFolder(
                    name=item.name,
                    path=str(item),
                )
            )

        return workspace