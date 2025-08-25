
import math
from jack_tokenizer import TokenType
from jack_tokenizer import JackTokenizer
from jack_tokens import Keyword,Symbol,Token

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


    def compile_class(self):
        '''
        Compile a complete class
        grammar: 'class' className '{' classVarDec* subroutineDec* '}'
        '''
        with open(self.output_file, 'w') as self.f:
            self.token = self.tokenizer.advance()  # 'class'
            self._open_tag('class')
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
            self._close_tag('class')
            if self.tokenizer.has_more_tokens():
                raise ValueError("Extra tokens after class declaration")
                
            

    def compile_class_var_dec(self):
        '''
        Compile a static variable declaration, or a field declaration.
        grammar: (static | field) type varName (',' varName)* ';'
        '''
        self._open_tag('classVarDec')
        self._write_token()  # 'static' | 'field'
        self.token = self.tokenizer.advance()  # type
        self._compile_type()
        self._compile_identifier()
        while self.token == Symbol.COMMA:
            self._write_token()
            self.token = self.tokenizer.advance()
            self._compile_identifier()
        self._compile_enumtoken(Symbol.SEMICOLON)
        self._close_tag('classVarDec')

    def compile_subroutine_dec(self):
        '''
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        '''
        self._open_tag('subroutineDec')
        self._write_token()  # 'constructor' | 'function' | 'method'
        self.token = self.tokenizer.advance()  # 'void' | type
        self._compile_return_type()
        self._compile_enumtoken(Symbol.LPAREN)
        self.compile_parameter_list()
        self._compile_enumtoken(Symbol.RPAREN)
        self.compile_subroutine_body()
        self._close_tag('subroutineDec')

    def _compile_return_type(self):
        if self.token == Keyword.VOID or self.token.ttype == TokenType.IDENTIFIER:
            self._write_token()
            self.token = self.tokenizer.advance()  # subroutineName
            self._compile_identifier()
        else:
            raise ValueError("Expected 'void' or 'type' after subroutine keyword")

    def compile_parameter_list(self):
        '''
        Compile a (possibly empty) parameter list.
        Does not handle the enclosing parentheses ().
        grammar: ((type varName) (',' type varName)*)?
        '''
        self._open_tag('parameterList')
        if self.token.is_type():  # type
            self._write_token()
            self.token = self.tokenizer.advance()
            self._compile_identifier()
            while self.token == Symbol.COMMA:  # (',' type varName)*)?
                self._write_token()
                self.token = self.tokenizer.advance()
                self._compile_type()
                self._compile_identifier()
        self._close_tag('parameterList')

    def compile_subroutine_body(self):
        '''
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        '''
        self._open_tag('subroutineBody')
        self._compile_enumtoken(Symbol.LBRACE)
        while self.token == Keyword.VAR:
            self.compile_var_dec()
        self.compile_statements()
        self._compile_enumtoken(Symbol.RBRACE)
        self._close_tag('subroutineBody')

    def compile_var_dec(self):
        '''
        Compile a variable declaration
        grammar: 'var' type varName (',' varName)* ';'
        '''
        self._open_tag('varDec')
        self._write_token()  # 'var'
        self.token = self.tokenizer.advance()
        if self.token.is_type():  # type
            self._write_token()
            self.token = self.tokenizer.advance()
            self._compile_identifier()  # varName
            while self.token == Symbol.COMMA:  # (',' varName)*?
                self._write_token()
                self.token = self.tokenizer.advance()
                self._compile_identifier()  # varName
            self._compile_enumtoken(Symbol.SEMICOLON)
        self._close_tag('varDec')

    def compile_statements(self):
        '''
        Compile a sequence of statements.
        Does not handle the enclosing braces {}.
        grammar: statement*
        '''
        self._open_tag('statements')
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
        self._close_tag('statements')

    def compile_let(self):
        '''
        Compile a let statement.
        grammar: 'let' varName('[' expression ']')? '=' expression ';'
        '''
        self._open_tag('letStatement')
        self._compile_enumtoken(Keyword.LET)
        self._compile_identifier()
        if self.token == Symbol.LBRACK:
            self._compile_enumtoken(Symbol.LBRACK)
            self.compile_expression()
            self._compile_enumtoken(Symbol.RBRACK)
        self._compile_enumtoken(Symbol.EQ)
        self.compile_expression()
        self._compile_enumtoken(Symbol.SEMICOLON)
        self._close_tag('letStatement')

    def compile_if(self):
        '''
        Compile an if statement, possibly with a trailing else clause.
        grammar: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        '''
        self._open_tag('ifStatement')
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
        self._close_tag('ifStatement')

    def compile_while(self):
        '''
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        '''
        self._open_tag('whileStatement')
        self._compile_enumtoken(Keyword.WHILE)
        self._compile_enumtoken(Symbol.LPAREN)
        self.compile_expression()
        self._compile_enumtoken(Symbol.RPAREN)
        self._compile_enumtoken(Symbol.LBRACE)
        self.compile_statements()
        self._compile_enumtoken(Symbol.RBRACE)
        self._close_tag('whileStatement')

    def compile_do(self):
        '''
        Compile a do statement.
        grammar: 'do' subroutineCall  ';'
        '''
        self._open_tag('doStatement')
        self._compile_enumtoken(Keyword.DO)
        self._compile_subroutine_call()
        self._compile_enumtoken(Symbol.SEMICOLON)
        self._close_tag('doStatement')

    def compile_return(self):
        '''
        Compile a return statement.
        grammar: 'return' expression? ';'
        '''
        self._open_tag('returnStatement')
        self._compile_enumtoken(Keyword.RETURN)
        if self.token != Symbol.SEMICOLON:
            self.compile_expression()
        self._compile_enumtoken(Symbol.SEMICOLON)
        self._close_tag('returnStatement')

    def compile_expression(self):
        '''
        Compile an expression.
        grammar: term (op term)*
        '''
        self._open_tag('expression')
        self.compile_term()
        while self.token.is_op():
            self._compile_enumtoken(self.token)
            self.compile_term()
        self._close_tag('expression')

    def compile_term(self):
        '''
        Compile a term. 
        If the current token is an identifier, the routine must distinguish 
        between a variable, an array entry, or a subroutine call.
        A single look-ahead token which may be one of: "[" "(" or ".", suffices to
        distinguish between the possibilities. Any other token is not part of this term 
        and should be advanced over.
        grammar: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        '''
        self._open_tag('term')
        if self.token.is_constant():
            self._write_token()
            self.token = self.tokenizer.advance()
        elif self.token.ttype == TokenType.IDENTIFIER:
            next_token = self.tokenizer.next_token()
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
        self._close_tag('term')

    def compile_expression_list(self):
        '''
        Compile a (possibly empty) comma-separated list of expressions.
        grammar: (expression (',' expression)*)?
        '''
        self._open_tag('expressionList')
        if self.token != Symbol.RPAREN:
            self.compile_expression()
            while self.token == Symbol.COMMA:
                self._compile_enumtoken(Symbol.COMMA)
                self.compile_expression()
        self._close_tag('expressionList')

    def _compile_subroutine_call(self):
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

    def _open_tag(self, tag_name: str):
        self._write(f'<{tag_name}>\n')
        self.ident += 2

    def _close_tag(self, tag_name: str):
        self.ident -= 2
        self._write(f'</{tag_name}>\n')

    def _write(self,text:str):
        self.f.write(f'{" " * self.ident}{text}')

    def _write_token(self):
        self._write(self.token.xml())

    def _compile_enumtoken(self, token: Keyword|Symbol):
        '''
        Compile a keyword or symbol
        grammar: keyword | symbol
        '''
        if self.token == token:
            self._write_token()
            self.token = self.tokenizer.advance()
        else:
            raise ValueError(f"Expected {token.ttype}: '{token}'")

    def _compile_identifier(self):
        '''
        Compile an identifier
        grammar: varName
        '''
        if self.token.ttype == TokenType.IDENTIFIER:
            self._write_token()
            self.token = self.tokenizer.advance()
        else:
            raise ValueError(f"Expected an identifier")


    def _compile_type(self):
        '''
        Compile a type
        grammar: 'int' | 'char' | 'boolean' | className
        '''
        if self.token.is_type():
            self._write_token()
            self.token = self.tokenizer.advance()
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