from app.core.logging import get_logger
from app.services.secret_scanner_service import SecretScannerService
from app.services.vulnerability_scanner_service import (
    VulnerabilityScannerService,
)
from app.services.dependency_security_service import (
    DependencySecurityService,
)

logger = get_logger(__name__)


class SecurityReportService:
    """
    Generate a complete security report for a project.
    """

    def __init__(self, project_root: str):

        self.project_root = project_root

        self.secret_scanner = SecretScannerService(
            project_root
        )

        self.vulnerability_scanner = (
            VulnerabilityScannerService(
                project_root
            )
        )

        self.dependency_scanner = (
            DependencySecurityService(
                project_root
            )
        )

    def generate_report(self) -> dict:

        logger.info(
            "Generating security report..."
        )

        secrets = self.secret_scanner.scan()

        vulnerabilities = (
            self.vulnerability_scanner.scan()
        )

        dependency_risks = (
            self.dependency_scanner.scan()
        )

        summary = self._build_summary(
            secrets,
            vulnerabilities,
            dependency_risks,
        )

        logger.info(
            "Security report generated."
        )

        return {
            "summary": summary,
            "secrets": secrets,
            "vulnerabilities": vulnerabilities,
            "dependency_risks": dependency_risks,
        }

    def _build_summary(
        self,
        secrets,
        vulnerabilities,
        dependency_risks,
    ):

        all_findings = (
            secrets
            + vulnerabilities
            + dependency_risks
        )

        severity_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
        }

        recommendations = set()

        for item in all_findings:

            severity = item.get("severity", "Low")

            if severity in severity_counts:
                severity_counts[severity] += 1

            recommendation = item.get(
                "recommendation"
            )

            if recommendation:
                recommendations.add(
                    recommendation
                )

        total = len(all_findings)

        score = 100

        score -= severity_counts["Critical"] * 20
        score -= severity_counts["High"] * 10
        score -= severity_counts["Medium"] * 5
        score -= severity_counts["Low"] * 2

        score = max(score, 0)

        if score >= 90:
            risk = "Low"
        elif score >= 70:
            risk = "Moderate"
        elif score >= 40:
            risk = "High"
        else:
            risk = "Critical"

        return {
            "critical": severity_counts["Critical"],
            "high": severity_counts["High"],
            "medium": severity_counts["Medium"],
            "low": severity_counts["Low"],
            "total": total,
            "security_score": score,
            "risk_level": risk,
            "recommendations": sorted(
                recommendations
            ),
        }