
from dataclasses import dataclass
from tokens.identifier import VariableScope as VarS


@dataclass(slots=True)
class Symbol:
    type: str
    kind: VarS
    index: int

class SymbolTable:
    def __init__(self,name:str) -> None:
        self.class_table: dict[str, Symbol] = {}
        self.subroutine_table: dict[str, Symbol] = {}
        self.index_counters: dict[VarS, int] = {kind: 0 for kind in VarS}
        self.name = name

    def start_subroutine(self):
        """Reset the subroutine scope and index counters for ARGUMENT and VAR."""
        self.subroutine_table.clear()
        self.index_counters[VarS.ARGUMENT] = 0
        self.index_counters[VarS.VAR] = 0

    def define(self, name: str, type: str, kind: VarS) -> None:
        """Define a new identifier of a given name, type, and kind."""
        index = self.index_counters[kind]
        symbol = Symbol(type=type, kind=kind, index=index)
        match kind:
            case VarS.STATIC | VarS.FIELD:
                self.class_table[name] = symbol
            case VarS.ARGUMENT | VarS.VAR:
                self.subroutine_table[name] = symbol
            case _:
                raise ValueError(f"Invalid kind: {kind}")
        self.index_counters[kind] += 1

    def var_count(self, kind: VarS) -> int:
        """Return the number of variables of the given kind already defined."""
        return self.index_counters[kind]

    def get_symbol(self, name: str) -> Symbol | None:
        """Return the symbol of the named identifier in the current scope."""
        symbol = self.subroutine_table.get(name) or self.class_table.get(name)
        return symbol

