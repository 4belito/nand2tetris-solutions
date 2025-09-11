from enum import Enum
from typing import TextIO
from contextlib import contextmanager
from symbol_table import VarK
from itertools import count

class SEGMENT(Enum):
    """Enum class to represent different memory segments."""
    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

class ARITHMETIC_CMD(Enum):
    """Enum class to represent different arithmetic commands."""
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

class VMWriter:
    ident = 4
    def __init__(self, output_file: str):
        self._output_file = output_file
        self._f: TextIO
        self.golabel_id: count[int] = count(start=0, step=2)
        self.iflabel_id: count[int] = count(start=1, step=2)

    def write_push(self, segment: SEGMENT, index: int):
        self.write(f"push {segment.value} {index}")

    def write_pop(self, segment: SEGMENT, index: int):
        self.write(f"pop {segment.value} {index}")

    def write_arithmetic(self, command: ARITHMETIC_CMD):
        self.write(f"{command.value}")

    def write_label(self, label: str):
        self.write(f"label {label}", indent=False)

    def write_goto(self, label: str):
        self.write(f"goto {label}")

    def write_if(self, label: str):
        self.write(f"if-goto {label}")

    def write_call(self, name: str, n_args: int):
        self.write(f"call {name} {n_args}")

    def write_function(self, name: str, n_locals: int):
        self.write(f"function {name} {n_locals}", indent=False)

    def write_return(self):
        self.write(f"return")

    ## NO API METHODS BELOW THIS LINE ##
    @contextmanager
    def open(self):
        self._f = open(self._output_file, 'w')
        yield
        self._f.flush()
        self._f.seek(0, 2)
        if self._f.tell() > 0:
            self._f.truncate(self._f.tell() - 1)  
        self._f.close()

    def write(self,command:str,indent:bool=True):
        if indent:
            command = f"{' ' * self.ident}{command}"
        self._f.write(command+'\n')

    def write_constructor_alloc(self, n_fields: int):                    
        self.write_push(SEGMENT.CONST, n_fields)
        self.write_call("Memory.alloc", 1)
        self.write_pop(SEGMENT.POINTER, 0)
        # Alternative implementation without using SEGMENT enum
    
    def write_method_setup(self):
        self.write_push(SEGMENT.ARG, 0)
        self.write_pop(SEGMENT.POINTER, 0)

    def write_push_array_element_address(self, var_kind: VarK, var_idx: int):
        """push the array element address in the stack
        assuming the index is in the top of stack."""
        self.write_push(SEGMENT[var_kind.name], var_idx)
        self.write_arithmetic(ARITHMETIC_CMD.ADD)

    def write_push_array_element(self, var_kind: VarK, var_idx: int):
        """push the array element in the stack
        assuming the array index is in the top of stack."""
        self.write_push_array_element_address(var_kind, var_idx)
        self.write_pop(SEGMENT.POINTER, 1)  # put address in the "that" pointer
        self.write_push(SEGMENT.THAT, 0)  # push the value of 'that'  

    def write_assign_to_array_element(self):
        '''Assign to an array element.
        Assumes the value to be assigned is at the top of the stack,
        and the array element address is the second element in the stack.'''
        self.write_pop(SEGMENT.TEMP, 0)  # store the value to be assigned in temp 0
        self.write_pop(SEGMENT.POINTER, 1)  # put the array element address in the "that" pointer
        self.write_push(SEGMENT.TEMP, 0)  # push the value to be assigned in the stack
        self.write_pop(SEGMENT.THAT, 0)  # put the value to be assigned in the array element



    def write_string_constant(self, string: str):
        """Write VM code to create a string constant."""
        self.write_push(SEGMENT.CONST, len(string))
        self.write_call("String.new", 1)
        for char in string:
            self.write_push(SEGMENT.CONST, ord(char))
            self.write_call("String.appendChar", 2)
