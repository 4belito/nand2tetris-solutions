"""JackTokenizer module: Provides functionality to tokenize Jack source code.

This module defines the JackTokenizer class, which reads Jack source files,
removes comments, splits the code into raw tokens, and provides access to
individual tokens for further parsing and analysis.
"""

import re
from collections import deque
from tokens.identifier import Identifier
from tokens.enums import Keyword, Symbol, PRIMITIVE_TYPE, KEYWORD_CONSTANTS
from tokens.inmutables import IntegerConstant, StringConstant
from tokens.enums import Symbol
from symbol_table import VariableKind, PrimitiveType, VarT

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
        self.advance()

    def has_more_tokens(self) -> bool:
        """Return True if there are more tokens to process."""
        return len(self._raw_tokens) > 0

    def advance(self):
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

    def identifier(self) -> Identifier:
        """Return the current token as an Identifier."""
        if isinstance(self.token, Identifier):
            return self.token
        raise RuntimeError("Current token is not an Identifier.")

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
        return self.token in PRIMITIVE_TYPE or isinstance(self.token, Identifier)

    def token_is_constant(self) -> bool:
        """Return True if token is any kind of constant."""
        return isinstance(self.token, (IntegerConstant, StringConstant)) or self.token in KEYWORD_CONSTANTS

    def var_type(self) -> VarT:
        """
        Map a Keyword to a VariableKind.
        note: Argument is excluded because it is not a keyword.
        """
        if isinstance(self.token, Identifier):
            return self.token
        match self.token:
            case Keyword.INT:
                return PrimitiveType.INT
            case Keyword.CHAR:
                return PrimitiveType.CHAR
            case Keyword.BOOLEAN:
                return PrimitiveType.BOOLEAN
            case _:
                raise ValueError(f"Cannot get VariableType from {self.token}.")

    def var_kind(self) -> VariableKind:
        """
        Map a Keyword to a VariableKind.
        note: Argument is excluded because it is not a keyword.
        """
        match self.token:
            case Keyword.VAR:
                return VariableKind.VAR
            case Keyword.STATIC:
                return VariableKind.STATIC
            case Keyword.FIELD:
                return VariableKind.FIELD
            case _:
                raise ValueError(f"Cannot get VariableKind from {self.token}.")

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
    
# Note: Peek method is added to the API for looking the next token without consuming it.
# The remaining method in the API are substituted by the token data structure itself.