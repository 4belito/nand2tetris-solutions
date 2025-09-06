
from dataclasses import dataclass

@dataclass
class Symbol:
    type: str
    kind: str
    index: int


class SymbolTable:
    def __init__(self):
        self._symbols = {}


table: dict[str, dict[str, str | int]] = {
    'x': {'type': 'int', 'kind': 'static', 'index': 0},
    'y': {'type': 'boolean', 'kind': 'field', 'index': 1},
    'pointCount': {'type': 'int', 'kind': 'static', 'index': 0},
}