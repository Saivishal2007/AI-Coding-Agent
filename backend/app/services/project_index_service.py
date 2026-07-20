from pathlib import Path
from app.services.project_configuration_service import ProjectConfigurationService
from app.services.symbol_index_service import SymbolIndexService
from app.services.cross_reference_service import CrossReferenceService
from app.services.dependency_graph_service import DependencyGraphService
from app.services.workspace_service import WorkspaceService
from app.services.test_discovery_service import TestDiscoveryService
from app.services.project_rules_service import ProjectRulesService
from app.services.git_service import GitService
from app.services.architecture_summary_service import ArchitectureSummaryService
import ast


class ProjectIndexService:
    """
    Builds a lightweight index of the project.

    Stores:
    - Files
    - Classes
    - Functions
    - Imports
    """

    def __init__(self, root: str):

        self.root = Path(root)

        self.index = {}

        self.project_configuration_service = ProjectConfigurationService()

        self.symbol_index_service = SymbolIndexService()

        self.cross_reference_service = CrossReferenceService()

        self.dependency_graph_service = DependencyGraphService()

        self.workspace_service = WorkspaceService()

        self.test_discovery_service = TestDiscoveryService()

        self.project_rules_service = ProjectRulesService()

        self.git_service = GitService()

        self.architecture_summary_service = ArchitectureSummaryService()

    def build(self):

        self.index.clear()

        for file in self.root.rglob("*.py"):

            if any(
                part in {
                    ".git",
                    ".venv",
                    "__pycache__",
                    "node_modules",
                    "dist",
                    "build",
                }
                for part in file.parts
            ):
                continue

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except Exception:

                continue

            relative = str(
                file.relative_to(self.root)
            )

            self.index[relative] = {

                "classes": [],

                "functions": [],

                "imports": []

            }

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    self.index[relative]["classes"].append(
                        node.name
                    )

                elif isinstance(node, ast.FunctionDef):

                    self.index[relative]["functions"].append(
                        node.name
                    )

                elif isinstance(node, ast.Import):

                    for alias in node.names:

                        self.index[relative]["imports"].append(
                            alias.name
                        )

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        self.index[relative]["imports"].append(
                            node.module
                        )

        print(f"Indexed {len(self.index)} Python files.")
        return self.index

    def get_index(self):

        if not self.index:

            self.build()

        return self.index

    def search_symbol(self, symbol: str):

        results = []

        symbol = symbol.lower()

        for file, info in self.get_index().items():

            if any(
                symbol in item.lower()
                for item in info["classes"]
            ):

                results.append(file)

                continue

            if any(
                symbol in item.lower()
                for item in info["functions"]
            ):

                results.append(file)

                continue

            if any(
                symbol in item.lower()
                for item in info["imports"]
            ):

                results.append(file)

        return results

    def summary(self):

        index = self.get_index()

        total_files = len(index)
        total_classes = 0
        total_functions = 0

        services = []
        models = []
        api_files = []

        for file, info in index.items():

            total_classes += len(info["classes"])
            total_functions += len(info["functions"])

            if "services/" in file:
                services.append(file)

            elif "models/" in file:
                models.append(file)

            elif "api/" in file:
                api_files.append(file)

        project_summary = f"""
    Project Statistics
    ------------------
    Python Files : {total_files}
    Classes      : {total_classes}
    Functions    : {total_functions}

    Services
    --------
    {chr(10).join(services)}

    Models
    ------
    {chr(10).join(models)}

    API
    ---
    {chr(10).join(api_files)}
    """

        project_configuration = (
            self.project_configuration_service.scan_project(
                str(self.root)
            )
        )

        symbol_index = (
            self.symbol_index_service.build_index(
                str(self.root)
            )
        )

        cross_references = (
            self.cross_reference_service.build_index(
                str(self.root)
            )
        )

        dependency_graph = (
            self.dependency_graph_service.build_graph(
                str(self.root)
            )
        )

        workspace = (
            self.workspace_service.scan_workspace(
                str(self.root)
            )
        )

        tests = (
            self.test_discovery_service.discover(
                str(self.root)
            )
        )

        project_rules = (
            self.project_rules_service.load_rules(
                str(self.root)
            )
        )

        git_info = (
            self.git_service.get_info(
                str(self.root)
            )
        )

        architecture_summary = (
            self.architecture_summary_service.build_summary(
                str(self.root)
            )
        )

        return {
            "project_summary": project_summary,
            "project_configuration": project_configuration.model_dump(),
            "symbol_index": symbol_index.model_dump(),
            "cross_references": cross_references.model_dump(),
            "dependency_graph": dependency_graph.model_dump(),
            "workspace": workspace.model_dump(),
            "tests": tests.model_dump(),
            "project_rules": project_rules.model_dump(),
            "git": git_info.model_dump(),
            "architecture_summary": architecture_summary.model_dump(),
        }  