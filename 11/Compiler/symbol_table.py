
from dataclasses import dataclass
from tokens.identifier import Identifier
from enum import Enum
from dataclasses import dataclass
from tokens.identifier import Identifier, IdentifierCategory
from tokens.enums import Keyword
from typing import Literal

class VariableKind(Enum):
    """Enum for Jack variable kinds."""
    LOCAL = "var"
    ARG = "argument"
    STATIC = "static"
    THIS = "field" # 'this' in VM, 'field' in Jack I named THIS for coding convenience.

    def __str__(self) -> str:
        """Return string representation of the identifier category."""
        return self.value

class VarUse(Enum):
    """Enum for Jack variable usage."""
    DEF = "def"
    REF = "ref"
    ASSIGN = "assign"

    def __str__(self) -> str:
        """Return string representation of the variable usage."""
        return self.value

@dataclass
class IdentifierContext:
    """Class for Jack identifier context."""
    category: IdentifierCategory
    use: VarUse
    kind: VariableKind | None = None
    index: int | None = None

    def __repr__(self):
        # Clean, parenthesis-free string for XML output, with leading space if not empty
        s = " ".join(f"{k}='{v}'" for k, v in vars(self).items() if v is not None)
        if s: s=" " + s
        return s


VarK = VariableKind  # Alias for brevity
VarT = Literal[Keyword.INT,Keyword.CHAR,Keyword.BOOLEAN] | Identifier

@dataclass(slots=True)
class Variable:
    type: VarT
    kind: VarK
    index: int

class SymbolTable:
    def __init__(self) -> None:
        self._class_table: dict[str, Variable] = {}
        self._subroutine_table: dict[Identifier, Variable] = {}
        self._index_counters: dict[VarK, int] = {kind: 0 for kind in VarK}
        self.subroutine_name: Identifier

    def start_subroutine(self):
        """Reset the subroutine scope and index counters for ARGUMENT and VAR."""
        self._subroutine_table.clear()
        self._index_counters[VarK.ARG] = 0
        self._index_counters[VarK.LOCAL] = 0

    def define(self, name: Identifier, type: VarT, kind: VarK) -> None:
        """Define a new identifier of a given name, type, and kind."""
        index = self.var_count(kind)
        symbol = Variable(type=type, kind=kind, index=index)
        match kind:
            case VarK.STATIC | VarK.THIS:
                self._class_table[name] = symbol
            case VarK.ARG | VarK.LOCAL:
                self._subroutine_table[name] = symbol
            case _:
                raise ValueError(f"Invalid kind: {kind}")
        self._index_counters[kind] += 1

    def var_count(self, kind: VarK) -> int:
        """Return the number of variables of the given kind already defined."""
        return self._index_counters[kind]

    def kind_of(self, name: Identifier) -> VarK | None:
        """Return the kind of the named identifier in the current scope."""
        symbol = self.get_var(name)
        return symbol.kind if symbol else None

    ### THIS API METHOD WERE NOT USED.
    # def type_of(self, name: Identifier) -> VarT:
    #     """Return the type of the named identifier in the current scope."""
    #     symbol = self.get_var(name)
    #     if symbol is None:
    #         raise ValueError(f"Identifier '{name}' not found in symbol table.")
    #     return symbol.type

    def index_of(self, name: Identifier) -> int:
        """Return the index assigned to the named identifier."""
        symbol = self.get_var(name)
        if symbol is None:
            raise ValueError(f"Identifier '{name}' not found in symbol table.")
        return symbol.index

    ## NO API METHODS BELOW THIS LINE ##
    def get_var(self, name: Identifier) -> Variable| None:
        """Return the symbol of the named identifier in the current scope."""
        return self._subroutine_table.get(name) or self._class_table.get(name)

