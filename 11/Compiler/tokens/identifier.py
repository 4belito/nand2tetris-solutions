from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from tokens.type import TokenType
import re

class IdentifierCategory(Enum):
    """Enum for Jack identifier categories."""
    CLASS = "class"
    SUBROUTINE = "subroutine"
    VAR_SCOPE = "var_scope"

    def __str__(self) -> str:
        """Return string representation of the identifier category."""
        return self.value

class VariableScope(Enum):
    """Enum for Jack variable scopes."""
    VAR = "var"
    ARGUMENT = "argument"
    STATIC = "static"
    FIELD = "field"

    def __str__(self) -> str:
        """Return string representation of the identifier category."""
        return self.value
    
@dataclass
class IdentifierContext:
    """Class for Jack identifier context."""
    category: IdentifierCategory
    is_def: bool 
    scope: VariableScope | None = None
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
        #obj.context = IdentifierContext(type=IdentifierType.VARIABLE, is_def=False)
        return obj

    @property
    def value(self) -> str:
        """Return identifier value."""
        return self

    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack identifier."""
        return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value))
