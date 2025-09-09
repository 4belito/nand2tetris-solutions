from __future__ import annotations

from enum import Enum
import re

class IdentifierCategory(Enum):
    """Enum for Jack identifier categories."""
    CLASS = "class"
    SUBROUTINE = "subroutine"
    VARIABLE = "variable"

    def __str__(self) -> str:
        """Return string representation of the identifier category."""
        return self.value
    
class Identifier(str):
    """Class for Jack identifiers."""

    def __new__(cls, name: str) -> Identifier:
        """Create Identifier from string value."""
        obj = str.__new__(cls, name)
        return obj

    @property
    def value(self) -> str:
        """Return identifier value."""
        return self

    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack identifier."""
        return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value))
