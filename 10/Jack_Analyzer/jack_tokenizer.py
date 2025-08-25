
import re
from jack_tokens import Token,Symbol,TokenType

class JackTokenizer:
    def __init__(self, input_file):
        with open(input_file, "r") as f:
            text = f.read()
        self.raw_tokens = JackTokenizer.tokenize_raw(text)
        self.n_tokens = len(self.raw_tokens)
        self.next_i = 0
        self.current_token: Token|None = None

    def has_more_tokens(self) -> bool:
        # Are there more tokens in the input?
        return self.next_i < self.n_tokens

    def advance(self):
        '''
        Get the next token from the input, and makes it the current token.
        This method should be called only if has_more_tokens() is true.
        Initially there is not current token.
        '''
        self.current_token = self.next_token()
        self.next_i += 1
        return self.current_token
    
    def next_token(self):
        raw_token = self.raw_tokens[self.next_i]
        return Token(raw_token)


    @staticmethod
    def tokenize_raw(text: str):
        '''
        Performs raw tokenization of Jack source code and returns a list of tokens.
        Removes comments and splits by symbols, string constants, and whitespace.
        '''
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL) #clean block comments
        text = re.sub(r'//.*?\n', '', text, flags=re.DOTALL) #clean line comments
        string_pattern = r'"[^"\n]*"'
        pattern = r'([' + re.escape(''.join(Symbol.values())) + r'])|(' + string_pattern + r')|\s+'
        raw_tokens = [p for p in re.split(pattern, text) if p]
        return raw_tokens