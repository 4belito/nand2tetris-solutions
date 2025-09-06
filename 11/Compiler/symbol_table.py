
from dataclasses import dataclass
from tokens.identifier import VariableCategory as VarCat


@dataclass(slots=True)
class Symbol:
    type: str
    kind: VarCat
    index: int

class SymbolTable:
    def __init__(self):
        self.class_table: dict[str, Symbol] = {}
        self.subroutine_table: dict[str, Symbol] = {}
        self.index_counters: dict[VarCat, int] = {kind: 0 for kind in VarCat}

    def start_subroutine(self):
        """Reset the subroutine scope and index counters for ARGUMENT and VAR."""
        self.subroutine_table.clear()
        self.index_counters[VarCat.ARGUMENT] = 0
        self.index_counters[VarCat.VAR] = 0

    def define(self, name: str, type: str, kind: VarCat):
        """Define a new identifier of a given name, type, and kind."""
        index = self.index_counters[kind]
        symbol = Symbol(type=type, kind=kind, index=index)
        match kind:
            case VarCat.STATIC | VarCat.FIELD:
                self.class_table[name] = symbol
            case VarCat.ARGUMENT | VarCat.VAR:
                self.subroutine_table[name] = symbol
            case _:
                raise ValueError(f"Invalid kind: {kind}")
        self.index_counters[kind] += 1

    def var_count(self, kind: VarCat) -> int:
        """Return the number of variables of the given kind already defined."""
        return self.index_counters[kind]

    def get_symbol(self, name: str) -> Symbol:
        """Return the symbol of the named identifier in the current scope."""
        symbol = self.subroutine_table.get(name) or self.class_table.get(name)
        if symbol is None:
            raise KeyError(f"Identifier '{name}' not found in symbol table.")
        return symbol

