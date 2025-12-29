from enum import Enum


class CMDType(Enum):
    """Enum class to represent different command types."""

    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"


class Parser:
    """A class to parse VM commands from a file."""

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
        """Checks if there are more commands to parse."""
        return self.instruction_index < self.n_instructions

    def advance(self) -> bool:
        """Advances to the next command in the instruction list."""
        if self.has_more_commands():
            self.instruction = self.instructions[self.instruction_index]
            self.instruction_index += 1
            self.tokens = self.instruction.split()
            self.keyword = self.tokens[0]
            return True
        return False

    def command_type(self) -> CMDType:
        """Determines the type of the current command."""

        match (len(self.tokens), self.keyword):
            case (1, self.keyword) if self.keyword in {
                "add",
                "sub",
                "neg",
                "eq",
                "gt",
                "lt",
                "and",
                "or",
                "not",
            }:
                return CMDType.C_ARITHMETIC
            case (3, "push"):
                return CMDType.C_PUSH
            case (3, "pop"):
                return CMDType.C_POP
            case _:
                raise ValueError(f"Unknown command type: {self.instruction}")

    def arg1(self) -> str:
        """Return the first argument of the current command."""
        if len(self.tokens) > 1:
            return self.tokens[1]
        raise ValueError("No first argument found.")

    def arg2(self) -> int:
        """Return the second argument of the current command."""
        if len(self.tokens) > 2:
            return int(self.tokens[2])
        raise ValueError("No second argument found.")
