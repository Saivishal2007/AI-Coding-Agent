from app.mcp.registry import registry
from app.mcp.models import MCPRequest, MCPResponse


class MCPServer:

    async def execute(self, request: MCPRequest):

        tool = registry.get(request.tool)

        if tool is None:
            return MCPResponse(
                success=False,
                error=f"Unknown tool: {request.tool}"
            )

        try:
            result = await tool(**request.arguments)

            return MCPResponse(
                success=True,
                result=result
            )

        except Exception as e:

            return MCPResponse(
                success=False,
                error=str(e)
            )


mcp_server = MCPServer()