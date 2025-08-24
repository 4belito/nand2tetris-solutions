
import re
from jack_tokens import Token,Symbol,TokenType,Keyword

class JackTokenizer:
    def __init__(self, input_file):
        with open(input_file, "r") as f:
            text = f.read()
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL) #clean block comments
        text = re.sub(r'//.*?\n', '', text, flags=re.DOTALL) #clean line comments
        pattern = r'([' + re.escape(''.join(Symbol.values())) + r'])|\s+'
        self.raw_tokens = [p for p in re.split(pattern, text) if p]
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
        raw_token = self.raw_tokens[self.next_i]
        self.current_token = Token(raw_token)
        self.next_i += 1
        

    def token_type(self) -> TokenType:
        ''' Return the type of the current token, as a constant. '''
        if self.current_token is not None:
            return self.current_token.type()
        raise ValueError("No current token")

    def keyword(self) -> str:
        ''' 
        Returns the keyword which is the current token as a constant.
        This method should be called only if token_type() is KEYWORD.
        '''
        if self.token_type() == TokenType.KEYWORD:
            return self.current_token.value
        raise ValueError("Current token is not a keyword")

    def symbol(self) -> str:
        '''
        Returns the character which is the current token.
        Should be called only if token_type() is SYMBOL.
        '''
        if self.token_type() == TokenType.SYMBOL:
            return self.current_token.value
        raise ValueError("Current token is not a symbol")

    def identifier(self) -> str:
        '''
        Returns the identifier which is the current token.
        Should be called only if token_type() is IDENTIFIER.
        '''
        if self.token_type() == TokenType.IDENTIFIER:
            return self.current_token.value
        else:
            raise ValueError("Current token is not an identifier")

    def int_val(self) -> int:
        '''
        Returns the integer value of the current token.
        Should be called only if token_type() is INT_CONST.
        '''
        if self.token_type() == TokenType.INT_CONST:
            return self.current_token.value
        else:
            raise ValueError("Current token is not an integer constant")
        
    def string_val(self) -> str:
        '''
        Returns the string value of the current token, without the two enclosing double quotes.
        Should be called only if token_type() is STRING_CONST.
        '''
        if self.token_type() == TokenType.STRING_CONST:
            return self.current_token.value
        else:
            raise ValueError("Current token is not a string constant")
