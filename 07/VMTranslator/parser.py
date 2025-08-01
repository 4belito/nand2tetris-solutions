class Parser:
    """
    A class to parse VM commands from a file.
    """

    def __init__(self, filepath: str):
        self.instruction_index = 0
        with open(filepath, "r") as f:
            self.instructions = []
            for line in f:
                cleaned_line = line.split("//")[0].strip()
                if cleaned_line:
                    self.instructions.append(cleaned_line)
        self.n_instructions = len(self.instructions)
        self.instruction = None
        self.tokens = None
        self.keyword = None

    def has_more_commands(self):
        '''Checks if there are more commands to parse.'''
        return self.instruction_index < self.n_instructions

    def advance(self):
        '''Advances to the next command in the instruction list.'''
        if self.has_more_commands():
            self.instruction = self.instructions[self.instruction_index]
            self.instruction_index += 1
            self.tokens = self.instruction.split()
            self.keyword = self.tokens[0]
            return True
        return False

    def command_type(self):
        '''Determines the type of the current command.'''
        if not self.instruction:
            return None

        match (len(self.tokens), self.keyword):
            case (1, self.keyword) if self.keyword in {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}:
                return "C_ARITHMETIC"
            case (3, "push"):
                return "C_PUSH"
            case (3, "pop"):
                return "C_POP"
            case (2, "label"):
                return "C_LABEL"
            case (2, "goto"):
                return "C_GOTO"
            case (2, "if-goto"):
                return "C_IF"
            case (3, "function"):
                return "C_FUNCTION"
            case (3, "call"):
                return "C_CALL"
            case (1, "return"):
                return "C_RETURN"
            case _:
                raise ValueError(f"Unknown command type: {self.instruction}")
            
    def arg1(self):
        '''Returns the first argument of the current command.'''
        if len(self.tokens) > 1:
            return self.tokens[1]
        return None 
    
    def arg2(self):
        '''Returns the second argument of the current command.'''
        if len(self.tokens) > 2:
            return int(self.tokens[2])
        return None
