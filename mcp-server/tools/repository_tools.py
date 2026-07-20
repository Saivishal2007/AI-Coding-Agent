from app.services.repository_search_service import RepositorySearchService


def register_repository_tools(mcp):
    """
    Register all repository-related MCP tools.
    """

    @mcp.tool()
    def search_repository(
        project_root: str,
        query: str,
        limit: int = 10,
    ) -> list:
        """
        Search the repository for files relevant to a query.

        Args:
            project_root: Absolute path to the project root.
            query: Search query.
            limit: Maximum number of results to return.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            if not query:
                raise ValueError("Query cannot be empty.")

            service = RepositorySearchService(project_root)

            return service.search(
                query=query,
                limit=limit,
            )

        except Exception as e:
            return [
                {
                    "status": "error",
                    "message": str(e),
                }
            ]