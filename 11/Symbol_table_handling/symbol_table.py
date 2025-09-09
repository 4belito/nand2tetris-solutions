
from dataclasses import dataclass
from tokens.identifier import Identifier
from enum import Enum
from dataclasses import dataclass
from tokens.identifier import Identifier, IdentifierCategory


class VariableKind(Enum):
    """Enum for Jack variable kinds."""
    VAR = "var"
    ARGUMENT = "argument"
    STATIC = "static"
    FIELD = "field"

    def __str__(self) -> str:
        """Return string representation of the identifier category."""
        return self.value

class PrimitiveType(Enum):
    """Enum for Jack variable types."""
    INT = "int"
    CHAR = "char"
    BOOLEAN = "boolean"

    def __str__(self) -> str:
        """Return string representation of the variable type."""
        return self.value

@dataclass
class IdentifierContext:
    """Class for Jack identifier context."""
    category: IdentifierCategory
    is_def: bool
    kind: VariableKind | None = None
    index: int | None = None

    def __repr__(self):
        # Clean, parenthesis-free string for XML output, with leading space if not empty
        s = " ".join(f"{k}='{v}'" for k, v in vars(self).items() if v is not None)
        if s: s=" " + s
        return s


VarK = VariableKind  # Alias for brevity
VarT = PrimitiveType | Identifier  # Variable type can be a primitive or a class name

@dataclass(slots=True)
class Symbol:
    type: VarT
    kind: VarK
    index: int

class SymbolTable:
    def __init__(self) -> None:
        self.class_table: dict[str, Symbol] = {}
        self.subroutine_table: dict[Identifier, Symbol] = {}
        self.index_counters: dict[VarK, int] = {kind: 0 for kind in VarK}
        self.class_name: Identifier

    def start_subroutine(self):
        """Reset the subroutine scope and index counters for ARGUMENT and VAR."""
        self.subroutine_table.clear()
        self.index_counters[VarK.ARGUMENT] = 0
        self.index_counters[VarK.VAR] = 0

    def define(self, name: Identifier, type: VarT, kind: VarK) -> None:
        """Define a new identifier of a given name, type, and kind."""
        index = self.var_count(kind)
        symbol = Symbol(type=type, kind=kind, index=index)
        match kind:
            case VarK.STATIC | VarK.FIELD:
                self.class_table[name] = symbol
            case VarK.ARGUMENT | VarK.VAR:
                self.subroutine_table[name] = symbol
            case _:
                raise ValueError(f"Invalid kind: {kind}")
        self.index_counters[kind] += 1

    def var_count(self, kind: VarK) -> int:
        """Return the number of variables of the given kind already defined."""
        return self.index_counters[kind]

    def get_symbol(self, name: Identifier) -> Symbol | None:
        """Return the symbol of the named identifier in the current scope."""
        symbol = self.subroutine_table.get(name) or self.class_table.get(name)
        return symbol

