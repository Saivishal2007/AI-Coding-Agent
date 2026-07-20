from pathlib import Path
import ast

from app.core.logging import get_logger

logger = get_logger(__name__)

IGNORE_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "node_modules",
}


class RepositorySearchService:

    def __init__(self, root_path: str):
        self.root = Path(root_path)

    def search(self, query: str, limit: int = 10):

        query = query.lower()

        words = {
            word
            for word in query.split()
            if len(word) > 2
        }

        # -----------------------------
        # Smart Intent Expansion
        # -----------------------------

        intent_map = {

            "authentication": [
                "auth",
                "login",
                "signin",
                "signup",
                "jwt",
                "token",
                "oauth",
                "middleware",
                "user",
            ],

            "login": [
                "auth",
                "signin",
                "jwt",
                "token",
                "user",
            ],

            "database": [
                "database",
                "db",
                "model",
                "models",
                "sql",
                "sqlite",
                "mysql",
                "postgres",
            ],

            "api": [
                "router",
                "route",
                "endpoint",
                "fastapi",
                "controller",
            ],

            "service": [
                "service",
                "manager",
                "provider",
            ],

            "config": [
                "config",
                "settings",
                "env",
            ],

            "edit": [
                "modify",
                "change",
                "rewrite",
                "update",
                "patch",
            ],

            "modify": [
                "edit",
                "rewrite",
                "change",
            ],

            "rewrite": [
                "edit",
                "modify",
                "refactor",
            ],

            "bug": [
                "bug",
                "fix",
                "error",
                "issue",
                "exception",
            ],

            "fix": [
                "bug",
                "repair",
                "correct",
            ],

            "create": [
                "generate",
                "write",
                "new",
                "build",
            ],

            "generate": [
                "create",
                "build",
                "write",
            ],

            "delete": [
                "remove",
                "erase",
            ],

            "remove": [
                "delete",
                "erase",
            ],

            "rename": [
                "move",
                "change",
            ],

            "review": [
                "analyze",
                "inspect",
                "audit",
            ],

            "explain": [
                "describe",
                "architecture",
                "overview",
            ],
        }

        expanded = set(words)

        for word in list(words):

            if word in intent_map:

                expanded.update(intent_map[word])

        logger.info("Repository Search")
        logger.info("----------------------------")
        logger.info("Query: %s", query)
        logger.info("Expanded: %s", sorted(expanded))

        matches = []

        for file in self.root.rglob("*.py"):

            relative = file.relative_to(self.root)

            if any(part in IGNORE_DIRS for part in relative.parts):
                continue

            score = 0

            path = str(relative)

            lower_path = path.lower()

            filename = file.stem.lower()

            # -----------------------------
            # Filename Score
            # -----------------------------

            for word in expanded:

                if filename == word:
                    score += 120

                elif word in filename:
                    score += 80

                elif word in lower_path:
                    score += 40

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:
                continue

            lower_content = content.lower()

            # -----------------------------
            # Content Score
            # -----------------------------

            for word in expanded:

                score += lower_content.count(word) * 2

            # -----------------------------
            # AST Score
            # -----------------------------

            try:

                tree = ast.parse(content)

                for node in ast.walk(tree):

                    if isinstance(node, ast.ClassDef):

                        name = node.name.lower()

                        for word in expanded:

                            if name == word:
                                score += 90

                            elif word in name:
                                score += 45

                    elif isinstance(node, ast.FunctionDef):

                        name = node.name.lower()

                        for word in expanded:

                            if name == word:
                                score += 80

                            elif word in name:
                                score += 40

                    elif isinstance(node, ast.Import):

                        for alias in node.names:

                            module = alias.name.lower()

                            for word in expanded:

                                if word in module:
                                    score += 35

                    elif isinstance(node, ast.ImportFrom):

                        if node.module:

                            module = node.module.lower()

                            for word in expanded:

                                if word in module:
                                    score += 35

            except Exception:

                pass

            # -----------------------------
            # Boost Important Files
            # -----------------------------

            important_files = {

                "agent_service.py": 50,

                "retrieval_service.py": 45,

                "planner_service.py": 40,

                "llm_service.py": 40,

                "action_processing_service.py": 35,

                "action_executor_service.py": 35,

                "repository_search_service.py": 35,

                "context_builder.py": 35,

                "project_summary_service.py": 30,

                "project_index_service.py": 30,

                "main.py": 25,

            }

            filename = file.name.lower()

            if filename in important_files:

                score += important_files[filename]

            if "service" in lower_path:

                score += 10

            if "router" in lower_path:

                score += 10

            if "model" in lower_path:

                score += 10

            if score > 0:

                matches.append({

                    "path": path,

                    "score": score,

                })

        matches.sort(

            key=lambda item: item["score"],

            reverse=True,

        )

        logger.info("Scanned %d files.", len(list(self.root.rglob("*.py"))))
        logger.info("Relevant Matches: %d", len(matches))
        logger.info("Top Matches: %s", matches[:5])

        return matches[:limit]