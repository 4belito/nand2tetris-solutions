from enum import Enum
from tokens.type import TokenType

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
    
    @property
    def context(self) -> str:
        """Return context for the keyword."""
        return ""


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