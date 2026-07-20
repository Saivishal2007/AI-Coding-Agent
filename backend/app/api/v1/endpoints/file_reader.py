from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.services.file_reader_service import FileReaderService

router = APIRouter()


@router.get("/read")
async def read_file(path: str):
    try:
        reader = FileReaderService(str(Path.cwd()))
        return reader.read(path)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))