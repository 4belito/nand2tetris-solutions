"""
parser.py

This module provides the `Parser` class for parsing VM commands and the `CMDType` class for command types.
"""

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

OPERATION_MAP = {
        "add": "+",
        "sub": "-",
        "neg": "-",
        "eq": "JEQ",
        "gt": "JGT",
        "lt": "JLT",
        "and": "&",
        "or": "|",
        "not": "!"
    }

class Parser:
    """
    A class to parse VM commands from a file.
    """

    def __init__(self, filepath: str):
        self.instruction_index = 0
        self.instructions: list[str] = []
        with open(filepath, "r") as f:
            for line in f:
                cleaned_line = line.split("//")[0].strip()
                if cleaned_line:
                    self.instructions.append(cleaned_line)
        self.n_instructions = len(self.instructions)
        self.instruction: str = ""
        self.tokens: list[str] = []
        self.keyword: str = ""

    def has_more_commands(self) -> bool:
        '''Checks if there are more commands to parse.'''
        return self.instruction_index < self.n_instructions

    def advance(self) -> bool:
        '''Advances to the next command in the instruction list.'''
        if self.has_more_commands():
            self.instruction = self.instructions[self.instruction_index]
            self.instruction_index += 1
            self.tokens = self.instruction.split()
            self.keyword = self.tokens[0]
            return True
        return False

    def command_type(self) -> CMD:
        '''Determines the type of the current command.'''

        match (len(self.tokens), self.keyword):
            case (1, self.keyword) if self.keyword in OPERATION_MAP:
                return CMD.ARITHMETIC
            case (3, "push"):
                return CMD.PUSH
            case (3, "pop"):
                return CMD.POP
            case (2, "label"):
                return CMD.LABEL
            case (2, "goto"):
                return CMD.GOTO
            case (2, "if-goto"):
                return CMD.IF_GOTO
            case (3, "function"):
                return CMD.FUNCTION
            case (3, "call"):
                return CMD.CALL
            case (1, "return"):
                return CMD.RETURN
            case _:
                raise ValueError(f"Unknown command type: {self.instruction}")

    def arg1(self) -> str:
        '''Returns the first argument of the current command.'''
        if len(self.tokens) > 1:
            return self.tokens[1]
        raise ValueError("No first argument found.")

    def arg2(self) -> int:
        '''Returns the second argument of the current command.'''
        if len(self.tokens) > 2:
            return int(self.tokens[2])
        raise ValueError("No second argument found.")
