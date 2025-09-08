"""JackTokenizer module: Provides functionality to tokenize Jack source code.

This module defines the JackTokenizer class, which reads Jack source files,
removes comments, splits the code into raw tokens, and provides access to
individual tokens for further parsing and analysis.
"""

import re
from collections import deque
from jack_tokens import Token, Symbol

class JackTokenizer:
    """Tokenizes Jack source code and provides access to tokens."""

    def __init__(self, input_file: str):
        """Initialize tokenizer from a Jack source file."""
        try:
            with open(input_file, "r") as f:
                text = f.read()
        except OSError as e:
            raise RuntimeError(f"Failed to open {input_file}: {e}")
        # Use deque for efficient left pops
        self.raw_tokens: deque[str] = deque(JackTokenizer.tokenize_raw(text))

    def has_more_tokens(self) -> bool:
        """Return True if there are more tokens to process."""
        return len(self.raw_tokens) > 0

    def advance(self) -> Token:
        '''
        Get the next token from the input, and makes it the current token.
        This method should be called only if has_more_tokens() is true.
        Initially there is not current token.
        '''
        if self.has_more_tokens():
            raw_token = self.raw_tokens.popleft()
            return Token(raw_token)
        raise RuntimeError("No more tokens available to advance.")

    def peek(self) -> Token:
        """Return the next token object without removing it."""
        if self.has_more_tokens():
            raw_token = self.raw_tokens[0]
            return Token(raw_token)
        raise RuntimeError("No more tokens available to peek.")


    @staticmethod
    def tokenize_raw(text: str) -> list[str]:
        """
        Perform raw tokenization of Jack source code and return a list of tokens.
        Removes comments and splits by symbols, string constants, and whitespace.

        Regex pattern explanation:
        - Matches Jack symbols (from Symbol enum)
        - Matches string constants (quoted strings)
        - Splits on whitespace
        """
        # Remove block comments (/* ... */) and line comments (// ...)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'//.*?\n', '', text, flags=re.DOTALL)
        # Regex pattern: match symbols, string constants, or whitespace
        string_pattern = r'"[^"\n]*"'
        pattern = r'([' + re.escape(''.join(Symbol.values())) + r'])|(' + string_pattern + r')|\s+'
        # Split and filter out empty strings
        raw_tokens = [p for p in re.split(pattern, text) if p]
        return raw_tokens

# Note: Peek method is added to the API for looking the next token without consuming it.
# The remaining method in the API are substituted by the token data structure itself.