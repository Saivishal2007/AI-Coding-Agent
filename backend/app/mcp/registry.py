from typing import Callable


class MCPRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, name: str, handler: Callable):
        self._tools[name] = handler

    def get(self, name: str):
        return self._tools.get(name)

    def list_tools(self):
        return list(self._tools.keys())


registry = MCPRegistry()