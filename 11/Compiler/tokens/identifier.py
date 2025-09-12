from __future__ import annotations

import re


class Identifier(str):
    """Class for Jack identifiers."""

    def __new__(cls, name: str) -> Identifier:
        """Create Identifier from string value."""
        obj = str.__new__(cls, name)
        return obj

    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack identifier."""
        return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", value))
