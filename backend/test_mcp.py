import asyncio

from app.mcp.client import MCPClient


async def main():

    client = MCPClient()

    result = await client.call_tool(
        "read_file",
        {
            "project_root": r"C:\Users\msaiv\Desktop\AI-Coding-Agent\backend",
            "relative_path": "main.py",
        },
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())