from pydantic import BaseModel


class Symbol(BaseModel):
    name: str
    symbol_type: str
    file: str
    line: int


class SymbolIndex(BaseModel):
    symbols: list[Symbol] = []