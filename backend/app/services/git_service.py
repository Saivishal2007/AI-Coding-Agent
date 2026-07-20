import subprocess
from pathlib import Path

from app.schemas.git_info import GitInfo


class GitService:

    def get_info(
        self,
        project_path: str,
    ) -> GitInfo:

        project = Path(project_path)

        if not (project / ".git").exists():
            return GitInfo()

        info = GitInfo(
            git_enabled=True,
        )

        info.current_branch = self._run(
            project,
            [
                "git",
                "branch",
                "--show-current",
            ],
        )

        info.modified_files = self._run_lines(
            project,
            [
                "git",
                "diff",
                "--name-only",
            ],
        )

        info.staged_files = self._run_lines(
            project,
            [
                "git",
                "diff",
                "--cached",
                "--name-only",
            ],
        )

        info.recent_commits = self._run_lines(
            project,
            [
                "git",
                "log",
                "--oneline",
                "-5",
            ],
        )

        return info

    def _run(
        self,
        cwd: Path,
        command: list[str],
    ) -> str | None:

        try:

            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
            )

            return result.stdout.strip() or None

        except Exception:

            return None

    def _run_lines(
        self,
        cwd: Path,
        command: list[str],
    ) -> list[str]:

        output = self._run(
            cwd,
            command,
        )

        if not output:
            return []

        return [
            line
            for line in output.splitlines()
            if line.strip()
        ]