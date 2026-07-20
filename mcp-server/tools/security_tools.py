from app.services.secret_scanner_service import SecretScannerService
from app.services.vulnerability_scanner_service import (
    VulnerabilityScannerService,
)
from app.services.dependency_security_service import (
    DependencySecurityService,
)
from app.services.security_report_service import (
    SecurityReportService,
)


def register_security_tools(mcp):
    """
    Register all security-related MCP tools.
    """

    @mcp.tool()
    def scan_secrets(
        project_root: str,
    ) -> dict:
        """
        Scan the project for hardcoded secrets and credentials.

        Args:
            project_root: Absolute path to the project root.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            service = SecretScannerService(project_root)
            return service.scan()

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @mcp.tool()
    def scan_vulnerabilities(
        project_root: str,
    ) -> dict:
        """
        Scan the project for insecure coding patterns.

        Args:
            project_root: Absolute path to the project root.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            service = VulnerabilityScannerService(project_root)
            return service.scan()

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @mcp.tool()
    def analyze_dependency_security(
        project_root: str,
    ) -> dict:
        """
        Analyze project dependencies for security risks.

        Args:
            project_root: Absolute path to the project root.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            service = DependencySecurityService(project_root)
            return service.scan()

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @mcp.tool()
    def generate_security_report(
        project_root: str,
    ) -> dict:
        """
        Generate a complete security report for the project.

        Args:
            project_root: Absolute path to the project root.
        """
        try:
            if not project_root:
                raise ValueError("Project root cannot be empty.")

            service = SecurityReportService(project_root)
            return service.generate_report()

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }