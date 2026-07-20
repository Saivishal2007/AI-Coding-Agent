from app.core.logging import get_logger
from app.models.schemas import AgentAction
from app.services.file_writer_service import FileWriterService
from app.services.file_editor_service import FileEditorService
from app.services.pending_edit_service import PendingEditService
from app.mcp.client import MCPClient

logger = get_logger(__name__)


class ActionExecutorService:
    """
    Executes actions returned by the LLM.
    """

    def __init__(
        self,
        writer: FileWriterService,
        editor: FileEditorService,
        pending: PendingEditService,
    ):
        self.writer = writer
        self.editor = editor
        self.pending = pending
        self.client = MCPClient()

    async def execute(
        self,
        action: AgentAction,
    ) -> dict:

        logger.info(
            "Executing action: %s",
            action.action,
        )

        # -------------------------------------------------
        # Respond
        # -------------------------------------------------

        if action.action == "respond":

            return action.model_dump()

        # -------------------------------------------------
        # Read File (via MCP)
        # -------------------------------------------------

        if action.action == "read_file":

            result = await self.client.call_tool(
                "read_file",
                {
                    "project_root": str(self.writer.root),
                    "relative_path": action.path,
                },
            )

            logger.info(
                "Read file: %s",
                action.path,
            )

            return {
                "success": True,
                "action": "read_file",
                "result": result,
            }

        # -------------------------------------------------
        # Create File (via MCP)
        # -------------------------------------------------

        if action.action == "write_file":

            result = await self.client.call_tool(
                "write_file",
                {
                    "project_root": str(self.writer.root),
                    "relative_path": action.path,
                    "content": action.content,
                },
            )

            logger.info(
                "Created file: %s",
                action.path,
            )

            return {
                "success": True,
                "action": "write_file",
                "result": result,
            }

        # -------------------------------------------------
        # Edit Single File (still local)
        # -------------------------------------------------

        if action.action == "edit_file":

            preview = self.editor.prepare_edit(
                relative_path=action.path,
                new_content=action.content,
            )

            edit_id = self.pending.create(preview)

            logger.info(
                "Prepared edit for %s",
                action.path,
            )

            return {
                "success": True,
                "action": "edit_file",
                "edit_id": edit_id,
                "preview": preview,
                "changed": preview["changed"],
            }

        # -------------------------------------------------
        # Edit Multiple Files (still local)
        # -------------------------------------------------

        if action.action == "edit_files":

            previews = []

            changed = 0

            unchanged = 0

            for file in action.files:

                preview = self.editor.prepare_edit(
                    relative_path=file.path,
                    new_content=file.content,
                )

                previews.append(preview)

                if preview["changed"]:
                    changed += 1
                else:
                    unchanged += 1

            edit_id = self.pending.create(previews)

            logger.info(
                "Prepared %d file edits (%d changed, %d unchanged).",
                len(previews),
                changed,
                unchanged,
            )

            return {
                "success": True,
                "action": "edit_files",
                "edit_id": edit_id,
                "previews": previews,
                "summary": {
                    "total": len(previews),
                    "changed": changed,
                    "unchanged": unchanged,
                },
            }
    
        # -------------------------------------------------
        # Search Repository (via MCP)
        # -------------------------------------------------

        if action.action == "search_repository":

            result = await self.client.call_tool(
                "search_repository",
                {
                    "project_root": str(self.writer.root),
                    "query": action.query,
                    "limit": action.limit,
                },
            )

            logger.info(
                "Repository search: %s",
                action.query,
            )

            return {
                "success": True,
                "action": "search_repository",
                "result": result,
            }
    
        # -------------------------------------------------
        # Scan Secrets (via MCP)
        # -------------------------------------------------

        if action.action == "scan_secrets":

            result = await self.client.call_tool(
                "scan_secrets",
                {
                    "project_root": str(self.writer.root),
                },
            )

            logger.info("Secret scan completed.")

            return {
                "success": True,
                "action": "scan_secrets",
                "result": result,
            }
        
        # -------------------------------------------------
        # Scan Vulnerabilities (via MCP)
        # -------------------------------------------------

        if action.action == "scan_vulnerabilities":

            result = await self.client.call_tool(
                "scan_vulnerabilities",
                {
                    "project_root": str(self.writer.root),
                },
            )

            logger.info("Vulnerability scan completed.")

            return {
                "success": True,
                "action": "scan_vulnerabilities",
                "result": result,
            }
                
        # -------------------------------------------------
        # Analyze Dependency Security (via MCP)
        # -------------------------------------------------

        if action.action == "analyze_dependency_security":

            result = await self.client.call_tool(
                "analyze_dependency_security",
                {
                    "project_root": str(self.writer.root),
                },
            )

            logger.info("Dependency security analysis completed.")

            return {
                "success": True,
                "action": "analyze_dependency_security",
                "result": result,
            }
        
        # -------------------------------------------------
        # Generate Security Report (via MCP)
        # -------------------------------------------------

        if action.action == "generate_security_report":

            result = await self.client.call_tool(
                "generate_security_report",
                {
                    "project_root": str(self.writer.root),
                },
            )

            logger.info("Security report generated.")

            return {
                "success": True,
                "action": "generate_security_report",
                "result": result,
            }
        
        logger.error(
            "Unknown action received: %s",
            action.action,
        )

        raise ValueError(
            f"Unknown action: {action.action}"
        )