from enum import Enum

class TokenType(Enum):
    """Enum for Jack token types."""
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"