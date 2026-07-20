from pathlib import Path

from fastapi import APIRouter

from app.services.repository_service import RepositoryService

router = APIRouter()


@router.get("/scan")
async def scan_repository():
    """
    Scan the current backend repository.
    """

    root = Path.cwd()

    scanner = RepositoryService(str(root))

    return scanner.scan()