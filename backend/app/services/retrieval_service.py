from app.services.repository_service import RepositoryService
from app.services.repository_search_service import RepositorySearchService
from app.services.file_reader_service import FileReaderService
from app.services.dependency_service import DependencyService
from app.services.context_builder import ContextBuilder
from app.services.project_index_service import ProjectIndexService
from app.services.project_summary_service import ProjectSummaryService
from app.core.logging import get_logger


logger = get_logger(__name__)


class RetrievalService:
    """
    Builds repository-aware context for the LLM.
    """

    def __init__(
        self,
        repository: RepositoryService,
        search: RepositorySearchService,
        reader: FileReaderService,
        dependencies: DependencyService,
        context_builder: ContextBuilder,
        project_index: ProjectIndexService,
        project_summary: ProjectSummaryService,
    ):
        self.repository = repository
        self.search = search
        self.reader = reader
        self.dependencies = dependencies
        self.context_builder = context_builder
        self.project_index = project_index
        self.project_summary = project_summary

    def build_context(
        self,
        prompt: str,
        editor_context: dict | None = None,
        conversation: str | None = None,
    ) -> str:

        logger.info("Building retrieval context")

        repository = self.repository.scan()
        repository["summary"] = self.project_summary.get_summary()

        # -----------------------------------
        # Phase 6 Project Intelligence
        # -----------------------------------

        project_intelligence = self.project_index.summary()

        # -----------------------------------
        # Repository Search
        # -----------------------------------

        ranked_results = self.search.search(
            prompt,
            limit=10,
        )

        search_results = []

        for result in ranked_results:

            path = result["path"]

            if path not in search_results:

                search_results.append(path)

        # -----------------------------------
        # Symbol Search
        # -----------------------------------

        symbol_results = self.project_index.search_symbol(
            prompt
        )

        for path in symbol_results:

            if path not in search_results:

                search_results.append(path)

        # -----------------------------------
        # Default File
        # -----------------------------------

        if not search_results:

            search_results = [
                "app/services/agent_service.py"
            ]

        files = []

        visited = set()

        for path in search_results:

            if path in visited:

                continue

            try:

                files.append(
                    self.reader.read(path)
                )

                visited.add(path)

            except Exception:

                continue

            # -----------------------------------
            # Dependencies
            # -----------------------------------

            for dependency in self.dependencies.find_dependencies(path):

                if dependency in visited:

                    continue

                try:

                    files.append(
                        self.reader.read(dependency)
                    )

                    visited.add(dependency)

                except Exception:

                    pass

        return self.context_builder.build(
            user_prompt=prompt,
            repository=repository,
            files=files,
            conversation=conversation,
            workspace=editor_context.get("workspace") if editor_context else None,
            active_file=editor_context.get("active_file") if editor_context else None,
            language=editor_context.get("language") if editor_context else None,
            selected_text=editor_context.get("selected_text") if editor_context else None,
            search_results=ranked_results,
            project_intelligence=project_intelligence,
        )