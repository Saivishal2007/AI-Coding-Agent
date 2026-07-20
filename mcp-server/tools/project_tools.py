from app.services.project_summary_service import ProjectSummaryService


def register_project_tools(mcp):

    @mcp.tool()
    def project_summary(project_root: str) -> str:
        """
        Generate a summary of a Python project.
        """
        service = ProjectSummaryService(project_root)
        return service.get_summary()