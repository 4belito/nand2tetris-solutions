

from enum import Enum


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
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.commands: list[str] = []

    def write_push(self, segment: SEGMENT, index: int):
        self.commands.append(f"push {segment.value} {index}")

    def write_pop(self, segment: SEGMENT, index: int):
        self.commands.append(f"pop {segment.value} {index}")

    def write_arithmetic(self, command: ARITHMETIC_CMD):
        self.commands.append(command.value)

    def write_label(self, label: str):  
        self.commands.append(f"label {label}")

    def write_goto(self, label: str):
        self.commands.append(f"goto {label}")
    
    def write_if(self, label: str):
        self.commands.append(f"if-goto {label}")

    def write_call(self, name: str, n_args: int):
        self.commands.append(f"call {name} {n_args}")

    def write_function(self, name: str, n_locals: int):
        self.commands.append(f"function {name} {n_locals}")

    def write_return(self):
        self.commands.append("return")

    def close(self):
        with open(self.output_file, 'w') as f:
            f.write("\n".join(self.commands))
