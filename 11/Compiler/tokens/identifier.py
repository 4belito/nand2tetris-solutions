from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from tokens.type import TokenType
import re
from tokens.enums import Keyword

class IdentifierType(Enum):
    """Enum for Jack identifier types."""
    CLASS = "class"
    SUBROUTINE = "subroutine"
    VARIABLE = "variable"

    def __repr__(self) -> str:
        """Return string representation of the identifier type."""
        return self.value
    
class VariableCategory(Enum):
    """Enum for Jack variable categories."""
    VAR = "var"
    ARGUMENT = "argument"
    STATIC = "static"
    FIELD = "field"

    @staticmethod
    def from_keyword(kw: Keyword) -> VariableCategory:
        """Map a Keyword to a VariableCategory."""
        match kw:
            case Keyword.VAR:
                return VariableCategory.VAR
            case Keyword.STATIC:
                return VariableCategory.STATIC
            case Keyword.FIELD:
                return VariableCategory.FIELD
            case _:
                raise ValueError(f"Cannot convert {kw} to VariableCategory.")


@dataclass
class IdentifierContext:
    """Class for Jack identifier context."""
    type: IdentifierType
    is_def: bool
    category: VariableCategory | None = None
    index: int | None = None

    def __repr__(self):
        # Clean, parenthesis-free string for XML output, with leading space if not empty
        s = " ".join(f"{k}='{v}'" for k, v in vars(self).items())
        if s: s=" " + s
        return s

class Identifier(str):
    """Class for Jack identifiers."""
    ttype = TokenType.IDENTIFIER
    context: IdentifierContext

    def __new__(cls, name: str) -> Identifier:
        """Create Identifier from string value."""
        obj = str.__new__(cls, name)
        obj.context = IdentifierContext(type=IdentifierType.VARIABLE, is_def=False)
        return obj

    @property
    def value(self) -> str:
        """Return identifier value."""
        return self

    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack identifier."""
        return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value))
