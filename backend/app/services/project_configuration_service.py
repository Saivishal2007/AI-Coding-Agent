from pathlib import Path

from app.schemas.project_configuration import ProjectConfiguration


class ProjectConfigurationService:

    def scan_project(self, project_path: str) -> ProjectConfiguration:

        project = Path(project_path)

        configuration = ProjectConfiguration()

        self._detect_python(project, configuration)
        self._detect_node(project, configuration)
        self._detect_docker(project, configuration)
        self._detect_git(project, configuration)
        self._detect_tests(project, configuration)

        return configuration

    def _detect_python(
        self,
        project: Path,
        configuration: ProjectConfiguration,
    ) -> None:

        requirements = project / "requirements.txt"
        pyproject = project / "pyproject.toml"

        if requirements.exists() or pyproject.exists():

            configuration.languages.append("Python")
            configuration.package_managers.append("pip")

            if requirements.exists():
                configuration.config_files.append("requirements.txt")

                text = requirements.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                configuration.dependencies.extend(
                    [
                        line.strip()
                        for line in text.splitlines()
                        if line.strip()
                    ]
                )

                if "fastapi" in text.lower():
                    configuration.frameworks.append("FastAPI")

                if "django" in text.lower():
                    configuration.frameworks.append("Django")

                if "flask" in text.lower():
                    configuration.frameworks.append("Flask")

    def _detect_node(
        self,
        project: Path,
        configuration: ProjectConfiguration,
    ) -> None:

        package_json = project / "package.json"

        if not package_json.exists():
            return

        configuration.languages.append("JavaScript")
        configuration.package_managers.append("npm")
        configuration.config_files.append("package.json")

    def _detect_docker(
        self,
        project: Path,
        configuration: ProjectConfiguration,
    ) -> None:

        dockerfile = project / "Dockerfile"

        if dockerfile.exists():

            configuration.docker_enabled = True
            configuration.config_files.append("Dockerfile")

    def _detect_git(
        self,
        project: Path,
        configuration: ProjectConfiguration,
    ) -> None:

        git = project / ".git"

        if git.exists():
            configuration.git_enabled = True

    def _detect_tests(
        self,
        project: Path,
        configuration: ProjectConfiguration,
    ) -> None:

        if (project / "pytest.ini").exists():
            configuration.test_frameworks.append("pytest")

        if (project / "tests").exists():
            configuration.entry_points.append("tests/")