from app.models.tool_call import ToolCall
from app.mcp.client import MCPClient


class ToolExecutorService:

    def __init__(self):
        self.client = MCPClient()

    async def execute(self, call: ToolCall):
        """
        Execute a tool through the MCP server.
        """

        return await self.client.call_tool(
            call.tool,
            call.arguments,
        )