from enum import Enum
from typing import TextIO
from contextlib import contextmanager

class CMD(Enum):
    """Enum class to represent different command types."""
    ARITHMETIC = "ARITHMETIC"
    PUSH = "PUSH"
    POP = "POP"
    LABEL = "LABEL"
    GOTO = "GOTO"
    IF_GOTO = "IF_GOTO"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    CALL = "CALL"

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
        self.output_file = output_file
        self.f: TextIO

    def write_push(self, segment: SEGMENT, index: int):
        self.write(f"{' ' * self.ident}push {segment.value} {index}")

    def write_pop(self, segment: SEGMENT, index: int):
        self.write(f"{' ' * self.ident}pop {segment.value} {index}")

    def write_arithmetic(self, command: ARITHMETIC_CMD):
        self.write(f"{' ' * self.ident}{command.value}")

    def write_label(self, label: str):
        self.write(f"label {label}")

    def write_goto(self, label: str):
        self.write(f"{' ' * self.ident}goto {label}")

    def write_if(self, label: str):
        self.write(f"{' ' * self.ident}if-goto {label}")

    def write_call(self, name: str, n_args: int):
        self.write(f"{' ' * self.ident}call {name} {n_args}")

    def write_function(self, name: str, n_locals: int):
        self.write(f"function {name} {n_locals}")

    def write_return(self):
        self.write(f"{' ' * self.ident}return")

    @contextmanager
    def open(self):
        self.f = open(self.output_file, 'w')
        yield
        self.f.close()

    def write(self,command:str):
        self.f.write(command+'\n')

