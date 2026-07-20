from pathlib import Path
import sys

# Add backend to Python path
BACKEND_ROOT = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from mcp.server.fastmcp import FastMCP

from tools.project_tools import register_project_tools
from tools.repository_tools import register_repository_tools
from tools.file_tools import register_file_tools
from tools.editor_tools import register_editor_tools
from tools.dependency_tools import register_dependency_tools
from tools.security_tools import register_security_tools
# from tools.review_tools import register_review_tools


mcp = FastMCP("AI Coding Agent MCP")


# -----------------------------
# Core Project Tools
# -----------------------------
register_project_tools(mcp)
register_repository_tools(mcp)
register_file_tools(mcp)
register_editor_tools(mcp)
register_dependency_tools(mcp)

# -----------------------------
# Security Tools
# -----------------------------
register_security_tools(mcp)

# -----------------------------
# AI Tools (Enable later)
# -----------------------------
# register_review_tools(mcp)

print("Starting MCP Server...")

if __name__ == "__main__":
    mcp.run()