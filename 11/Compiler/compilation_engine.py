"""
compilation_engine.py

This module implements the CompilationEngine for the Jack Analyzer project in nand2tetris.
It parses Jack source code according to the Jack grammar and generates the corresponding output,
serving as the core of the Jack _compiler's syntax analysis phase.
"""

from contextlib import contextmanager

from jack_tokenizer import JackTokenizer, Token
from vm_writer import VMWriter,SEGMENT as SEG,ARITHMETIC_CMD as A_CMD
from tokens.enums import UNARY_OPS, BINARY_OPS,SUBROUTINES,JACK_OPS, Keyword, Symbol
from tokens.identifier import IdentifierCategory as IdCat, Identifier
from tokens.inmutables import IntegerConstant,StringConstant
from symbol_table import SymbolTable,VarK, VarT, IdentifierContext as IdContext,VarUse, VarSymbol
from typing import Literal
from itertools import count

class CompilationEngine:
    '''
    Builds the XML representation of the Jack program.
    It has a compile method for 15 of the 21 non-terminal rules of the Jack grammar
    '''
    ident_step = 2

    def __init__(self, input_file:str, output_file: str):
        self.tokenizer = JackTokenizer(input_file)
        self.vm_writer = VMWriter(output_file)
        self.table = SymbolTable()
        self.output_file = output_file
        self.ident = 0
        self.n_expr = 0
        # The labels id can be jointly managed with a single counter
        # I implement it this way just to reproduce the course compiler implementation
        self.golabel_id: count[int] = count(start=0, step=2)
        self.iflabel_id: count[int] = count(start=1, step=2)
        self.class_name: Identifier
        self.subroutine_token: Keyword
        self.context: IdContext | Literal[""] = ""

    # ----------------------------------------
    # Compilation Methods
    # ----------------------------------------

    def compile_class(self) -> None:
        '''
        Compile a complete class
        grammar: 'class' className '{' classVarDec* subroutineDec* '}'
        '''
        try:
            with self.vm_writer.open():
                self._consume(Keyword.CLASS)
                self.class_name = self.tokenizer.identifier()
                self.context = IdContext(IdCat.CLASS, use=VarUse.DEF)
                self._consume(Identifier)
                with self._braces():
                    while self.token in (Keyword.STATIC, Keyword.FIELD):
                        self._compile_class_var_dec()
                    while self.token in SUBROUTINES:
                        self._compile_subroutine_dec()
                if self.tokenizer.has_more_tokens():
                    raise ValueError("Extra tokens after class end")
        finally:
            self.vm_writer.f.close()

    def _compile_class_var_dec(self) -> None:
        '''
        Compile a static variable declaration, or a field declaration.
        grammar: (static | field) type varName (',' varName)* ';'
        '''
        var_kind = self.tokenizer.var_kind()
        self._consume(Keyword.STATIC, Keyword.FIELD)
        var_type = self._compile_type()  # type
        self._compile_variable_def(var_kind, var_type)
        while self.token == Symbol.COMMA:
            self._consume()
            self._compile_variable_def(var_kind, var_type)
        self._consume(Symbol.SEMICOLON)

    def _compile_subroutine_dec(self) -> None:
        '''
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        '''
        self.table.start_subroutine()
        self.subroutine_token = self.tokenizer.keyword()
        self._consume(*SUBROUTINES)
        if self.subroutine_token == Keyword.CONSTRUCTOR:
            return_type = self.tokenizer.identifier()
            assert self.class_name == return_type, f"Constructor return type must be the class name '{self.class_name}', got '{return_type}'"
        self._compile_return_type()
        self.context = IdContext(IdCat.SUBROUTINE, use=VarUse.DEF)
        self.table.subroutine_name = self.tokenizer.identifier()
        self._consume(Identifier)
        if self.subroutine_token == Keyword.METHOD:
            # Implicit 'this' argument for methods
            self.table.define(Identifier('this'), self.class_name, VarK.ARG)
        with self._parentheses():
            self._compile_parameter_list()      
        self._compile_subroutine_body()
        
    def _compile_parameter_list(self) -> None:
        '''
        Compile a (possibly empty) parameter list.
        Does not handle the enclosing parentheses ().
        grammar: ((type varName) (',' type varName)*)?
        '''
        if self.tokenizer.token_is_var_type():
            self._compile_variable_def(kind=VarK.ARG)
            while self.token == Symbol.COMMA:  # (',' type varName)*)?
                self._consume()
                self._compile_variable_def(kind=VarK.ARG)

    def _compile_subroutine_body(self) -> None:
        '''
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        '''
        with self._braces():
            while self.token == Keyword.VAR:
                self._compile_var_dec()
            function_name = f"{self.class_name}.{self.table.subroutine_name}"
            self.vm_writer.write_function(function_name, self.table.var_count(VarK.LOCAL))
            if self.subroutine_token == Keyword.CONSTRUCTOR:
                n_fields = self.table.var_count(VarK.THIS)
                self.vm_writer.write_push(SEG.CONST, n_fields)
                self.vm_writer.write_call("Memory.alloc", 1)
                self.vm_writer.write_pop(SEG.POINTER, 0)  # set 'this' to the base address
            elif self.subroutine_token == Keyword.METHOD:
                self.vm_writer.write_push(SEG.ARG, 0)
                self.vm_writer.write_pop(SEG.POINTER, 0)  # set 'this' to the first argument
            self._compile_statements()

    def _compile_var_dec(self) -> None:
        '''
        Compile a variable declaration
        grammar: 'var' type varName (',' varName)* ';'
        '''
        self._consume(Keyword.VAR)
        if self.tokenizer.token_is_var_type():  # type
            var_type = self._compile_type()
            self._compile_variable_def(VarK.LOCAL, var_type)
            while self.token == Symbol.COMMA:  # (',' varName)*?
                self._consume()
                self._compile_variable_def(VarK.LOCAL, var_type)  # varName
            self._consume(Symbol.SEMICOLON)

    def _compile_statements(self) -> None:
        '''
        Compile a sequence of statements.
        Does not handle the enclosing braces {}.
        grammar: statement*
        '''
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
        '''
        Compile a let statement.
        grammar: 'let' varName('[' expression ']')? '=' expression ';'
        '''
        self._consume(Keyword.LET)
        var_name = self.tokenizer.identifier()
        symbol = self.table.get_symbol(var_name)  # to ensure it exists
        if symbol is None:
            raise ValueError(f"Identifier '{var_name}' not found in symbol table.")
        self._consume_variable(var_name=var_name, use=VarUse.ASSIGN)
        array_var = self.token == Symbol.LBRACK
        if array_var:
            with self._brackets():
                self._compile_expression()
            self.vm_writer.write_push(SEG[symbol.kind.name], symbol.index)
            self.vm_writer.write_arithmetic(A_CMD['ADD'])
        self._consume(Symbol.EQ)
        self._compile_expression()
        if array_var:
            self.vm_writer.write_pop(SEG.TEMP, 0)  # store the value to be assigned in temp 0
            self.vm_writer.write_pop(SEG.POINTER, 1)  # that = base address + offset
            self.vm_writer.write_push(SEG.TEMP, 0)  # push the value of 'that' (base address + offset)
            self.vm_writer.write_pop(SEG.THAT, 0)  # store the value to be assigned in temp 0
        else:
            self.vm_writer.write_pop(SEG[symbol.kind.name], symbol.index)  # for assignment
        self._consume(Symbol.SEMICOLON)

    def _compile_if(self) -> None:
        '''
        Compile an if statement, possibly with a trailing else clause.
        grammar: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        '''
        # The l2 id assignation can be placed after compiling the "if statements" 
        # This way you get a sequential labeling.
        # I placed here just to reproduce the course compiler implementation
        l1 = next(self.iflabel_id)
        l2 = next(self.golabel_id)
        self._consume(Keyword.IF)
        with self._parentheses():
            self._compile_expression()
        self.vm_writer.write_arithmetic(A_CMD['NOT'])

        self.vm_writer.write_if(f"{self.class_name}_{l1}")
        with self._braces():
            self._compile_statements()
        
        self.vm_writer.write_goto(f"{self.class_name}_{l2}")
        self._write_label(l1)
        if self.token == Keyword.ELSE:
            self._consume(Keyword.ELSE)
            with self._braces():
                self._compile_statements()
        self._write_label(l2)

    def _compile_while(self) -> None:
        '''
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        '''
        self._consume(Keyword.WHILE)
        l1 = next(self.golabel_id)
        self._write_label(l1)
        with self._parentheses():
            self._compile_expression()
            self.vm_writer.write_arithmetic(A_CMD['NOT'])
            l2 = next(self.iflabel_id)
            self.vm_writer.write_if(f"{self.class_name}_{l2}")
        with self._braces():
            self._compile_statements()
        self.vm_writer.write_goto(f"{self.class_name}_{l1}")
        self._write_label(l2)

    def _compile_do(self) -> None:
        '''
        Compile a do statement.
        grammar: 'do' subroutineCall  ';'
        '''
        self._consume(Keyword.DO)
        self._compile_subroutine_call(self.tokenizer.peek())
        self.vm_writer.write_pop(SEG.TEMP,0)  # discard return value
        self._consume(Symbol.SEMICOLON)

    def _compile_return(self) -> None:
        '''
        Compile a return statement.
        grammar: 'return' expression? ';'
        '''
        self._consume(Keyword.RETURN)
        ## void subroutine
        if self.token == Symbol.SEMICOLON:
            self.vm_writer.write_push(SEG.CONST, 0)
        ## constructor or method
        elif self.token == Keyword.THIS:
            self.vm_writer.write_push(SEG.POINTER, 0)
            self._consume(Keyword.THIS)
        else:
            self._compile_expression()
        self._consume(Symbol.SEMICOLON)
        self.vm_writer.write_return()

    def _compile_expression(self) -> None:
        '''
        Compile an expression.
        grammar: term (op term)*
        '''
        self._compile_term()
        while self.token in BINARY_OPS:
            op_token = self.token
            self._consume()
            self._compile_term()
            if op_token in JACK_OPS:
                self.vm_writer.write_arithmetic(A_CMD[op_token.name])
            elif op_token == Symbol.MULT:
                self.vm_writer.write_call("Math.multiply", 2)
            elif op_token == Symbol.DIV:
                self.vm_writer.write_call("Math.divide", 2)

    def _compile_term(self) -> None:
        '''
        Compile a term. 
        If the current token is an identifier, the routine must distinguish 
        between a variable, an array entry, or a subroutine call.
        A single look-ahead token which may be one of: "[" "(" or ".", suffices to
        distinguish between the possibilities. Any other token is not part of this term 
        and should be advanced over.
        grammar: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        '''
        # integerConstant | stringConstant | keywordConstant
        if self.tokenizer.token_is_constant():
            if self.token == Keyword.TRUE:
                self.vm_writer.write_push(SEG.CONST, 1)
                self.vm_writer.write_arithmetic(A_CMD['NEG'])
            if self.token in (Keyword.FALSE, Keyword.NULL):
                self.vm_writer.write_push(SEG.CONST, 0)
            if self.token == Keyword.THIS:
                self.vm_writer.write_push(SEG.POINTER, 0)
            if isinstance(self.token,IntegerConstant):
                self.vm_writer.write_push(SEG.CONST, self.token)
            if isinstance(self.token, StringConstant):  # stringConstant
                string = str(self.token)
                self.vm_writer.write_push(SEG.CONST, len(string))
                self.vm_writer.write_call("String.new", 1)
                for char in string:
                    self.vm_writer.write_push(SEG.CONST, ord(char))
                    self.vm_writer.write_call("String.appendChar", 2)
            self._consume()
        # '(' expression ')' 
        elif self.token == Symbol.LPAREN:
            with self._parentheses():
                self._compile_expression()
        # unaryOp term
        elif self.token in UNARY_OPS:
            uop_token = self.token
            self._consume()
            self._compile_term()
            self.vm_writer.write_arithmetic(A_CMD['NEG' if uop_token == Symbol.SUB else 'NOT'])
        # varName| varName '[' expression ']' | subroutineCall
        elif isinstance(self.token, Identifier):
            next_token = self.tokenizer.peek()
            # subroutineCall
            if next_token in [Symbol.LPAREN, Symbol.DOT]:
                self._compile_subroutine_call(next_token)
            # varName | varName '[' expression ']'
            else:
                symbol = self.table.get_symbol(self.token)
                if symbol is None:
                    raise ValueError(f"Identifier '{self.token}' not found in symbol table.")
                self._consume_variable(var_name=self.token, use=VarUse.REF)
                # varName '[' expression ']'
                if self.token == Symbol.LBRACK:
                    with self._brackets():
                        self._compile_expression()
                    self.vm_writer.write_push(SEG[symbol.kind.name], symbol.index)
                    self.vm_writer.write_arithmetic(A_CMD['ADD'])
                    self.vm_writer.write_pop(SEG.POINTER, 1)  # that = base address + offset
                    self.vm_writer.write_push(SEG.THAT, 0)  # push the value of 'that' (base address + offset)
                # varName 
                else:
                    self.vm_writer.write_push(SEG[symbol.kind.name], symbol.index)  # to match the course compiler implementation
        else:
            raise ValueError(f"Unexpected token in term: {self.token}")

    def _compile_expression_list(self) -> None:
        '''
        Compile a (possibly empty) comma-separated list of expressions.
        grammar: (expression (',' expression)*)?
        '''
        self.n_expr = 0
        if self.token != Symbol.RPAREN:
            self._compile_expression()
            self.n_expr += 1
            while self.token == Symbol.COMMA:
                self._consume()
                self._compile_expression()
                self.n_expr += 1

    def _compile_subroutine_call(self, next_token: Token) -> None:
        '''
        Compile a subroutine call.
        grammar: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList  ')'
        '''
        call_text = ""
        object_call = False
        # (className | varName) '.' subroutineName '(' expressionList  ')'
        if next_token == Symbol.DOT:
            identifier = self.tokenizer.identifier()
            symbol = self.table.get_symbol(identifier)
            # className
            if symbol is None:
                call_text += str(self.token)
                self.context = IdContext(IdCat.CLASS, use=VarUse.REF)
            # varName
            # This is an object call (using a method)
            elif isinstance(symbol.type, Identifier):
                object_call = True
                call_text += str(symbol.type)
                self.vm_writer.write_push(SEG[symbol.kind.name], symbol.index) # push 'this' to the stack
                self.context = IdContext(IdCat.VARIABLE, use=VarUse.REF, kind=symbol.kind, index=symbol.index)
            else:
                raise ValueError(f"A class name or variable name is expected.")
            self._consume(Identifier)
            call_text += str(self.token)
            self._consume(Symbol.DOT)
        # subroutineName '(' expressionList ')'
        # this is a call from the current object 
        else:
            object_call = True
            self.vm_writer.write_push(SEG.POINTER, 0)
            call_text += str(self.class_name)+"."
        self.context = IdContext(IdCat.SUBROUTINE, use=VarUse.REF)
        call_text += str(self.token)
        self._consume(Identifier)
        with self._parentheses():
            self._compile_expression_list()
        self.vm_writer.write_call(call_text, self.n_expr+object_call)

    def _compile_type(self) -> VarT:
        '''
        Compile a type
        grammar: 'int' | 'char' | 'boolean' | className
        '''
        
        if isinstance(self.token, Identifier):
            self.context = IdContext(IdCat.CLASS, use=VarUse.REF)
        else:
            match self.token:
                case Keyword.INT | Keyword.CHAR | Keyword.BOOLEAN:
                    pass
                case _:
                    raise ValueError("Expected type to be 'int', 'char', 'boolean', or className")
        var_type = self.token
        self._consume()
        return var_type

    def _compile_return_type(self) -> None:
        '''
        Compile a return type
        grammar: 'void' | type
        '''
        if self.token == Keyword.VOID:
            self._consume()
        else:
            self._compile_type()

    def _compile_variable_def(self, kind: VarK, var_type: VarT|None=None) -> None:
        '''
        Compile a variable
        grammar: (type) varName
        '''
        if var_type is None:
            var_type = self._compile_type()
        var_name = self.tokenizer.identifier()
        self.table.define(var_name, var_type, kind)
        self._consume_variable(var_name=var_name, use=VarUse.DEF)

    # ----------------------------------------
    # Compile Helpers (token handling)
    # ----------------------------------------

    def _consume(self, *tokens: Keyword | Symbol | type[Identifier]) -> None:
        """
        Write and advance if the current token matches any of the provided tokens.
        If no tokens are provided, always write and advance.
        """
        if not tokens or any(
            self.token == t or (isinstance(t, type) and isinstance(self.token, t))
            for t in tokens
        ):
            #self._write_token()
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
        else:
            expected = ', '.join(str(t) for t in tokens)
            raise ValueError(f"Expected one of: {expected}, got: '{self.token}'")

    def _consume_variable(self, var_name: Identifier, use: VarUse) -> VarSymbol:
        '''
        Consume a variable
        grammar: varName
        '''
        symbol = self.table.get_symbol(var_name)
        if symbol is None:
            raise ValueError(f"Identifier '{var_name}' not found in symbol table.")
        self.context = IdContext(IdCat.VARIABLE, use=use, kind=symbol.kind, index=symbol.index)
        self._consume(Identifier)
        return symbol

    @property
    def token(self) -> Token:
        """Alias for the current token from the tokenizer."""
        return self.tokenizer.token

    def _write_label(self,label_id:int):            
        self.vm_writer.write_label(f"{self.class_name}_{label_id}")

    # ------------------------------------------------------------
    # context management helper methods (private)
    # ------------------------------------------------------------
    
    @contextmanager
    def _symbol_context(self, open_symbol: Symbol, close_symbol: Symbol):
        '''Context manager for symbols like {}, (), []'''
        self._consume(open_symbol)
        yield
        self._consume(close_symbol)

    def _braces(self):
        '''Context manager for braces {}'''
        return self._symbol_context(Symbol.LBRACE, Symbol.RBRACE)

    def _parentheses(self):
        '''Context manager for parentheses ()'''
        return self._symbol_context(Symbol.LPAREN, Symbol.RPAREN)

    def _brackets(self):
        '''Context manager for brackets []'''
        return self._symbol_context(Symbol.LBRACK, Symbol.RBRACK)


