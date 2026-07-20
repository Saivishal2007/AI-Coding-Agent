import json
from pathlib import Path

from app.core.logging import get_logger

logger = get_logger(__name__)


class DependencySecurityService:
    """
    Analyze dependency files for common security risks.
    """

    RISKY_PACKAGES = {
        "django": {
            "min_version": "4.2",
            "severity": "High",
            "reason": "Older Django versions may contain known security vulnerabilities.",
            "recommendation": "Upgrade to a supported LTS version.",
        },
        "flask": {
            "min_version": "2.3",
            "severity": "Medium",
            "reason": "Older Flask versions may miss important security fixes.",
            "recommendation": "Upgrade to the latest stable release.",
        },
        "requests": {
            "min_version": "2.31",
            "severity": "Medium",
            "reason": "Older Requests versions may contain security fixes.",
            "recommendation": "Upgrade to the latest stable version.",
        },
        "pyyaml": {
            "min_version": "6.0",
            "severity": "High",
            "reason": "Older PyYAML versions have unsafe loading vulnerabilities.",
            "recommendation": "Upgrade and use yaml.safe_load().",
        },
    }

    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def scan(self) -> list[dict]:

        findings = []

        requirements = self.root / "requirements.txt"
        package_json = self.root / "package.json"

        if requirements.exists():
            findings.extend(
                self._scan_requirements(requirements)
            )

        if package_json.exists():
            findings.extend(
                self._scan_package_json(package_json)
            )

        logger.info(
            "Dependency security scan completed. %d findings.",
            len(findings),
        )

        return findings

    def _scan_requirements(
        self,
        path: Path,
    ) -> list[dict]:

        findings = []

        try:
            lines = path.read_text(
                encoding="utf-8",
                errors="ignore",
            ).splitlines()

        except Exception:
            return findings

        for line in lines:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "==" not in line:

                findings.append(
                    {
                        "package": line,
                        "severity": "Low",
                        "reason": "Dependency version is not pinned.",
                        "recommendation": "Pin dependency versions for reproducible builds.",
                    }
                )
                continue

            package, version = line.split("==", 1)

            package = package.strip().lower()
            version = version.strip()

            if package not in self.RISKY_PACKAGES:
                continue

            info = self.RISKY_PACKAGES[package]

            if version < info["min_version"]:

                findings.append(
                    {
                        "package": package,
                        "version": version,
                        "minimum_safe_version": info["min_version"],
                        "severity": info["severity"],
                        "reason": info["reason"],
                        "recommendation": info["recommendation"],
                    }
                )

        return findings

    def _scan_package_json(
        self,
        path: Path,
    ) -> list[dict]:

        findings = []

        try:

            data = json.loads(
                path.read_text(
                    encoding="utf-8",
                )
            )

        except Exception:
            return findings

        dependencies = {}

        dependencies.update(
            data.get(
                "dependencies",
                {},
            )
        )

        dependencies.update(
            data.get(
                "devDependencies",
                {},
            )
        )

        for package, version in dependencies.items():

            severity = None
            reason = None
            recommendation = None

            if version.startswith("^") or version.startswith("~"):

                severity = "Low"
                reason = "Using floating dependency versions."
                recommendation = (
                    "Pin exact versions for better security and reproducibility."
                )

            elif version in {"latest", "*"}:

                severity = "Medium"
                reason = "Using an unbounded dependency version."
                recommendation = (
                    "Use a fixed version to avoid unexpected updates."
                )

            if severity:

                findings.append(
                    {
                        "package": package,
                        "version": version,
                        "severity": severity,
                        "reason": reason,
                        "recommendation": recommendation,
                    }
                )

        return findings