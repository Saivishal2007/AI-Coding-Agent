from pathlib import Path

from app.core.logging import get_logger

logger = get_logger(__name__)


class ProjectSummaryService:

    def __init__(self, root: str):

        self.root = Path(root)

        self.summary = ""

    def build(self) -> str:

        python_files = list(
            self.root.rglob("*.py")
        )

        logger.info(
            "Scanning %d python files...",
            len(python_files)
        )

        services = []
        models = []
        routers = []
        prompts = []

        for file in python_files:

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:

                continue

            name = file.stem

            if name.endswith("_service"):

                services.append(name)

            if name.endswith("_prompt"):

                prompts.append(name)

            if "APIRouter(" in text:

                routers.append(name)

            if "BaseModel" in text:

                models.append(name)

        services = sorted(set(services))
        models = sorted(set(models))
        routers = sorted(set(routers))
        prompts = sorted(set(prompts))

        self.summary = f"""
PROJECT SUMMARY

Python Files : {len(python_files)}

Services ({len(services)})
--------------------------
{chr(10).join(services)}

Models ({len(models)})
----------------------
{chr(10).join(models)}

Routers ({len(routers)})
------------------------
{chr(10).join(routers)}

Prompts ({len(prompts)})
------------------------
{chr(10).join(prompts)}
""".strip()

        logger.info("=" * 60)
        logger.info("PROJECT SUMMARY")
        logger.info("=" * 60)
        logger.info("\n%s", self.summary)
        logger.info("=" * 60)

        return self.summary

    def get_summary(self) -> str:

        if not self.summary:

            self.build()

        return self.summary