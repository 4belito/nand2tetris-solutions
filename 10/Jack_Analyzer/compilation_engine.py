"""
compilation_engine.py

This module implements the CompilationEngine for the Jack Analyzer project in nand2tetris.
It parses Jack source code according to the Jack grammar and generates the corresponding output,
serving as the core of the Jack compiler's syntax analysis phase.
"""

from contextlib import contextmanager

from jack_tokenizer import JackTokenizer
from jack_tokens import Keyword, Symbol, TokenType,Token, UNARY_OPS, BINARY_OPS,SUBROUTINES,PRIMITIVE_TYPE
from typing import TextIO

class CompilationEngine:
    '''Builds the XML representation of the Jack program.
    It has a compile method for 15 of the 21 non-terminal rules of the Jack grammar
    '''
    def __init__(self, input_file: str, output_file: str):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = output_file
        self.ident = 0
        self.token: Token
        self.f: TextIO

    def compile_class(self) -> None:
        '''
        Compile a complete class
        grammar: 'class' className '{' classVarDec* subroutineDec* '}'
        '''
        with open(self.output_file, 'w') as self.f:
            self.token = self.tokenizer.advance()
            with self.tag('class'):
                self._consume(Keyword.CLASS)
                self._consume(TokenType.IDENTIFIER)
                with self._braces():
                    while self.token.is_in([Keyword.STATIC, Keyword.FIELD]):
                        self.compile_class_var_dec()
                    while self.token.is_in(SUBROUTINES):
                        self.compile_subroutine_dec()
            if self.tokenizer.has_more_tokens():
                raise ValueError("Extra tokens after class end")

    def compile_class_var_dec(self) -> None:
        '''
        Compile a static variable declaration, or a field declaration.
        grammar: (static | field) type varName (',' varName)* ';'
        '''
        with self.tag('classVarDec'):
            self._consume(Keyword.STATIC, Keyword.FIELD)
            self._compile_variable_def()
            while self.token == Symbol.COMMA:
                self._consume()
                self._consume(TokenType.IDENTIFIER)
            self._consume(Symbol.SEMICOLON)

    def compile_subroutine_dec(self) -> None:
        '''
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        '''
        with self.tag('subroutineDec'):
            self._consume(*SUBROUTINES)
            self._consume(Keyword.VOID,*PRIMITIVE_TYPE, TokenType.IDENTIFIER)
            self._consume(TokenType.IDENTIFIER)
            with self._parentheses():
                self.compile_parameter_list()
            self.compile_subroutine_body()

    def compile_parameter_list(self) -> None:
        '''
        Compile a (possibly empty) parameter list.
        Does not handle the enclosing parentheses ().
        grammar: ((type varName) (',' type varName)*)?
        '''
        with self.tag('parameterList'):
            if self.token.is_type(): 
                self._compile_variable_def()
                while self.token == Symbol.COMMA:  # (',' type varName)*)?
                    self._consume()
                    self._compile_variable_def()

    def compile_subroutine_body(self) -> None:
        '''
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        '''
        with self.tag('subroutineBody'):
            with self._braces():
                while self.token == Keyword.VAR:
                    self.compile_var_dec()
                self.compile_statements()

    def compile_var_dec(self) -> None:
        '''
        Compile a variable declaration
        grammar: 'var' type varName (',' varName)* ';'
        '''
        with self.tag('varDec'):
            self._consume(Keyword.VAR)  # 'var'
            if self.token.is_type():  # type
                self._consume(*PRIMITIVE_TYPE, TokenType.IDENTIFIER)
                self._consume(TokenType.IDENTIFIER)  # varName
                while self.token == Symbol.COMMA:  # (',' varName)*?
                    self._consume()
                    self._consume(TokenType.IDENTIFIER)  # varName
                self._consume(Symbol.SEMICOLON)

    def compile_statements(self) -> None:
        '''
        Compile a sequence of statements.
        Does not handle the enclosing braces {}.
        grammar: statement*
        '''
        with self.tag('statements'):
            while True:
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
                    case _:
                        break

    def compile_let(self) -> None:
        '''
        Compile a let statement.
        grammar: 'let' varName('[' expression ']')? '=' expression ';'
        '''
        with self.tag('letStatement'):
            self._consume(Keyword.LET)
            self._consume(TokenType.IDENTIFIER)
            if self.token == Symbol.LBRACK:
                with self._brackets():
                    self.compile_expression()
            self._consume(Symbol.EQ)
            self.compile_expression()
            self._consume(Symbol.SEMICOLON)

    def compile_if(self) -> None:
        '''
        Compile an if statement, possibly with a trailing else clause.
        grammar: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        '''
        with self.tag('ifStatement'):
            self._consume(Keyword.IF)
            with self._parentheses():
                self.compile_expression()
            with self._braces():
                self.compile_statements()
            if self.token == Keyword.ELSE:
                self._consume()
                with self._braces():
                    self.compile_statements()

    def compile_while(self) -> None:
        '''
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        '''
        with self.tag('whileStatement'):
            self._consume(Keyword.WHILE)
            with self._parentheses():
                self.compile_expression()
            with self._braces():
                self.compile_statements()

    def compile_do(self) -> None:
        '''
        Compile a do statement.
        grammar: 'do' subroutineCall  ';'
        '''
        with self.tag('doStatement'):
            self._consume(Keyword.DO)
            self.compile_subroutine_call()
            self._consume(Symbol.SEMICOLON)

    def compile_return(self) -> None:
        '''
        Compile a return statement.
        grammar: 'return' expression? ';'
        '''
        with self.tag('returnStatement'):
            self._consume(Keyword.RETURN)
            if self.token != Symbol.SEMICOLON:
                self.compile_expression()
            self._consume(Symbol.SEMICOLON)

    def compile_expression(self) -> None:
        '''
        Compile an expression.
        grammar: term (op term)*
        '''
        with self.tag('expression'):
            self.compile_term()
            while self.token.is_in(BINARY_OPS):
                self._consume()
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
                self._consume()
            elif self.token.ttype == TokenType.IDENTIFIER:
                next_token = self.tokenizer.peek()
                if next_token == Symbol.LBRACK:
                    self._consume(TokenType.IDENTIFIER)
                    with self._brackets():
                        self.compile_expression()
                elif next_token.is_in([Symbol.LPAREN, Symbol.DOT]):
                    self.compile_subroutine_call()
                else:
                    self._consume(TokenType.IDENTIFIER)
            elif self.token == Symbol.LPAREN:
                with self._parentheses():
                    self.compile_expression()
            elif self.token.is_in(UNARY_OPS):
                self._consume()
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
                    self._consume()
                    self.compile_expression()

    def compile_subroutine_call(self) -> None:
        '''
        Compile a subroutine call.
        grammar: subroutineName '(' expressionList ')'| (className | varName) '.' subroutineName '(' expressionList  ')'
        '''
        self._consume(TokenType.IDENTIFIER)  # subroutineName | className | varName
        if self.token == Symbol.LPAREN:
            with self._parentheses():
                self.compile_expression_list()
        elif self.token == Symbol.DOT:
            self._consume()
            self._consume(TokenType.IDENTIFIER)  # subroutineName
            with self._parentheses():
                self.compile_expression_list()
    
    # ----------------------------------------
    # Private Parsing Helpers (token handling)
    # ----------------------------------------
       
    def _compile_variable_def(self) -> None:
        '''
        Compile a variable definition
        grammar: type varName
        '''
        self._consume(*PRIMITIVE_TYPE, TokenType.IDENTIFIER)
        self._consume(TokenType.IDENTIFIER)

    def _consume(self, *tokens: Keyword | Symbol | TokenType) -> None:
        '''
        Compile the current token, and advance to the next token.
        If the current token is not one of the given tokens, raise an error.
        '''
        if not tokens or any(self.token == t or self.token.ttype == t for t in tokens):
            self._write_token()
            if self.tokenizer.has_more_tokens():
                self.token = self.tokenizer.advance()
        else:
            expected = ', '.join(str(t) for t in tokens)
            raise ValueError(f"Expected one of: {expected}, got: '{self.token}'")
        
    # ------------------------------------------------------------
    # Output and XML/context management helper methods (private)
    # ------------------------------------------------------------

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

    @contextmanager
    def _symbol_context(self, open_symbol: Symbol, close_symbol: Symbol):
        self._consume(open_symbol)
        yield
        self._consume(close_symbol)

    def _braces(self):
        return self._symbol_context(Symbol.LBRACE, Symbol.RBRACE)

    def _parentheses(self):
        return self._symbol_context(Symbol.LPAREN, Symbol.RPAREN)

    def _brackets(self):
        return self._symbol_context(Symbol.LBRACK, Symbol.RBRACK)

    def _write(self, text: str) -> None:
        self.f.write(f'{" " * self.ident}{text}')

    def _write_token(self) -> None:
        self._write(self.token.xml())


# Note: The following rules in the Jack grammar have no corresponding compile_xxx methods:
# - type
# - className
# - subroutineName
# - variableName
# - statement
# The parsing logic of these rules is handled by the rules that invoke them. 
# In the course SubroutineCall is included in this list in the 