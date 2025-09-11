"""
compilation_engine.py

This module implements the CompilationEngine for the Jack Analyzer project in nand2tetris.
It parses Jack source code according to the Jack grammar and generates the corresponding output,
serving as the core of the Jack _compiler's syntax analysis phase.
"""

from contextlib import contextmanager

from jack_tokenizer import JackTokenizer, Token
from vm_writer import VMWriter,SEGMENT as SEG,ARITHMETIC_CMD as A_CMD
from tokens.enums import UNARY_OPS, BINARY_OPS,SUBROUTINES,PRIMITIVE_TYPES, Keyword as Key, Symbol
from tokens.identifier import IdentifierCategory as IdCat, Identifier
from tokens.inmutables import IntegerConstant,StringConstant
from symbol_table import SymbolTable,VarK, VarT, IdentifierContext as IdContext,VarUse

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
        
        # The labels id can be jointly managed with a single counter
        # I implement it this way just to reproduce the course compiler implementation
        self.class_name: Identifier
        self.context: IdContext

    # ----------------------------------------
    # Compilation Methods
    # ----------------------------------------

    def compile_class(self) -> None:
        '''
        Compile a complete class
        grammar: 'class' className '{' classVarDec* subroutineDec* '}'
        '''
        with self.vm_writer.open():
            self.tokenizer.consume(Key.CLASS)
            self.class_name = self.tokenizer.consume(Identifier)
            with self._braces():
                while self.token in (Key.STATIC, Key.FIELD):
                    self._compile_var_dec(Key.STATIC, Key.FIELD)
                while self.token in SUBROUTINES:
                    self._compile_subroutine_dec()
            if self.tokenizer.has_more_tokens():
                raise ValueError("Extra tokens after class end")


    def _compile_subroutine_dec(self) -> None:
        '''
        Compile a complete method, function, or constructor
        grammar: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('parameterList')' subroutineBody
        '''
        self.table.start_subroutine()
        subroutine_key = self.tokenizer.consume(*SUBROUTINES)
        self.tokenizer.consume(Key.VOID, *PRIMITIVE_TYPES, Identifier)
        self.context = IdContext(IdCat.SUBROUTINE, use=VarUse.DEF)
        self.table.subroutine_name = self.tokenizer.consume(Identifier)
        if subroutine_key == Key.METHOD:
            self.table.define(Identifier('this'), self.class_name, VarK.ARG)
        with self._parentheses():
            if self.tokenizer.token_is_var_type():
                self._compile_parameter_list(var_kind=VarK.ARG)
        self._compile_subroutine_body(subroutine_key)

    def _compile_parameter_list(self,var_kind: VarK, var_type: VarT|None=None) -> None:
        '''
        Compile a (possibly empty) parameter list.
        Does not handle the enclosing parentheses ().
        grammar: ((type varName) (',' type varName)*)?
        '''
        self._compile_variable_def(kind=var_kind, var_type=var_type)
        while self.token == Symbol.COMMA:  # (',' type varName)*)?
            self.tokenizer.consume(Symbol.COMMA)
            self._compile_variable_def(kind=var_kind, var_type=var_type)

    def _compile_subroutine_body(self, subroutine_key: Key) -> None:
        '''
        Compile a subroutine's body
        grammar: '{' varDec* statements '}'
        '''
        with self._braces():
            while self.token == Key.VAR:
                self._compile_var_dec(Key.VAR)
            function_name = f"{self.class_name}.{self.table.subroutine_name}"
            self.vm_writer.write_function(function_name, self.table.var_count(VarK.LOCAL))
            if subroutine_key == Key.CONSTRUCTOR:
                n_fields = self.table.var_count(VarK.THIS)
                self.vm_writer.write_constructor_alloc(n_fields)  # set 'this' to the base address
            elif subroutine_key == Key.METHOD:
                self.vm_writer.write_method_setup()
            self._compile_statements()

    def _compile_var_dec(self, *var_kind_keys: Key) -> None:
        '''
        Compile a variable declaration
        grammar: var_kind type varName (',' varName)* ';'
        '''
        var_kind = self.tokenizer.consume_var_kind(*var_kind_keys)
        if isinstance(self.token, Identifier):
            self.context = IdContext(IdCat.CLASS, use=VarUse.REF)
        var_type = self.tokenizer.consume(Key.INT, Key.CHAR, Key.BOOLEAN, Identifier)
        self._compile_parameter_list(var_kind,var_type)
        self.tokenizer.consume(Symbol.SEMICOLON)

    def _compile_statements(self) -> None:
        '''
        Compile a sequence of statements.
        Does not handle the enclosing braces {}.
        grammar: statement*
        '''
        while True:
            match self.token:
                case Key.LET:
                    self._compile_let()
                case Key.IF:
                    self._compile_if()
                case Key.WHILE:
                    self._compile_while()
                case Key.DO:
                    self._compile_do()
                case Key.RETURN:
                    self._compile_return()
                case _:
                    break

    def _compile_let(self) -> None:
        '''
        Compile a let statement.
        grammar: 'let' varName('[' expression ']')? '=' expression ';'
        '''
        self.tokenizer.consume(Key.LET)
        var_address = self._compile_variable(use=VarUse.ASSIGN)
        is_array_var = self.token == Symbol.LBRACK
        if is_array_var:
            with self._brackets():
                self._compile_expression()
            self.vm_writer.write_push_array_element_address(*var_address)
        self.tokenizer.consume(Symbol.EQ)
        self._compile_expression()
        if is_array_var:
            self.vm_writer.write_assign_to_array_element()
        else:
            self.vm_writer.write_pop_variable(*var_address)  # for assignment
        self.tokenizer.consume(Symbol.SEMICOLON)

    def _compile_if(self) -> None:
        '''
        Compile an if statement, possibly with a trailing else clause.
        grammar: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        '''
        # The l2 id assignation can be placed after compiling the "if statements" 
        # This way you get a sequential labeling.
        # I placed here just to reproduce the course compiler implementation
        l1 = next(self.vm_writer.iflabel_id)
        l2 = next(self.vm_writer.golabel_id)
        self.tokenizer.consume(Key.IF)
        with self._parentheses():
            self._compile_expression()
        self.vm_writer.write_arithmetic(A_CMD.NOT)
        self._write_if(l1)
        with self._braces():
            self._compile_statements()
        self._write_goto(l2)
        self._write_label(l1)
        if self.token == Key.ELSE:
            self.tokenizer.consume(Key.ELSE)
            with self._braces():
                self._compile_statements()
        self._write_label(l2)

    def _compile_while(self) -> None:
        '''
        Compile a while statement.
        grammar: 'while' '(' expression ')' '{' statements '}'
        '''
        self.tokenizer.consume(Key.WHILE)
        l1 = next(self.vm_writer.golabel_id)
        l2 = next(self.vm_writer.iflabel_id)
        self._write_label(l1)
        with self._parentheses():
            self._compile_expression()
            self.vm_writer.write_arithmetic(A_CMD.NOT)
            self._write_if(l2)
        with self._braces():
            self._compile_statements()
        self._write_goto(l1)
        self._write_label(l2)

    def _compile_do(self) -> None:
        '''
        Compile a do statement.
        grammar: 'do' subroutineCall  ';'
        '''
        self.tokenizer.consume(Key.DO)
        self._compile_subroutine_call(self.tokenizer.peek())
        self.vm_writer.write_pop(SEG.TEMP,0)  # discard return value
        self.tokenizer.consume(Symbol.SEMICOLON)

    def _compile_return(self) -> None:
        '''
        Compile a return statement.
        grammar: 'return' expression? ';'
        '''
        self.tokenizer.consume(Key.RETURN)
        ## void subroutine
        if self.token == Symbol.SEMICOLON:
            self.vm_writer.write_push(SEG.CONST, 0)
        ## constructor or method
        elif self.token == Key.THIS:
            self.vm_writer.write_push(SEG.POINTER, 0)
            self.tokenizer.consume(Key.THIS)
        else:
            self._compile_expression()
        self.tokenizer.consume(Symbol.SEMICOLON)
        self.vm_writer.write_return()

    def _compile_expression(self) -> None:
        '''
        Compile an expression.
        grammar: term (op term)*
        '''
        self._compile_term()
        while self.token in BINARY_OPS:
            op_token = self.tokenizer.consume(*BINARY_OPS)
            self._compile_term()
            match op_token:
                case Symbol.MULT:
                    self.vm_writer.write_call("Math.multiply", 2)
                case Symbol.DIV:
                    self.vm_writer.write_call("Math.divide", 2)
                case _:
                    self.vm_writer.write_arithmetic(A_CMD[op_token.name])

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
            match self.token:
                case Key.TRUE:
                    self.vm_writer.write_push(SEG.CONST, 1)
                    self.vm_writer.write_arithmetic(A_CMD.NEG)
                case Key.FALSE | Key.NULL:
                    self.vm_writer.write_push(SEG.CONST, 0)
                case Key.THIS:
                    self.vm_writer.write_push(SEG.POINTER, 0)
                case _:
                    if isinstance(self.token, IntegerConstant):
                        self.vm_writer.write_push(SEG.CONST, self.token)
                    if isinstance(self.token, StringConstant):  # stringConstant
                        self.vm_writer.write_string_constant(str(self.token))
            self.tokenizer.consume() 
        # '(' expression ')' 
        elif self.token == Symbol.LPAREN:
            with self._parentheses():
                self._compile_expression()
        # unaryOp term
        elif self.token in UNARY_OPS:
            uop_token = self.tokenizer.consume(*UNARY_OPS)
            self._compile_term()
            self.vm_writer.write_arithmetic(A_CMD.NEG if uop_token == Symbol.SUB else A_CMD.NOT)
        # varName| varName '[' expression ']' | subroutineCall
        elif isinstance(self.token, Identifier):
            next_token = self.tokenizer.peek()
            # subroutineCall
            if next_token in (Symbol.LPAREN, Symbol.DOT):
                self._compile_subroutine_call(next_token)
            # varName | varName '[' expression ']'
            else:
                var_address = self._compile_variable(use=VarUse.REF)
                # varName '[' expression ']'
                if self.token == Symbol.LBRACK:
                    with self._brackets():
                        self._compile_expression()
                    self.vm_writer.write_push_array_element(*var_address)
                # varName 
                else:
                    self.vm_writer.write_push_variable(*var_address)  # to match the course compiler implementation
        else:
            raise ValueError(f"Unexpected token in term: {self.token}")

    def _compile_expression_list(self) -> int:
        '''
        Compile a (possibly empty) comma-separated list of expressions.
        grammar: (expression (',' expression)*)?
        '''
        n_expr = 0
        if self.token != Symbol.RPAREN:
            self._compile_expression()
            n_expr += 1
            while self.token == Symbol.COMMA:
                self.tokenizer.consume(Symbol.COMMA)
                self._compile_expression()
                n_expr += 1
        return n_expr
    
    ## NO API METHODS BELOW THIS LINE ##
    def _compile_variable_def(self, kind: VarK, var_type: VarT | None = None) -> None:
        '''
        Compile a variable
        grammar: (type)? varName
        '''
        if var_type is None:
            var_type = self.tokenizer.consume(Key.INT, Key.CHAR, Key.BOOLEAN, Identifier)
        var_name = self.tokenizer.consume(Identifier)
        self.table.define(var_name, var_type, kind)
        var_idx = self.table.index_of(var_name)
        self.context = IdContext(IdCat.VARIABLE, use=VarUse.DEF, kind=kind, index=var_idx)

    def _compile_variable(self, use: VarUse) -> tuple[VarK,int]:
        '''
        Consume a variable reference
        grammar: varName
        '''
        var_name = self.tokenizer.consume(Identifier)
        var_kind = self.table.kind_of(var_name)
        if var_kind is None:
            raise ValueError(f"Identifier '{var_name}' not found in symbol table.")
        var_idx = self.table.index_of(var_name)
        self.context = IdContext(IdCat.VARIABLE, use=use, kind=var_kind, index=var_idx)
        return var_kind, var_idx
    
    def _compile_subroutine_call(self, next_token: Token) -> None:
        '''
        Compile a subroutine call.
        grammar: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList  ')'
        '''
        call_name = ""
        object_call = False
        # (className | varName) '.' subroutineName '(' expressionList  ')'
        if next_token == Symbol.DOT:
            var_name = self.tokenizer.consume(Identifier)
            variable = self.table.get_var(var_name)
            # className
            if variable is None:
                call_name += var_name
                self.context = IdContext(IdCat.CLASS, use=VarUse.REF)
            # varName
            # This is an object call (using a method)
            elif isinstance(variable.type, Identifier):
                object_call = True
                call_name += str(variable.type)
                self.vm_writer.write_push_variable(variable.kind, variable.index)  # push 'this' to the stack (to become arg0)
                self.context = IdContext(IdCat.VARIABLE, use=VarUse.REF, kind=variable.kind, index=variable.index)
            else:
                raise ValueError(f"A class name or variable name is expected.")
            self.tokenizer.consume(Symbol.DOT)
        # subroutineName '(' expressionList ')'
        # this is a call from the current object 
        else:
            object_call = True
            self.vm_writer.write_push(SEG.POINTER, 0)
            call_name += str(self.class_name)
        self.context = IdContext(IdCat.SUBROUTINE, use=VarUse.REF)
        sub_routine_name = self.tokenizer.consume(Identifier)
        call_name += "."+sub_routine_name
        with self._parentheses():
            n_expr = self._compile_expression_list()
        self.vm_writer.write_call(call_name, n_expr+object_call)

    # ----------------------------------------
    # Compile Helpers (token handling)
    # ----------------------------------------

    @property
    def token(self) -> Token:
        """Alias for the current token from the tokenizer."""
        return self.tokenizer.token

    def _write_label(self,label_id:int):            
        self.vm_writer.write_label(f"{self.class_name}_{label_id}")

    def _write_if(self,label_id:int):            
        self.vm_writer.write_if(f"{self.class_name}_{label_id}")

    def _write_goto(self,label_id:int):            
        self.vm_writer.write_goto(f"{self.class_name}_{label_id}")

    # ------------------------------------------------------------
    # context management helper methods (private)
    # ------------------------------------------------------------
    
    @contextmanager
    def _symbol_context(self, open_symbol: Symbol, close_symbol: Symbol):
        '''Context manager for symbols like {}, (), []'''
        self.tokenizer.consume(open_symbol)
        yield
        self.tokenizer.consume(close_symbol)

    def _braces(self):
        '''Context manager for braces {}'''
        return self._symbol_context(Symbol.LBRACE, Symbol.RBRACE)

    def _parentheses(self):
        '''Context manager for parentheses ()'''
        return self._symbol_context(Symbol.LPAREN, Symbol.RPAREN)

    def _brackets(self):
        '''Context manager for brackets []'''
        return self._symbol_context(Symbol.LBRACK, Symbol.RBRACK)


