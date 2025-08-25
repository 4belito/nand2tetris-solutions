from contextlib import contextmanager

from jack_tokenizer import JackTokenizer
from jack_tokens import Keyword, Symbol, TokenType, Token


class CompilationEngine:
    '''Builds the XML representation of the Jack program.
    It has a compile method for 15 of the 21 non-terminal rules of the Jack grammar
    '''
    def __init__(self, tokenizer: JackTokenizer, output_file: str):
        self.tokenizer= tokenizer
        self.output_file = output_file
        self.token = None
        self.f = None
        self.ident = 0


    def compile_class(self) -> None:
        '''
        Compile a complete class
        grammar: 'class' className '{' classVarDec* subroutineDec* '}'
        '''
        with open(self.output_file, 'w') as self.f:
            self.token = self.tokenizer.advance()  # 'class'
            with self.tag('class'):
                self._compile_enumtoken(Keyword.CLASS)
                self._compile_identifier()
                self._compile_enumtoken(Symbol.LBRACE)
                if self.token in (Keyword.STATIC, Keyword.FIELD):
                    while self.token in (Keyword.STATIC, Keyword.FIELD):
                        self.compile_class_var_dec()
                if self.token.is_subroutine():
                    while self.token.is_subroutine():
                        self.compile_subroutine_dec()
                if self.token == Symbol.RBRACE:
                    self._write_token()
            if self.tokenizer.has_more_tokens():
                raise ValueError("Extra tokens after class declaration")
                
            

    def compile_class_var_dec(self) -> None:
        '''
        Compile a static variable declaration, or a field declaration.
        grammar: (static | field) type varName (',' varName)* ';'
        '''
        with self.tag('classVarDec'):
            self._write_and_advance()  # 'static' | 'field'
            self._compile_type()
            self._compile_identifier()
            while self.token == Symbol.COMMA:
                self._write_and_advance()
                self._compile_identifier()
            self._compile_enumtoken(Symbol.SEMICOLON)

    def compile_subroutine_dec(self) -> None:
        '''
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        '''
        with self.tag('subroutineDec'):
            self._write_and_advance()  # 'constructor' | 'function' | 'method'
            self._compile_return_type()
            self._compile_enumtoken(Symbol.LPAREN)
            self.compile_parameter_list()
            self._compile_enumtoken(Symbol.RPAREN)
            self.compile_subroutine_body()

    def compile_parameter_list(self) -> None:
        '''
        Compile a (possibly empty) parameter list.
        Does not handle the enclosing parentheses ().
        grammar: ((type varName) (',' type varName)*)?
        '''
        with self.tag('parameterList'):
            if self.token.is_type():  # type
                self._write_and_advance()
                self._compile_identifier()
                while self.token == Symbol.COMMA:  # (',' type varName)*)?
                    self._write_and_advance()
                    self._compile_type()
                    self._compile_identifier()

    def compile_subroutine_body(self) -> None:
        '''
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        '''
        with self.tag('subroutineBody'):
            self._compile_enumtoken(Symbol.LBRACE)
            while self.token == Keyword.VAR:
                self.compile_var_dec()
            self.compile_statements()
            self._compile_enumtoken(Symbol.RBRACE)

    def compile_var_dec(self) -> None:
        '''
        Compile a variable declaration
        grammar: 'var' type varName (',' varName)* ';'
        '''
        with self.tag('varDec'):
            self._write_and_advance()  # 'var'
            if self.token.is_type():  # type
                self._write_and_advance()
                self._compile_identifier()  # varName
                while self.token == Symbol.COMMA:  # (',' varName)*?
                    self._write_and_advance()
                    self._compile_identifier()  # varName
                self._compile_enumtoken(Symbol.SEMICOLON)

    def compile_statements(self) -> None:
        '''
        Compile a sequence of statements.
        Does not handle the enclosing braces {}.
        grammar: statement*
        '''
        with self.tag('statements'):
            while self.token.is_statement():
                match self.token:
                    case Keyword.LET:
                        self.compile_let()
                    case Keyword.IF:
                        self.compile_if()
                    case Keyword.WHILE:
                        self.compile_while()
                    case Keyword.DO:
                        self.compile_do()
                    case Keyword.RETURN:
                        self.compile_return()

    def compile_let(self) -> None:
        '''
        Compile a let statement.
        grammar: 'let' varName('[' expression ']')? '=' expression ';'
        '''
        with self.tag('letStatement'):
            self._compile_enumtoken(Keyword.LET)
            self._compile_identifier()
            if self.token == Symbol.LBRACK:
                self._compile_enumtoken(Symbol.LBRACK)
                self.compile_expression()
                self._compile_enumtoken(Symbol.RBRACK)
            self._compile_enumtoken(Symbol.EQ)
            self.compile_expression()
            self._compile_enumtoken(Symbol.SEMICOLON)

    def compile_if(self) -> None:
        '''
        Compile an if statement, possibly with a trailing else clause.
        grammar: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        '''
        with self.tag('ifStatement'):
            self._compile_enumtoken(Keyword.IF)
            self._compile_enumtoken(Symbol.LPAREN)
            self.compile_expression()
            self._compile_enumtoken(Symbol.RPAREN)
            self._compile_enumtoken(Symbol.LBRACE)
            self.compile_statements()
            self._compile_enumtoken(Symbol.RBRACE)
            if self.token == Keyword.ELSE:
                self._compile_enumtoken(Keyword.ELSE)
                self._compile_enumtoken(Symbol.LBRACE)
                self.compile_statements()
                self._compile_enumtoken(Symbol.RBRACE)

    def compile_while(self) -> None:
        '''
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        '''
        with self.tag('whileStatement'):
            self._compile_enumtoken(Keyword.WHILE)
            self._compile_enumtoken(Symbol.LPAREN)
            self.compile_expression()
            self._compile_enumtoken(Symbol.RPAREN)
            self._compile_enumtoken(Symbol.LBRACE)
            self.compile_statements()
            self._compile_enumtoken(Symbol.RBRACE)

    def compile_do(self) -> None:
        '''
        Compile a do statement.
        grammar: 'do' subroutineCall  ';'
        '''
        with self.tag('doStatement'):
            self._compile_enumtoken(Keyword.DO)
            self._compile_subroutine_call()
            self._compile_enumtoken(Symbol.SEMICOLON)

    def compile_return(self) -> None:
        '''
        Compile a return statement.
        grammar: 'return' expression? ';'
        '''
        with self.tag('returnStatement'):
            self._compile_enumtoken(Keyword.RETURN)
            if self.token != Symbol.SEMICOLON:
                self.compile_expression()
            self._compile_enumtoken(Symbol.SEMICOLON)

    def compile_expression(self) -> None:
        '''
        Compile an expression.
        grammar: term (op term)*
        '''
        with self.tag('expression'):
            self.compile_term()
            while self.token.is_op():
                self._compile_enumtoken(self.token)
                self.compile_term()

    def compile_term(self) -> None:
        '''
        Compile a term. 
        If the current token is an identifier, the routine must distinguish 
        between a variable, an array entry, or a subroutine call.
        A single look-ahead token which may be one of: "[" "(" or ".", suffices to
        distinguish between the possibilities. Any other token is not part of this term 
        and should be advanced over.
        grammar: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        '''
        with self.tag('term'):
            if self.token.is_constant():
                self._write_and_advance()
            elif self.token.ttype == TokenType.IDENTIFIER:
                next_token = self.tokenizer.peek()
                if next_token == Symbol.LBRACK:
                    self._compile_identifier()
                    self._compile_enumtoken(Symbol.LBRACK)
                    self.compile_expression()
                    self._compile_enumtoken(Symbol.RBRACK)
                elif next_token in (Symbol.LPAREN, Symbol.DOT):
                    self._compile_subroutine_call()
                else:
                    self._compile_identifier()
            elif self.token == Symbol.LPAREN:
                self._compile_enumtoken(Symbol.LPAREN)
                self.compile_expression()
                self._compile_enumtoken(Symbol.RPAREN)
            elif self.token.is_unary_op():
                self._compile_enumtoken(self.token)
                self.compile_term()

    def compile_expression_list(self) -> None:
        '''
        Compile a (possibly empty) comma-separated list of expressions.
        grammar: (expression (',' expression)*)?
        '''
        with self.tag('expressionList'):
            if self.token != Symbol.RPAREN:
                self.compile_expression()
                while self.token == Symbol.COMMA:
                    self._compile_enumtoken(Symbol.COMMA)
                    self.compile_expression()

    def _compile_return_type(self) -> None:
        if self.token == Keyword.VOID or self.token.ttype == TokenType.IDENTIFIER:
            self._write_and_advance()
            self._compile_identifier()
        else:
            raise ValueError("Expected 'void' or 'type' after subroutine keyword")

    def _compile_subroutine_call(self) -> None:
        '''
        Compile a subroutine call.
        grammar: subroutineName '(' expressionList ')'| (className | varName) '.' subroutineName '(' expressionList  ')'
        '''
        self._compile_identifier()  # subroutineName | className | varName
        if self.token == Symbol.LPAREN:
            self._compile_enumtoken(Symbol.LPAREN)
            self.compile_expression_list()
            self._compile_enumtoken(Symbol.RPAREN)
        elif self.token == Symbol.DOT:
            self._compile_enumtoken(Symbol.DOT)
            self._compile_identifier()  # subroutineName
            self._compile_enumtoken(Symbol.LPAREN)
            self.compile_expression_list()
            self._compile_enumtoken(Symbol.RPAREN)

    def _open_tag(self, tag_name: str) -> None:
        self._write(f'<{tag_name}>\n')
        self.ident += 2

    def _close_tag(self, tag_name: str) -> None:
        self.ident -= 2
        self._write(f'</{tag_name}>\n')

    @contextmanager
    def tag(self, tag_name: str):
        self._open_tag(tag_name)
        yield
        self._close_tag(tag_name)

    def _write(self, text: str) -> None:
        self.f.write(f'{" " * self.ident}{text}')

    def _write_token(self) -> None:
        self._write(self.token.xml())

    def _write_and_advance(self) -> None:
        self._write_token()
        self.token = self.tokenizer.advance()

    def _compile_enumtoken(self, token: Keyword | Symbol) -> None:
        '''
        Compile a keyword or symbol
        grammar: keyword | symbol
        '''
        if self.token == token:
            self._write_and_advance()
        else:
            raise ValueError(f"Expected {token.ttype}: '{token}'")

    def _compile_identifier(self) -> None:
        '''
        Compile an identifier
        grammar: varName
        '''
        if self.token.ttype == TokenType.IDENTIFIER:
            self._write_and_advance()
        else:
            raise ValueError(f"Expected an identifier")

    def _compile_type(self) -> None:
        '''
        Compile a type
        grammar: 'int' | 'char' | 'boolean' | className
        '''
        if self.token.is_type():
            self._write_and_advance()
        else:
            raise ValueError("Expected type to be 'int', 'char', 'boolean', or className")





# Note: The following rules in the Jack grammar have no corresponding compile_xxx methods:
# - type
# - className
# - subroutineName
# - variableName
# - statement
# - subroutineCall
# The parsing logic of these rules is handled by the rules that invoke them.