from app.core.logging import get_logger

logger = get_logger(__name__)


class ContextBuilder:
    """
    Builds a rich repository-aware prompt for the LLM.
    """

    def build(
        self,
        user_prompt: str,
        repository: dict,
        files: list[dict],
        workspace: dict | None = None,
        active_file: str | None = None,
        language: str | None = None,
        selected_text: str | None = None,
        conversation: str | None = None,
        search_results: list[dict] | None = None,
        project_intelligence: dict | None = None,
    ) -> str:

        logger.info("Building repository context.")

        context = ""

        # ----------------------------------
        # Conversation
        # ----------------------------------

        if conversation:

            context += f"""
==========================
CONVERSATION HISTORY
==========================

{conversation}

"""

        # ----------------------------------
        # Project Summary
        # ----------------------------------

        context += f"""
==========================
PROJECT SUMMARY
==========================

{repository.get("summary", "")}

==========================
PROJECT INFORMATION
==========================

Repository Root:
{repository["root"]}

Python Files:
{repository["python_files"]}

Directories:
{repository["directories"]}

"""

        # ----------------------------------
        # Project Intelligence
        # ----------------------------------

        if project_intelligence:

            context += f"""
==========================
PROJECT INTELLIGENCE
==========================

{project_intelligence}

"""

        # ----------------------------------
        # Workspace
        # ----------------------------------

        if workspace:

            context += f"""
==========================
WORKSPACE
==========================

Project:
{workspace.get("projectName", "")}

Tree:

{workspace.get("tree", "")}

"""

        # ----------------------------------
        # Active File
        # ----------------------------------

        if active_file:

            context += f"""
==========================
ACTIVE FILE
==========================

{active_file}

Language:
{language}

"""

        # ----------------------------------
        # Selected Text
        # ----------------------------------

        if selected_text:

            context += f"""
==========================
CURRENT SELECTION
==========================

{selected_text}

"""

        # ----------------------------------
        # Search Ranking
        # ----------------------------------

        if search_results:

            context += """
==========================
TOP SEARCH MATCHES
==========================

"""

            for index, result in enumerate(search_results, start=1):

                context += (
                    f"{index}. "
                    f"{result['path']} "
                    f"(Score: {result['score']})\n"
                )

            context += "\n"

        # ----------------------------------
        # Relevant Files
        # ----------------------------------

        context += """
==========================
RELEVANT FILES
==========================

"""

        for file in files:

            context += f"""
FILE:
{file["path"]}

----------------------------------------

{file["content"]}

========================================
"""

        # ----------------------------------
        # User Request
        # ----------------------------------

        context += f"""
==========================
USER REQUEST
==========================

{user_prompt}

"""

        return context