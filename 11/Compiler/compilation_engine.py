"""
compilation_engine.py

This module implements the CompilationEngine for the Jack Analyzer project in nand2tetris.
It parses Jack source code according to the Jack grammar and generates the corresponding output,
serving as the core of the Jack compiler's syntax analysis phase.
"""

from contextlib import contextmanager

from jack_tokenizer import JackTokenizer
from tokens.token import Keyword, Symbol, TokenType,Token
from tokens.identifier import IdentifierContext as IdContext
from tokens.identifier import IdentifierCategory as IdCat
from symbol_table import SymbolTable
from typing import TextIO
from tokens.identifier import VariableScope as VarS

class CompilationEngine:
    '''Builds the XML representation of the Jack program.
    It has a compile method for 15 of the 21 non-terminal rules of the Jack grammar
    '''
    def __init__(self, tokenizer: JackTokenizer, output_file: str):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.ident = 0
        self.table: SymbolTable
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
                self._compile_enumtoken(Keyword.CLASS)
                self.table = SymbolTable(name=self.token.value)
                self._compile_identifier(IdContext(IdCat.CLASS, is_def=True))
                with self._braces():
                    while self.token.is_in([Keyword.STATIC, Keyword.FIELD]):
                        self.compile_class_var_declaration()
                    while self.token.is_subroutine():
                        self.compile_subroutine_declaration()
            if self.tokenizer.has_more_tokens():
                raise ValueError("Extra tokens after class end")


    def compile_class_var_declaration(self) -> None:
        '''
        Compile a static variable declaration, or a field declaration.
        grammar: (static | field) type varName (',' varName)* ';'
        '''
        var_scope = self.token.get_variable_scope()
        with self.tag('classVarDec'):
            self._compile()  # 'static' | 'field'
            var_type = self._compile_type()  # type
            self._compile_variable_def(var_scope, var_type)
            while self.token == Symbol.COMMA:
                self._compile()
                self._compile_variable_def(var_scope, var_type)
            self._compile_enumtoken(Symbol.SEMICOLON)

    def compile_subroutine_declaration(self) -> None:
        '''
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        '''
        with self.tag('subroutineDec'):
            self.table.start_subroutine()
            if self.token == Keyword.METHOD:
                # Implicit 'this' argument for methods
                self.table.define('this', self.table.name, VarS.ARGUMENT)
            self._compile()  # 'constructor' | 'function' | 'method'
            self._compile_return_type()
            self._compile_identifier(IdContext(IdCat.SUBROUTINE, is_def=True))
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
                self._compile_variable_def(scope=VarS.ARGUMENT)
                while self.token == Symbol.COMMA:  # (',' type varName)*)?
                    self._compile()
                    self._compile_variable_def(scope=VarS.ARGUMENT)

    def compile_subroutine_body(self) -> None:
        '''
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        '''
        with self.tag('subroutineBody'):
            with self._braces():
                while self.token == Keyword.VAR:
                    self.compile_var_declaration()
                self.compile_statements()

    def compile_var_declaration(self) -> None:
        '''
        Compile a variable declaration
        grammar: 'var' type varName (',' varName)* ';'
        '''
        with self.tag('varDec'):
            self._compile()  # 'var'
            if self.token.is_type():  # type
                var_type = self._compile_type()
                self._compile_variable_def(VarS.VAR, var_type)
                #self._compile_identifier()  # varName
                while self.token == Symbol.COMMA:  # (',' varName)*?
                    self._compile()
                    self._compile_variable_def(VarS.VAR, var_type)  # varName
                self._compile_enumtoken(Symbol.SEMICOLON)

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
            self._compile_enumtoken(Keyword.LET)
            self._compile_variable(var_name=self.token.value,is_def=False)
            if self.token == Symbol.LBRACK:
                with self._brackets():
                    self.compile_expression()
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
            with self._parentheses():
                self.compile_expression()
            with self._braces():
                self.compile_statements()
            if self.token == Keyword.ELSE:
                self._compile_enumtoken(Keyword.ELSE)
                with self._braces():
                    self.compile_statements()

    def compile_while(self) -> None:
        '''
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        '''
        with self.tag('whileStatement'):
            self._compile_enumtoken(Keyword.WHILE)
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
            self._compile_enumtoken(Keyword.DO)
            self._compile_subroutine_call(self.tokenizer.peek())
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
                self._compile()
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
                self._compile()
            elif self.token.ttype == TokenType.IDENTIFIER:
                next_token = self.tokenizer.peek()
                if next_token == Symbol.LBRACK:
                    self._compile_variable(var_name=self.token.value, is_def=False)
                    with self._brackets():
                        self.compile_expression()
                elif next_token.is_in([Symbol.LPAREN, Symbol.DOT]):
                    self._compile_subroutine_call(next_token)
                else:
                    self._compile_variable(var_name=self.token.value, is_def=False)
            elif self.token == Symbol.LPAREN:
                with self._parentheses():
                    self.compile_expression()
            elif self.token.is_unary_op():
                self._compile()
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

    def _compile_return_type(self):
        if self.token == Keyword.VOID:
            self._compile()
        else:
            self._compile_type()

    def _compile_subroutine_call(self, next_token: Token) -> None:
        '''
        Compile a subroutine call.
        grammar: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList  ')'
        '''
        if next_token == Symbol.DOT:
            if self.table.get_symbol(self.token.value) is None:
                self._compile_identifier(IdContext(IdCat.CLASS, is_def=False))
            else:
                self._compile_variable(var_name=self.token.value, is_def=False)
            self._compile_enumtoken(Symbol.DOT)
        self._compile_identifier(IdContext(IdCat.SUBROUTINE, is_def=False)) # subroutineName | className | varName
        with self._parentheses():
            self.compile_expression_list()

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
        self._compile_enumtoken(open_symbol)
        yield
        self._compile_enumtoken(close_symbol)

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

    def _compile(self) -> None:
        self._write_token()
        if self.tokenizer.has_more_tokens():
            self.token = self.tokenizer.advance()

    def _compile_enumtoken(self, token: Keyword | Symbol) -> None:
        '''
        Compile a keyword or symbol
        grammar: keyword | symbol
        '''
        if self.token == token:
            self._compile()
        else:
            raise ValueError(f"Expected {token.ttype}: '{token}'")

    def _compile_identifier(self,context: IdContext ) -> None: #
        '''
        Compile an identifier
        grammar: varName
        '''
        if self.token.ttype == TokenType.IDENTIFIER:
            self.token.set_context(context)
            self._compile()
        else:
            raise ValueError(f"Expected an identifier")

    def _compile_type(self) -> str:
        '''
        Compile a type
        grammar: 'int' | 'char' | 'boolean' | className
        '''
        var_type = self.token.value
        if self.token.ttype == TokenType.IDENTIFIER:
            self._compile_identifier(IdContext(IdCat.CLASS,is_def=False))
        elif self.token.is_primitive_type():
            self._compile()
        else:
            raise ValueError("Expected type to be 'int', 'char', 'boolean', or className")
        return var_type

    def _compile_variable_def(self, scope: VarS, var_type: str|None=None) -> None:
        '''
        Compile a variable
        grammar: (type) varName
        '''
        if var_type is None:
            var_type = self._compile_type()
        var_name = self.token.value
        self.table.define(var_name, var_type, scope)
        self._compile_variable(var_name, is_def=True)

    def _compile_variable(self, var_name: str, is_def: bool) -> None:
        '''
        Compile a variable
        grammar: varName
        '''
        symbol = self.table.get_symbol(var_name)
        if symbol is None:
            raise ValueError(f"Identifier '{var_name}' not found in symbol table.")
        id_context = IdContext(IdCat.VARIABLE, is_def=is_def, scope=symbol.kind, index=symbol.index)
        self._compile_identifier(id_context)


# Note: The following rules in the Jack grammar have no corresponding compile_xxx methods:
# - type
# - className
# - subroutineName
# - variableName
# - statement
# - subroutineCall
# The parsing logic of these rules is handled by the rules that invoke them.