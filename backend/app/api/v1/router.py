from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    agent,
    repository,
    file_reader,
    edit,
    stream,
)

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["health"],
)

api_router.include_router(
    agent.router,
    prefix="/agent",
    tags=["agent"],
)

# ADD THIS 👇
api_router.include_router(
    stream.router,
    prefix="/agent",
    tags=["agent"],
)

api_router.include_router(
    repository.router,
    prefix="/repository",
    tags=["repository"],
)

api_router.include_router(
    file_reader.router,
    prefix="/files",
    tags=["files"],
)

api_router.include_router(
    edit.router,
    prefix="/agent",
    tags=["agent"],
)