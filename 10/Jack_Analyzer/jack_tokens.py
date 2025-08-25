"""
Jack token definitions and utilities. 
It supports validation, type identification, and unified
access to token values and types for use in Jack language parsing and analysis.
"""

from enum import Enum
import re

class EnumTokens(Enum):
    """Base enum class for Jack token types with utility methods."""
    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid enum member."""
        return value in set(item.value for item in cls)

    @classmethod
    def values(cls) -> list[str]:
        """Return all enum values as a list."""
        return [item.value for item in cls]

    def __str__(self) -> str:
        """Return string representation of the enum member."""
        return self.value


class TokenType(Enum):
    """Enum for Jack token types."""
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"


class Keyword(EnumTokens):
    """Enum for Jack language keywords."""
    CLASS = "class"
    CONSTRUCTOR = "constructor"    
    FUNCTION = "function"    
    METHOD = "method"
    FIELD = "field"
    STATIC = "static"
    VAR = "var"   
    INT = "int"
    CHAR = "char"   
    BOOLEAN = "boolean"
    VOID = "void"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"

    @property
    def ttype(self) -> TokenType:
        """Return TokenType.KEYWORD."""
        return TokenType.KEYWORD

class Symbol(EnumTokens):
    """Enum for Jack language symbols."""
    LBRACE = '{'
    RBRACE = '}'
    LPAREN = '('
    RPAREN = ')'
    LBRACK = '['
    RBRACK = ']'
    DOT = "."
    COMMA = ","
    SEMICOLON = ";"
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    DIV = "/"
    AND = "&"
    OR = "|"
    LT = "<"
    GT = ">"
    EQ = "="
    NOT = "~"

    @property
    def ttype(self) -> TokenType:
        """Return TokenType.SYMBOL."""
        return TokenType.SYMBOL

    def __str__(self) -> str:
        """Return string representation of the symbol."""
        match self:
            case Symbol.LT:
                return "&lt;"
            case Symbol.GT:
                return "&gt;"
            case Symbol.AND:
                return "&amp;"
            case _:
                return self.value

class IntegerConstant(int):
    """Class for Jack integer constants."""
    MAX_VALUE = 32767

    def __new__(cls, value: str) -> int:
        """Create IntegerConstant from string value."""
        return int.__new__(cls, value)
    
    @property
    def value(self) -> int:
        """Return integer value."""
        return self

    @property
    def ttype(self) -> TokenType:
        """Return TokenType.INT_CONST."""
        return TokenType.INT_CONST

    @staticmethod
    def valid(value: str) -> bool:
        """Return True if value is a valid Jack integer constant."""
        return  value.isdigit() and 0 <= int(value) <= IntegerConstant.MAX_VALUE


class StringConstant(str):
    """Class for Jack string constants."""
    def __new__(cls, value: str) -> 'StringConstant':
        """Create StringConstant from string value."""
        return str.__new__(cls, value)

    @property
    def value(self) -> str:
        """Return string value without quotes."""
        return self

    @property
    def ttype(self) -> TokenType:
        """Return TokenType.STRING_CONST."""
        return TokenType.STRING_CONST

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


class Identifier(str):
    """Class for Jack identifiers."""
    def __new__(cls, value: str) -> 'Identifier':
        """Create Identifier from string value."""
        return str.__new__(cls, value)

    @property
    def ttype(self) -> TokenType:
        """Return TokenType.IDENTIFIER."""
        return TokenType.IDENTIFIER

    @property
    def value(self) -> str:
        """Return identifier value."""
        return self
    
    @classmethod
    def valid(cls, value: str) -> bool:
        """Return True if value is a valid Jack identifier."""
        return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value))


class Token:
    """Wrapper for Jack tokens, providing unified access to type and value."""
    def __init__(self, value: str):
        """Create Token from string value, determining its type."""
        for token_cls in (Keyword, Symbol, IntegerConstant, StringConstant, Identifier):
            if token_cls.valid(value):
                self._token = token_cls(value)
                break
        else:
            raise ValueError(f"Unknown token type for value {value}")

    @property
    def ttype(self) -> TokenType:
        """Return token type."""
        return self._token.ttype

    @property
    def value(self) -> str|int:
        """Return token value."""
        return self._token.value
    
    def __eq__(self, other: object) -> bool:
        """Compare Token to another Token or token object."""
        return self._token == other or self._token == getattr(other, '_token', None)

    def __hash__(self) -> int:
        """Return hash of underlying token for sets/dicts."""
        return hash(self._token)

    def xml(self) -> str:
        """Return XML representation of the token."""
        token = self._token
        return f'<{token.ttype.value}> {token} </{token.ttype.value}>\n'
    
    def is_type(self) -> bool:
        """Return True if token is a type keyword or identifier."""
        token = self._token
        return token in (Keyword.INT, Keyword.CHAR, Keyword.BOOLEAN) or token.ttype == TokenType.IDENTIFIER

    def is_statement(self) -> bool:
        """Return True if token is a statement keyword."""
        token = self._token
        return token.ttype == TokenType.KEYWORD and token in (Keyword.LET, Keyword.IF, Keyword.WHILE, Keyword.DO, Keyword.RETURN)

    def is_subroutine(self) -> bool:
        """Return True if token is a subroutine keyword."""
        token = self._token
        return token.ttype == TokenType.KEYWORD and token in (Keyword.CONSTRUCTOR, Keyword.FUNCTION, Keyword.METHOD)

    def is_keyword_constant(self) -> bool:
        """Return True if token is a keyword constant."""
        token = self._token
        return token.ttype == TokenType.KEYWORD and token in (Keyword.TRUE, Keyword.FALSE, Keyword.NULL, Keyword.THIS)

    def is_constant(self) -> bool:
        """Return True if token is any kind of constant."""
        token = self._token
        return token.ttype in (TokenType.INT_CONST, TokenType.STRING_CONST) or self.is_keyword_constant()

    def is_unary_op(self) -> bool:
        """Return True if token is a unary operator."""
        token = self._token
        return token.ttype == TokenType.SYMBOL and token in (Symbol.MINUS, Symbol.NOT)

    def is_op(self) -> bool:
        """Return True if token is a binary operator."""
        token = self._token
        return token.ttype == TokenType.SYMBOL and token in (Symbol.PLUS, Symbol.MINUS, Symbol.MULT, Symbol.DIV, Symbol.AND, Symbol.OR, Symbol.LT, Symbol.GT, Symbol.EQ)