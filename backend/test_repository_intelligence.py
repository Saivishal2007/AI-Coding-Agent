from app.intelligence.repository_index_service import RepositoryIndexService
from app.intelligence.function_index_service import FunctionIndexService
from app.intelligence.class_index_service import ClassIndexService
from app.intelligence.import_graph_service import ImportGraphService
from app.intelligence.route_index_service import RouteIndexService
from app.intelligence.repository_intelligence_service import RepositoryIntelligenceService
from app.intelligence.symbol_search_service import SymbolSearchService
from app.intelligence.project_analyzer_service import ProjectAnalyzerService


PROJECT_ROOT = "."


def main():

    print("=" * 60)
    print("Repository Index")
    print("=" * 60)

    repo = RepositoryIndexService(PROJECT_ROOT).build_index()
    print(repo["summary"])

    print()

    print("=" * 60)
    print("Function Index")
    print("=" * 60)

    functions = FunctionIndexService(PROJECT_ROOT).build_index()
    print(f"Functions: {len(functions)}")

    print()

    print("=" * 60)
    print("Class Index")
    print("=" * 60)

    classes = ClassIndexService(PROJECT_ROOT).build_index()
    print(f"Classes: {len(classes)}")

    print()

    print("=" * 60)
    print("Import Graph")
    print("=" * 60)

    imports = ImportGraphService(PROJECT_ROOT).build_graph()
    print(f"Files with imports: {len(imports)}")

    print()

    print("=" * 60)
    print("Route Index")
    print("=" * 60)

    routes = RouteIndexService(PROJECT_ROOT).build_index()
    print(f"Routes: {len(routes)}")

    print()

    print("=" * 60)
    print("Repository Intelligence")
    print("=" * 60)

    knowledge = RepositoryIntelligenceService(PROJECT_ROOT).build()

    print("Files:", len(knowledge.files))
    print("Functions:", len(knowledge.functions))
    print("Classes:", len(knowledge.classes))
    print("Routes:", len(knowledge.routes))

    print()

    print("=" * 60)
    print("Symbol Search")
    print("=" * 60)

    search = SymbolSearchService(knowledge)

    result = search.search("service")

    print(result)

    print()

    print("=" * 60)
    print("Project Analyzer")
    print("=" * 60)

    analyzer = ProjectAnalyzerService(PROJECT_ROOT)

    print(analyzer.analyze())


if __name__ == "__main__":
    main()