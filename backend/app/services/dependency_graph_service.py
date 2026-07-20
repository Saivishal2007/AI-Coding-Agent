from app.schemas.dependency_graph import (
    Dependency,
    DependencyGraph,
)
from app.services.cross_reference_service import (
    CrossReferenceService,
)


class DependencyGraphService:

    def __init__(self):

        self.cross_reference_service = CrossReferenceService()

    def build_graph(
        self,
        project_path: str,
    ) -> DependencyGraph:

        graph = DependencyGraph()

        references = self.cross_reference_service.build_index(
            project_path
        )

        for reference in references.references:

            graph.dependencies.append(
                Dependency(
                    source=reference.source_file,
                    target=reference.imported_module,
                )
            )

        return graph