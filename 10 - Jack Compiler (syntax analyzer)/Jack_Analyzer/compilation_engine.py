"""
compilation_engine.py

This module implements the CompilationEngine for the Jack Analyzer project in nand2tetris.
It parses Jack source code according to the Jack grammar and generates the corresponding output,
serving as the core of the Jack _compiler's syntax analysis phase.
"""

from contextlib import contextmanager

from jack_tokenizer import JackTokenizer, Token
from tokens.enums import Keyword, Symbol, UNARY_OPS, BINARY_OPS, SUBROUTINES, PRIMITIVE_TYPES
from tokens.identifier import Identifier
from typing import TextIO


class CompilationEngine:
    """
    Builds the XML representation of the Jack program.
    It has a _compile method for 15 of the 21 non-terminal rules of the Jack grammar
    """

    ident_step = 2

    def __init__(self, input_file: str, output_file: str):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = output_file
        self.ident = 0
        self.f: TextIO

    # ----------------------------------------
    # Compilation Methods
    # ----------------------------------------

    def compile_class(self) -> None:
        """
        Compile a complete class
        grammar: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        with open(self.output_file, "w") as self.f:
            with self.tag("class"):
                self._consume(Keyword.CLASS)
                self._consume(Identifier)
                with self._braces():
                    while self.token in [Keyword.STATIC, Keyword.FIELD]:
                        self._compile_class_var_dec()
                    while self.token in SUBROUTINES:
                        self._compile_subroutine_dec()
            if self.tokenizer.has_more_tokens():
                raise ValueError("Extra tokens after class end")

    def _compile_class_var_dec(self) -> None:
        """
        Compile a static variable declaration, or a field declaration.
        grammar: (static | field) type varName (',' varName)* ';'
        """
        with self.tag("classVarDec"):
            self._consume(Keyword.STATIC, Keyword.FIELD)
            self._compile_variable_def()
            while self.token == Symbol.COMMA:
                self._consume()
                self._consume(Identifier)
            self._consume(Symbol.SEMICOLON)

    def _compile_subroutine_dec(self) -> None:
        """
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        """
        with self.tag("subroutineDec"):
            self._consume(*SUBROUTINES)
            self._consume(Keyword.VOID, *PRIMITIVE_TYPES, Identifier)
            self._consume(Identifier)
            with self._parentheses():
                self._compile_parameter_list()
            self._compile_subroutine_body()

    def _compile_parameter_list(self) -> None:
        """
        Compile a (possibly empty) parameter list.
        Does not handle the enclosing parentheses ().
        grammar: ((type varName) (',' type varName)*)?
        """
        with self.tag("parameterList"):
            if self.tokenizer.token_is_var_type():
                self._compile_variable_def()
                while self.token == Symbol.COMMA:  # (',' type varName)*)?
                    self._consume()
                    self._compile_variable_def()

    def _compile_subroutine_body(self) -> None:
        """
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        """
        with self.tag("subroutineBody"):
            with self._braces():
                while self.token == Keyword.VAR:
                    self._compile_var_dec()
                self._compile_statements()

    def _compile_var_dec(self) -> None:
        """
        Compile a variable declaration
        grammar: 'var' type varName (',' varName)* ';'
        """
        with self.tag("varDec"):
            self._consume(Keyword.VAR)  # 'var'
            if self.tokenizer.token_is_var_type():  # type
                self._consume(*PRIMITIVE_TYPES, Identifier)
                self._consume(Identifier)  # varName
                while self.token == Symbol.COMMA:  # (',' varName)*?
                    self._consume()
                    self._consume(Identifier)  # varName
                self._consume(Symbol.SEMICOLON)

    def _compile_statements(self) -> None:
        """
        Compile a sequence of statements.
        Does not handle the enclosing braces {}.
        grammar: statement*
        """
        with self.tag("statements"):
            while True:
                match self.token:
                    case Keyword.LET:
                        self._compile_let()
                    case Keyword.IF:
                        self._compile_if()
                    case Keyword.WHILE:
                        self._compile_while()
                    case Keyword.DO:
                        self._compile_do()
                    case Keyword.RETURN:
                        self._compile_return()
                    case _:
                        break

    def _compile_let(self) -> None:
        """
        Compile a let statement.
        grammar: 'let' varName('[' expression ']')? '=' expression ';'
        """
        with self.tag("letStatement"):
            self._consume(Keyword.LET)
            self._consume(Identifier)
            if self.token == Symbol.LBRACK:
                with self._brackets():
                    self._compile_expression()
            self._consume(Symbol.EQ)
            self._compile_expression()
            self._consume(Symbol.SEMICOLON)

    def _compile_if(self) -> None:
        """
        Compile an if statement, possibly with a trailing else clause.
        grammar: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        with self.tag("ifStatement"):
            self._consume(Keyword.IF)
            with self._parentheses():
                self._compile_expression()
            with self._braces():
                self._compile_statements()
            if self.token == Keyword.ELSE:
                self._consume()
                with self._braces():
                    self._compile_statements()

    def _compile_while(self) -> None:
        """
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        """
        with self.tag("whileStatement"):
            self._consume(Keyword.WHILE)
            with self._parentheses():
                self._compile_expression()
            with self._braces():
                self._compile_statements()

    def _compile_do(self) -> None:
        """
        Compile a do statement.
        grammar: 'do' subroutineCall  ';'
        """
        with self.tag("doStatement"):
            self._consume(Keyword.DO)
            self._compile_subroutine_call()
            self._consume(Symbol.SEMICOLON)

    def _compile_return(self) -> None:
        """
        Compile a return statement.
        grammar: 'return' expression? ';'
        """
        with self.tag("returnStatement"):
            self._consume(Keyword.RETURN)
            if self.token != Symbol.SEMICOLON:
                self._compile_expression()
            self._consume(Symbol.SEMICOLON)

    def _compile_expression(self) -> None:
        """
        Compile an expression.
        grammar: term (op term)*
        """
        with self.tag("expression"):
            self._compile_term()
            while self.token in BINARY_OPS:
                self._consume()
                self._compile_term()

    def _compile_term(self) -> None:
        """
        Compile a term.
        If the current token is an identifier, the routine must distinguish
        between a variable, an array entry, or a subroutine call.
        A single look-ahead token which may be one of: "[" "(" or ".", suffices to
        distinguish between the possibilities. Any other token is not part of this term
        and should be advanced over.
        grammar: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        """
        with self.tag("term"):
            if self.tokenizer.token_is_constant():
                self._consume()
            elif self.token == Symbol.LPAREN:
                with self._parentheses():
                    self._compile_expression()
            elif self.token in UNARY_OPS:
                self._consume()
                self._compile_term()
            elif isinstance(self.token, Identifier):
                next_token = self.tokenizer.peek()
                if next_token == Symbol.LBRACK:
                    self._consume(Identifier)
                    with self._brackets():
                        self._compile_expression()
                elif next_token in [Symbol.LPAREN, Symbol.DOT]:
                    self._compile_subroutine_call()
                else:
                    self._consume(Identifier)

    def _compile_expression_list(self) -> None:
        """
        Compile a (possibly empty) comma-separated list of expressions.
        grammar: (expression (',' expression)*)?
        """
        with self.tag("expressionList"):
            if self.token != Symbol.RPAREN:
                self._compile_expression()
                while self.token == Symbol.COMMA:
                    self._consume()
                    self._compile_expression()

    def _compile_subroutine_call(self) -> None:
        """
        Compile a subroutine call.
        grammar: subroutineName '(' expressionList ')'| (className | varName) '.' subroutineName '(' expressionList  ')'
        """
        self._consume(Identifier)  # subroutineName | className | varName
        if self.token == Symbol.LPAREN:
            with self._parentheses():
                self._compile_expression_list()
        elif self.token == Symbol.DOT:
            self._consume()
            self._consume(Identifier)  # subroutineName
            with self._parentheses():
                self._compile_expression_list()

    def _compile_variable_def(self) -> None:
        """
        Compile a variable definition
        grammar: type varName
        """
        self._consume(*PRIMITIVE_TYPES, Identifier)
        self._consume(Identifier)

    # ----------------------------------------
    # Parsing Helpers (token handling)
    # ----------------------------------------

    def _consume(self, *tokens: Keyword | Symbol | type[Identifier]) -> None:
        """
        Write and advance if the current token matches any of the provided tokens.
        If no tokens are provided, always write and advance.
        """
        if not tokens or any(
            self.token == t or (isinstance(t, type) and isinstance(self.token, t)) for t in tokens
        ):
            self._write_token()
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
        else:
            expected = ", ".join(str(t) for t in tokens)
            raise ValueError(f"Expected one of: {expected}, got: '{self.token}'")

    @property
    def token(self) -> Token:
        """Alias for the current token from the tokenizer."""
        return self.tokenizer.token

    # ------------------------------------------------------------
    # Output and XML/context management helper methods (private)
    # ------------------------------------------------------------

    def _write(self, text: str) -> None:
        """Write text to the output file with current indentation."""
        self.f.write(f'{" " * self.ident}{text}')

    def _write_token(self) -> None:
        """Write the current token in XML format to the output file."""
        s = type(self.token).__name__
        token_type = s[0].lower() + s[1:]
        self._write(f"<{token_type}> {self.token} </{token_type}>\n")

    def _open_tag(self, tag_name: str) -> None:
        """Open an XML tag and increase indentation."""
        self._write(f"<{tag_name}>\n")
        self.ident += 2

    def _close_tag(self, tag_name: str) -> None:
        """Close an XML tag and decrease indentation."""
        self.ident -= 2
        self._write(f"</{tag_name}>\n")

    @contextmanager
    def tag(self, tag_name: str):
        """Context manager for XML tags."""
        self._open_tag(tag_name)
        yield
        self._close_tag(tag_name)

    @contextmanager
    def _symbol_context(self, open_symbol: Symbol, close_symbol: Symbol):
        """Context manager for symbols like {}, (), []"""
        self._consume(open_symbol)
        yield
        self._consume(close_symbol)

    def _braces(self):
        """Context manager for braces {}"""
        return self._symbol_context(Symbol.LBRACE, Symbol.RBRACE)

    def _parentheses(self):
        """Context manager for parentheses ()"""
        return self._symbol_context(Symbol.LPAREN, Symbol.RPAREN)

    def _brackets(self):
        """Context manager for brackets []"""
        return self._symbol_context(Symbol.LBRACK, Symbol.RBRACK)


# Note: The following rules in the Jack grammar have no corresponding _compile_xxx methods:
# - type
# - className
# - subroutineName
# - variableName
# - statement
# The parsing logic of these rules is handled by the rules that invoke them.
# In the course SubroutineCall is included in this list in the
