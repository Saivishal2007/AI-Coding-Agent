from app.intelligence.repository_knowledge import RepositoryKnowledge
from app.intelligence.repository_index_service import RepositoryIndexService
from app.intelligence.function_index_service import FunctionIndexService
from app.intelligence.class_index_service import ClassIndexService
from app.intelligence.import_graph_service import ImportGraphService
from app.intelligence.route_index_service import RouteIndexService

from app.core.logging import get_logger

logger = get_logger(__name__)


class RepositoryIntelligenceService:
    """
    Builds the complete repository knowledge.
    """

    def __init__(self, project_root: str):
        self.project_root = project_root

    def build(self) -> RepositoryKnowledge:

        logger.info("Building repository intelligence...")

        knowledge = RepositoryKnowledge()

        repository_service = RepositoryIndexService(self.project_root)
        repository_data = repository_service.build_index()

        knowledge.summary = repository_data["summary"]
        knowledge.files = repository_data["files"]

        knowledge.functions = (
            FunctionIndexService(self.project_root)
            .build_index()
        )

        knowledge.classes = (
            ClassIndexService(self.project_root)
            .build_index()
        )

        knowledge.imports = (
            ImportGraphService(self.project_root)
            .build_graph()
        )

        knowledge.routes = (
            RouteIndexService(self.project_root)
            .build_index()
        )
        logger.info("Repository intelligence completed.")

        return knowledge