from __future__ import annotations
from tokens.type import TokenType


class IntegerConstant(int):
    """Class for Jack integer constants."""
    MAX_VALUE = 32767
    ttype = TokenType.INT_CONST
    context = ""

    def __new__(cls, value: str) -> IntegerConstant:
        """Create IntegerConstant from string value."""
        return int.__new__(cls, value)

    @property
    def value(self) -> str:
        """Return integer value."""
        return str(self)

    @staticmethod
    def valid(value: str) -> bool:
        """Return True if value is a valid Jack integer constant."""
        return  value.isdigit() and 0 <= int(value) <= IntegerConstant.MAX_VALUE


class StringConstant(str):
    """Class for Jack string constants."""
    ttype = TokenType.STRING_CONST
    context = ""

    def __new__(cls, value: str) -> StringConstant:
        """Create StringConstant from string value."""
        return str.__new__(cls, value)

    @property
    def value(self) -> str:
        """Return string value without quotes."""
        return self


    def __str__(self) -> str:
        """Return string representation of the string constant."""
        return self.value[1:-1]

    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack string constant."""
        if len(value) < 2 or value[0] != '"' or value[-1] != '"':
            return False
        inner_value = value[1:-1]
        return '\n' not in inner_value and '"' not in inner_value