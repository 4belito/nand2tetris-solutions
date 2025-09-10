from enum import Enum
from typing import TextIO
from contextlib import contextmanager

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
        self._f.close()

    def write(self,command:str,indent:bool=True):
        if indent:
            command = f"{' ' * self.ident}{command}"
        self._f.write(command+'\n')

