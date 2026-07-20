from app.schemas.architecture_summary import (
    ArchitectureSummary,
)
from app.services.dependency_graph_service import (
    DependencyGraphService,
)
from app.services.git_service import (
    GitService,
)
from app.services.project_configuration_service import (
    ProjectConfigurationService,
)
from app.services.symbol_index_service import (
    SymbolIndexService,
)
from app.services.test_discovery_service import (
    TestDiscoveryService,
)
from app.services.workspace_service import (
    WorkspaceService,
)


class ArchitectureSummaryService:

    def __init__(self):

        self.configuration_service = ProjectConfigurationService()

        self.workspace_service = WorkspaceService()

        self.symbol_service = SymbolIndexService()

        self.dependency_service = DependencyGraphService()

        self.test_service = TestDiscoveryService()

        self.git_service = GitService()

    def build_summary(
        self,
        project_path: str,
    ) -> ArchitectureSummary:

        configuration = self.configuration_service.scan_project(
            project_path
        )

        workspace = self.workspace_service.scan_workspace(
            project_path
        )

        symbols = self.symbol_service.build_index(
            project_path
        )

        dependencies = self.dependency_service.build_graph(
            project_path
        )

        tests = self.test_service.discover(
            project_path
        )

        git = self.git_service.get_info(
            project_path
        )

        return ArchitectureSummary(

            languages=configuration.languages,

            frameworks=configuration.frameworks,

            workspace_folders=[
                folder.name
                for folder in workspace.folders
            ],

            total_symbols=len(
                symbols.symbols
            ),

            total_dependencies=len(
                dependencies.dependencies
            ),

            test_frameworks=[
                framework.name
                for framework in tests.frameworks
            ],

            git_enabled=git.git_enabled,
        )