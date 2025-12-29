from __future__ import annotations


class IntegerConstant(int):
    """Class for Jack integer constants."""

    MAX_VALUE = 32767

    def __new__(cls, value: str) -> IntegerConstant:
        """Create IntegerConstant from string value."""
        return int.__new__(cls, value)

    @staticmethod
    def valid(value: str) -> bool:
        """Return True if value is a valid Jack integer constant."""
        return value.isdigit() and 0 <= int(value) <= IntegerConstant.MAX_VALUE


class StringConstant(str):
    """Class for Jack string constants."""

    def __new__(cls, value: str) -> StringConstant:
        """Create StringConstant from string value."""
        return str.__new__(cls, value)

    def __str__(self) -> str:
        """Return string representation of the string constant."""
        return self[1:-1]

    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack string constant."""
        return len(value) > 1 and value[0] == '"' and value[-1] == '"'
