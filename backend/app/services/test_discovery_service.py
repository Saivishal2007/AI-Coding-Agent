from pathlib import Path

from app.schemas.test_discovery import (
    TestDiscovery,
    TestFramework,
)


class TestDiscoveryService:

    def discover(
        self,
        project_path: str,
    ) -> TestDiscovery:

        project = Path(project_path)

        discovery = TestDiscovery()

        self._detect_pytest(project, discovery)
        self._detect_unittest(project, discovery)
        self._detect_jest(project, discovery)
        self._detect_mocha(project, discovery)
        self._detect_junit(project, discovery)
        self._detect_go_test(project, discovery)
        self._detect_cargo_test(project, discovery)

        return discovery

    def _add(
        self,
        discovery: TestDiscovery,
        name: str,
        detected_by: str,
    ) -> None:

        discovery.frameworks.append(
            TestFramework(
                name=name,
                detected_by=detected_by,
            )
        )

    def _detect_pytest(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        if (project / "pytest.ini").exists():
            self._add(discovery, "pytest", "pytest.ini")

    def _detect_unittest(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        if any(project.rglob("test_*.py")):
            self._add(discovery, "unittest", "test_*.py")

    def _detect_jest(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        package = project / "package.json"

        if package.exists():

            text = package.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            if "jest" in text.lower():
                self._add(discovery, "Jest", "package.json")

    def _detect_mocha(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        package = project / "package.json"

        if package.exists():

            text = package.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            if "mocha" in text.lower():
                self._add(discovery, "Mocha", "package.json")

    def _detect_junit(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        if (project / "pom.xml").exists():
            self._add(discovery, "JUnit", "pom.xml")

    def _detect_go_test(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        if (project / "go.mod").exists():
            self._add(discovery, "Go Test", "go.mod")

    def _detect_cargo_test(
        self,
        project: Path,
        discovery: TestDiscovery,
    ) -> None:

        if (project / "Cargo.toml").exists():
            self._add(discovery, "Cargo Test", "Cargo.toml")