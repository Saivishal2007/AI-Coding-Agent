from app.services.file_reader_service import FileReaderService
from app.services.file_writer_service import FileWriterService


def register_file_tools(mcp):
    """
    Register all file-related MCP tools.
    """

    @mcp.tool()
    def read_file(
        project_root: str,
        relative_path: str,
    ) -> dict:
        """
        Read the contents of a file from the project.

        Args:
            project_root: Absolute path to the project root.
            relative_path: File path relative to the project root.

        Returns:
            Dictionary containing the file path and contents.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            if not relative_path:
                raise ValueError("Relative path cannot be empty.")

            service = FileReaderService(project_root)

            return service.read(relative_path)

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @mcp.tool()
    def write_file(
        project_root: str,
        relative_path: str,
        content: str,
    ) -> dict:
        """
        Write content to a file inside the project.

        Args:
            project_root: Absolute path to the project root.
            relative_path: File path relative to the project root.
            content: Content to write into the file.

        Returns:
            Dictionary describing the write operation.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            if not relative_path:
                raise ValueError("Relative path cannot be empty.")

            service = FileWriterService(project_root)

            return service.write(
                relative_path=relative_path,
                content=content,
            )

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }