from app.services.file_reader_service import FileReaderService
from app.services.file_editor_service import FileEditorService


def register_editor_tools(mcp):
    """
    Register all editor-related MCP tools.
    """

    @mcp.tool()
    def edit_file(
        project_root: str,
        relative_path: str,
        new_content: str,
    ) -> dict:
        """
        Prepare an edit for an existing file.

        Args:
            project_root: Absolute path to the project root.
            relative_path: Path to the file relative to the project root.
            new_content: The updated file contents.

        Returns:
            Information about the prepared edit.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            if not relative_path:
                raise ValueError("Relative path cannot be empty.")

            reader = FileReaderService(project_root)
            service = FileEditorService(reader)

            return service.prepare_edit(
                relative_path=relative_path,
                new_content=new_content,
            )

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }