import json
from pathlib import Path

from app.schemas.project_rules import (
    ProjectRule,
    ProjectRules,
)


class ProjectRulesService:

    def load_rules(
        self,
        project_path: str,
    ) -> ProjectRules:

        project = Path(project_path)

        rules = ProjectRules()

        self._load_agent_json(project, rules)
        self._load_editorconfig(project, rules)
        self._load_gitignore(project, rules)

        return rules

    def _add(
        self,
        rules: ProjectRules,
        key: str,
        value: str,
    ) -> None:

        rules.rules.append(
            ProjectRule(
                key=key,
                value=value,
            )
        )

    def _load_agent_json(
        self,
        project: Path,
        rules: ProjectRules,
    ) -> None:

        file = project / "agent.json"

        if not file.exists():
            return

        try:

            data = json.loads(
                file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            )

            for key, value in data.items():

                self._add(
                    rules,
                    key,
                    str(value),
                )

        except Exception:
            pass

    def _load_editorconfig(
        self,
        project: Path,
        rules: ProjectRules,
    ) -> None:

        file = project / ".editorconfig"

        if not file.exists():
            return

        lines = file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()

        for line in lines:

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            self._add(
                rules,
                key.strip(),
                value.strip(),
            )

    def _load_gitignore(
        self,
        project: Path,
        rules: ProjectRules,
    ) -> None:

        file = project / ".gitignore"

        if not file.exists():
            return

        ignored = []

        for line in file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            ignored.append(line)

        self._add(
            rules,
            "gitignore",
            ",".join(ignored),
        )