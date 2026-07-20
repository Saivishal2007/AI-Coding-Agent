from pydantic import BaseModel


class CrossReference(BaseModel):
    source_file: str
    imported_module: str


class CrossReferenceIndex(BaseModel):
    references: list[CrossReference] = []