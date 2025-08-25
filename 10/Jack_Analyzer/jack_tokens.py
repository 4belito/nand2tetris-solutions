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
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"


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
    def ttype(self) -> TokenType:
        return TokenType.KEYWORD

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
        return TokenType.SYMBOL

class IntegerConstant(int):
    MAX_VALUE = 32767

    def __new__(cls, value: str) -> int:
        return int.__new__(cls, value)
    
    @property
    def value(self) -> int:
        return self

    @property
    def ttype(self) -> TokenType:
        return TokenType.INT_CONST

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
    def ttype(self) -> TokenType:
        return TokenType.STRING_CONST

    @classmethod
    def valid(cls, value: str) -> bool:
        if len(value) < 2 or value[0] != '"' or value[-1] != '"':
            return False
        inner_value = value[1:-1]
        return '\n' not in inner_value and '"' not in inner_value



class Identifier(str):
    def __new__(cls, value: str):
        return str.__new__(cls, value)

    @property
    def ttype(self) -> TokenType:
        return TokenType.IDENTIFIER

    @property
    def value(self) -> str:
        return str(self)

    @classmethod
    def valid(cls, value: str) -> bool:
        # Jack identifier: non-empty, only letters/digits/underscore, not starting with digit
        return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value))


class Token:
    """
    Wrapper for Jack tokens, providing unified access to type and value.
    """
    def __init__(self, value: str):
        for token_cls in (Keyword, Symbol, IntegerConstant, StringConstant, Identifier):
            if token_cls.valid(value):
                self._token = token_cls(value)
                break
        else:
            raise ValueError(f"Unknown token type for value {value}")

    @property
    def ttype(self) -> TokenType:
        return self._token.ttype

    @property
    def value(self) -> str|int:
        return self._token.value
    

    def __eq__(self, other):
        return self._token == other or self._token == getattr(other, '_token', None)

    def __hash__(self):
        return hash(self._token)

    def xml(self):
        token = self._token
        return f'<{token.ttype.value}> {token.value} </{token.ttype.value}>\n'
    
    def is_type(self):
        token = self._token
        return token in (Keyword.INT, Keyword.CHAR, Keyword.BOOLEAN) or token.ttype == TokenType.IDENTIFIER

    def is_statement(self):
        token = self._token
        return token.ttype == TokenType.KEYWORD and token in (Keyword.LET, Keyword.IF, Keyword.WHILE, Keyword.DO, Keyword.RETURN)

    def is_subroutine(self):
        token = self._token
        return token.ttype == TokenType.KEYWORD and token in (Keyword.CONSTRUCTOR, Keyword.FUNCTION, Keyword.METHOD)

    def is_keyword_constant(self):
        token = self._token
        return token.ttype == TokenType.KEYWORD and token in (Keyword.TRUE, Keyword.FALSE, Keyword.NULL, Keyword.THIS)

    def is_constant(self):
        token = self._token
        return token.ttype in (TokenType.INT_CONST, TokenType.STRING_CONST) or self.is_keyword_constant()

    def is_unary_op(self):
        token = self._token
        return token.ttype == TokenType.SYMBOL and token in (Symbol.MINUS, Symbol.NOT)

    def is_op(self):
        token = self._token
        return token.ttype == TokenType.SYMBOL and token in (Symbol.PLUS, Symbol.MINUS, Symbol.MULT, Symbol.DIV, Symbol.AND, Symbol.OR, Symbol.LT, Symbol.GT, Symbol.EQ)