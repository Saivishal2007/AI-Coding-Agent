import re
from pathlib import Path

from app.core.logging import get_logger

logger = get_logger(__name__)


class SecretScannerService:
    """
    Scan a project for hardcoded secrets and credentials.
    """

    IGNORE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".idea",
        ".vscode",
        "node_modules",
        "dist",
        "build",
        ".ai_backups",
    }

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".json",
        ".yaml",
        ".yml",
        ".env",
        ".ini",
        ".cfg",
        ".toml",
    }

    PLACEHOLDER_VALUES = {
        "password",
        "changeme",
        "example",
        "your_api_key",
        "your_secret",
        "secret",
        "token",
        "test",
        "dummy",
        "xxxxx",
    }

    SECRET_PATTERNS = {
        "Hardcoded Password": re.compile(
            r'password\s*=\s*["\'](.+?)["\']',
            re.IGNORECASE,
        ),
        "API Key": re.compile(
            r'api[_-]?key\s*=\s*["\'](.+?)["\']',
            re.IGNORECASE,
        ),
        "Secret Key": re.compile(
            r'secret[_-]?key\s*=\s*["\'](.+?)["\']',
            re.IGNORECASE,
        ),
        "Access Token": re.compile(
            r'token\s*=\s*["\'](.+?)["\']',
            re.IGNORECASE,
        ),
        "AWS Access Key": re.compile(
            r'(AKIA[0-9A-Z]{16})'
        ),
        "Private Key": re.compile(
            r'-----BEGIN .* PRIVATE KEY-----'
        ),
    }

    SEVERITY = {
        "Private Key": "Critical",
        "AWS Access Key": "Critical",
        "API Key": "High",
        "Secret Key": "High",
        "Access Token": "High",
        "Hardcoded Password": "Medium",
    }

    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def _mask_line(self, line: str) -> str:
        if "=" in line:
            key, _ = line.split("=", 1)
            return f"{key.strip()} = ********"
        return "********"

    def scan(self) -> list[dict]:

        findings = []

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            relative = file.relative_to(self.root)

            if any(part in self.IGNORE_DIRS for part in relative.parts):
                continue

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:
                continue

            for line_number, line in enumerate(
                content.splitlines(),
                start=1,
            ):

                for secret_type, pattern in self.SECRET_PATTERNS.items():

                    match = pattern.search(line)

                    if not match:
                        continue

                    if match.lastindex:

                        value = match.group(1).strip().lower()

                        if value in self.PLACEHOLDER_VALUES:
                            continue

                    findings.append(
                        {
                            "file": str(relative),
                            "line": line_number,
                            "type": secret_type,
                            "severity": self.SEVERITY.get(
                                secret_type,
                                "High",
                            ),
                            "preview": self._mask_line(line),
                        }
                    )

        logger.info(
            "Secret scan completed. %d findings.",
            len(findings),
        )

        return findings