"""
Jack token definitions and utilities. 
It supports validation, type identification, and unified
access to token values and types for use in Jack language parsing and analysis.
"""

from __future__ import annotations
from tokens.enums import Keyword, Symbol
from tokens.inmutables import IntegerConstant, StringConstant
from tokens.identifier import Identifier, IdentifierContext
from tokens.type import TokenType

from abc import ABC, abstractmethod


class Token(ABC):
    @property
    @abstractmethod
    def ttype(self): ...
    @property
    @abstractmethod
    def value(self): ...
      
    def set_context(self, context: IdentifierContext):
        """Set the context of the token if it is an Identifier."""
        if isinstance(self._token, Identifier):
            self._token.context = context
        else:
            raise TypeError("Only Identifier tokens can have context set.")
    
    @property
    def context(self) -> str|IdentifierContext:
        """Return the context of the token."""
        return self._token.context


    def __eq__(self, other: object) -> bool:
        """Compare Token to another Token or token object."""
        return self._token == other or self._token == getattr(other, '_token', None)

    def __hash__(self) -> int:
        """Return hash of underlying token for sets/dicts."""
        return hash(self._token)

    def is_in(self, items: list[Keyword|Symbol|IntegerConstant|StringConstant|Identifier])->bool:
        # Allow: if Keyword.STATIC in token
        return self._token in items

    def xml(self) -> str:
        """Return XML representation of the token."""
        return f'<{self.ttype.value}{self.context}> {self._token} </{self.ttype.value}>\n'

    def is_type(self) -> bool:
        """Return True if token is a type keyword or identifier."""
        return self.ttype == TokenType.KEYWORD and self.is_in([Keyword.INT, Keyword.CHAR, Keyword.BOOLEAN]) or self.ttype == TokenType.IDENTIFIER

    def is_subroutine(self) -> bool:
        """Return True if token is a subroutine keyword."""
        return self.is_in([Keyword.CONSTRUCTOR, Keyword.FUNCTION, Keyword.METHOD])

    def is_keyword_constant(self) -> bool:
        """Return True if token is a keyword constant."""
        return self.ttype == TokenType.KEYWORD and self.is_in([Keyword.TRUE, Keyword.FALSE, Keyword.NULL, Keyword.THIS])

    def is_constant(self) -> bool:
        """Return True if token is any kind of constant."""
        return self.ttype in (TokenType.INT_CONST, TokenType.STRING_CONST) or self.is_keyword_constant()

    def is_unary_op(self) -> bool:
        """Return True if token is a unary operator."""
        return self.ttype == TokenType.SYMBOL and self.is_in([Symbol.MINUS, Symbol.NOT])

    def is_op(self) -> bool:
        """Return True if token is a binary operator."""
        return self.ttype == TokenType.SYMBOL and self.is_in([Symbol.PLUS, Symbol.MINUS, Symbol.MULT, Symbol.DIV, Symbol.AND, Symbol.OR, Symbol.LT, Symbol.GT, Symbol.EQ])