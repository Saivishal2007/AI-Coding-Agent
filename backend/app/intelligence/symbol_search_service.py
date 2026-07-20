from app.intelligence.repository_knowledge import RepositoryKnowledge


class SymbolSearchService:
    """
    Search for symbols in the repository knowledge.
    """

    def __init__(self, knowledge: RepositoryKnowledge):
        self.knowledge = knowledge

    def search(self, query: str) -> dict:

        query = query.lower()

        results = {
            "files": [],
            "functions": [],
            "classes": [],
            "routes": [],
        }

        for file in self.knowledge.files:

            if query in file["name"].lower():

                results["files"].append(file)

        for function in self.knowledge.functions:

            if query in function["name"].lower():

                results["functions"].append(function)

        for cls in self.knowledge.classes:

            if query in cls["name"].lower():

                results["classes"].append(cls)

        for route in self.knowledge.routes:

            if (
                query in route["function"].lower()
                or query in route["path"].lower()
            ):

                results["routes"].append(route)

        return results