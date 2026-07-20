from pathlib import Path

from app.intelligence.repository_intelligence_service import (
    RepositoryIntelligenceService,
)


class ProjectAnalyzerService:

    def __init__(self, project_root: str):

        self.root = Path(project_root)

    def analyze(self) -> dict:

        knowledge = (
            RepositoryIntelligenceService(
                str(self.root)
            ).build()
        )

        files = {
            p.name.lower()
            for p in self.root.rglob("*")
            if p.is_file()
        }

        frameworks = []

        if "requirements.txt" in files:

            content = (
                self.root / "requirements.txt"
            ).read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if "fastapi" in content:
                frameworks.append("FastAPI")

            if "flask" in content:
                frameworks.append("Flask")

            if "django" in content:
                frameworks.append("Django")

        if "package.json" in files:

            frameworks.append("Node.js")

        resolved_root = self.root.resolve()

        return {
            "project_name": resolved_root.name,
            "frameworks": frameworks,
            "total_files": len(knowledge.files),
            "total_functions": len(knowledge.functions),
            "total_classes": len(knowledge.classes),
            "total_routes": len(knowledge.routes),
            "languages": sorted(
                {
                    f["language"]
                    for f in knowledge.files
                }
            ),
        }