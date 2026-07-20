from app.services.dependency_service import DependencyService


def register_dependency_tools(mcp):
    """
    Register all dependency-related MCP tools.
    """

    @mcp.tool()
    def analyze_dependencies(
        project_root: str,
        file_path: str,
    ) -> dict:
        """
        Analyze the dependencies of a file.

        Args:
            project_root: Absolute path to the project root.
            file_path: Path to the file relative to the project root.

        Returns:
            Dependency analysis results.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            if not file_path:
                raise ValueError("File path cannot be empty.")

            service = DependencyService(project_root)

            return service.find_dependencies(
                file_path=file_path,
            )

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }