"""JackTokenizer module: Provides functionality to tokenize Jack source code.

This module defines the JackTokenizer class, which reads Jack source files,
removes comments, splits the code into raw tokens, and provides access to
individual tokens for further parsing and analysis.
"""
from __future__ import annotations

import re
from collections import deque
from tokens.identifier import Identifier
from tokens.enums import Keyword, Symbol, PRIMITIVE_TYPES, KEYWORD_CONSTANTS
from tokens.inmutables import IntegerConstant, StringConstant
from tokens.enums import Symbol
from symbol_table import VariableKind,VarT
from typing import overload,Literal

Token = Identifier | Keyword | Symbol | IntegerConstant | StringConstant

class JackTokenizer:
    """Tokenizes Jack source code and provides access to tokens."""

    def __init__(self, input_file: str):
        """Initialize tokenizer from a Jack source file."""
        try:
            with open(input_file, "r") as f:
                text = f.read()
        except OSError as e:
            raise RuntimeError(f"Failed to open {input_file}: {e}")
        self._raw_tokens: deque[str] = deque(JackTokenizer._raw_tokenize(text))
        self.token: Token
        self._advance()

    def has_more_tokens(self) -> bool:
        """Return True if there are more tokens to process."""
        return len(self._raw_tokens) > 0

    def _advance(self):
        '''
        Get the next token from the input, and makes it the current token.
        This method should be called only if has_more_tokens() is true.
        Initially there is not current token.
        '''
        raw_token = self._raw_tokens.popleft()
        for token_cls in (Keyword, Symbol, IntegerConstant, StringConstant, Identifier):
            if token_cls.valid(raw_token):
                self.token = token_cls(raw_token)
                return
        raise RuntimeError(f"Unknown token type for value {raw_token}")

    ## NO API METHODS BELOW THIS LINE ##
    def peek(self) -> Token:
        """Return the next token without advancing the tokenizer."""
        if self.has_more_tokens():
            raw_token = self._raw_tokens[0]
            for token_cls in (Keyword, Symbol, IntegerConstant, StringConstant, Identifier):
                if token_cls.valid(raw_token):
                    return token_cls(raw_token)
        raise RuntimeError("No more tokens to peek.")

    def token_is_var_type(self) -> bool:
        """Return True if token is a type keyword or identifier."""
        return self.token in PRIMITIVE_TYPES or isinstance(self.token, Identifier)

    def token_is_constant(self) -> bool:
        """Return True if token is any kind of constant."""
        return isinstance(self.token, (IntegerConstant, StringConstant)) or self.token in KEYWORD_CONSTANTS

    def consume_var_kind(self,*var_kinds:Keyword) -> VariableKind:
        """
        Map a Keyword to a VariableKind.
        note: Argument is excluded because it is not a keyword.
        """
        match self.token:
            case Keyword.VAR:
                var_kind = VariableKind.LOCAL
            case Keyword.STATIC:
                var_kind = VariableKind.STATIC
            case Keyword.FIELD:
                var_kind = VariableKind.THIS
            case _:
                raise ValueError(f"Cannot get VariableKind from {self.token}.")
        self.consume(*var_kinds)
        return var_kind

    @overload
    def consume(self, *token: Keyword) -> Keyword: ...

    @overload
    def consume(self, *token: Symbol) -> Symbol: ...

    @overload
    def consume(self, *token: type[Identifier]) -> Identifier: ...

    @overload
    def consume(self, __token1: Literal[Keyword.INT],
                __token2: Literal[Keyword.CHAR],
                __token3: Literal[Keyword.BOOLEAN],
                __token4: type[Identifier],
                ) -> VarT: ...

    @overload
    def consume(self,*tokens: Keyword | Symbol | type[Identifier]) -> Token: ...

    def consume(self, *tokens: Keyword | Symbol | type[Identifier]) -> Token:
        """
        Write and advance if the current token matches any of the provided tokens.
        If no tokens are provided, always write and advance.
        """
        if not tokens or any(
            self.token == t or (isinstance(t, type) and isinstance(self.token, t))
            for t in tokens
        ):
            token = self.token
            if self.has_more_tokens():
                self._advance()
            return token
        else:
            expected = ', '.join(str(t) for t in tokens)
            raise ValueError(f"Expected one of: {expected}, got: '{self.token}'")

    @staticmethod
    def _raw_tokenize(text: str) -> list[str]:
        """
        Perform raw tokenization of Jack source code and return a list of raw_tokens.
        Removes comments and splits by symbols, string constants, and whitespace.
        """
        # Remove block comments (/* ... */) and line comments (// ...)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'//.*?\n', '', text, flags=re.DOTALL)
        # Regex pattern: match symbols, string constants, or whitespace
        string_pattern = r'"[^"\n]*"'
        pattern = r'([' + re.escape(''.join(Symbol.values())) + r'])|(' + string_pattern + r')|\s+'
        # Split and filter out empty strings
        tokens = [raw_token for raw_token in re.split(pattern, text) if raw_token]
        return tokens

    ### THIS API METHODS WERE NOT USED.
    # I used consume(token) method instead of these methods.

    # def token_type(self) -> type[Token]:
    #     """Return the type of the current token."""
    #     return type(self.token)
    # def keyword(self) -> Keyword:
    #     """Return the current token as a Keyword."""
    #     if isinstance(self.token, Keyword):
    #         return self.token
    #     raise RuntimeError("Current token is not a Keyword.")

    # def symbol(self) -> Symbol:
    #     """Return the current token as a Symbol."""
    #     if isinstance(self.token, Symbol):
    #         return self.token
    #     raise RuntimeError("Current token is not a Symbol.")

    # def identifier(self) -> Identifier:
    #     """Return the current token as an Identifier."""
    #     if isinstance(self.token, Identifier):
    #         return self.token
    #     raise RuntimeError("Current token is not an Identifier.")

    # def int_val(self) -> IntegerConstant:
    #     """Return the current token as an IntegerConstant."""
    #     if isinstance(self.token, IntegerConstant):
    #         return self.token
    #     raise RuntimeError("Current token is not an IntegerConstant.")

    # def string_val(self) -> StringConstant:
    #     """Return the current token as a StringConstant."""
    #     if isinstance(self.token, StringConstant):
    #         return self.token
    #     raise RuntimeError("Current token is not a StringConstant.")



# Note: Peek method is added to the API for looking the next token without consuming it.
# The remaining method in the API are substituted by the token data structure itself.