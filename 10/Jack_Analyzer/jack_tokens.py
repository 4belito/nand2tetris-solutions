from enum import Enum
import re


# Enum for all enumerated token types
class EnumTokens(Enum):
    @classmethod
    def valid(cls, value: str) -> bool:
        return value in set(item.value for item in cls)

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


class Keyword(EnumTokens):
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
    def ttype(self) -> str:
        return TokenType.KEYWORD.value

class Symbol(EnumTokens):
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
    def ttype(self) -> str:
        return TokenType.SYMBOL.value

class IntegerConstant(int):
    MAX_VALUE = 32767

    def __new__(cls, value: str) -> int:
        return int.__new__(cls, value)
    
    @property
    def value(self) -> int:
        return self

    @property
    def ttype(self) -> str:
        return TokenType.INT_CONST.value

    @staticmethod
    def valid(value: str) -> bool:
        return  value.isdigit() and 0 <= int(value) <= IntegerConstant.MAX_VALUE


class StringConstant(str):
    def __new__(cls, value):
        return str.__new__(cls, value)

    @property
    def value(self) -> str:
        return self[1:-1]

    @property
    def ttype(self) -> str:
        return TokenType.STRING_CONST.value

    @classmethod
    def valid(cls, value: str) -> bool:
        start, inner_value, end = value[0], value[1:-1], value[-1]
        return start=='"' and end=='"' and '\n' not in inner_value



class Identifier(str):
    def __new__(cls, value: str):
        return str.__new__(cls, value)

    @property
    def ttype(self) -> str:
        return TokenType.IDENTIFIER.value

    @property
    def value(self) -> str:
        return str(self)

    @classmethod
    def valid(cls, value: str) -> bool:
        # Jack identifier: non-empty, only letters/digits/underscore, not starting with digit
        return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value))


class Token:
    def __init__(self, value: str):
        for token_cls in (Keyword, Symbol, IntegerConstant, StringConstant, Identifier):
            if token_cls.valid(value):
                self._token = token_cls(value)
                break
        else:
            raise ValueError(f"Unknown token type for value {value}")

    @property
    def ttype(self) -> str:
        return self._token.ttype

    @property
    def value(self) -> str|int:
        return self._token.value
        
