import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    MCP Client for communicating with the local MCP server.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parents[3]

        server_file = (
            project_root
            / "mcp-server"
            / "main.py"
        )

        self.server_params = StdioServerParameters(
            command="python",
            args=[str(server_file)],
        )

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        async with stdio_client(self.server_params) as (
            read_stream,
            write_stream,
        ):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments=arguments,
                )

                if result.isError:
                    raise RuntimeError(
                        result.content[0].text
                    )

                if result.content:

                    text = result.content[0].text

                    try:
                        return json.loads(text)

                    except Exception:
                        return text

                return None