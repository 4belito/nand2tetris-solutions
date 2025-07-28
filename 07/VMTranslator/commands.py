"""
CMDS: Provides translation of VM commands into Hack assembly code.
"""
from abc import ABC, abstractmethod

class CMD(ABC):

    @abstractmethod
    def translate(self, **arg) -> str:
        pass

    def point_last(self) -> str:
        return f'''// Get value from stack
@SP
M=M-1
A=M'''
    
    def increment(self) -> str:
        return '''// increment stack pointer
@SP
M=M+1'''

    def push_fromD(self) -> str:
        return f'''// push from D
@SP
A=M
M=D
{self.increment()}'''

    def pop_toD(self) -> str:
        return f'''// pop to D
{self.point_last()}
D=M'''
    
    def end(self) -> str:
        return '''// end of execution
(END)
    @END
    0;JMP'''

class Arithmetic(CMD):

    MAP = {
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

    def compare(self, op: str, line_num:int) -> str:
        return f'''
// {op}
{self.pop_toD()}
{self.point_last()}
D=M-D
@TRUE{line_num}
D;{self.MAP[op]}
@SP
A=M
M=0
@END{line_num}
0;JMP
(TRUE{line_num})
    @SP
    A=M
    M=-1
(END{line_num})
{self.increment()}'''
    
    def operation1(self, op: str) -> str:
        return f'''
// {op}
{self.point_last()}
M={self.MAP[op]}M
{self.increment()}'''

    def operation2(self, op: str) -> str:
        return f'''
// {op}
{self.pop_toD()}
{self.point_last()}
M={'M-D' if op == "sub" else f'D{self.MAP[op]}M'}
{self.increment()}'''

    def translate(self, op: str, line_num: int) -> str:
        match op:
            case "add":
                return self.operation2(op="add")
            case "sub":
                return self.operation2(op="sub")
            case "neg":
                return self.operation1(op="neg")
            case "eq":
                return self.compare("eq", line_num)
            case "gt":
                return self.compare("gt", line_num)
            case "lt":
                return self.compare("lt", line_num)
            case "and":
                return self.operation2(op="and")
            case "or":
                return self.operation2(op="or")
            case "not":
                return self.operation1(op="not")
            case _:
                raise ValueError(f"Unknown arithmetic command: {op}")

class Memory(CMD):
    MAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
    
    def __init__(self,file_name:str):
        self.file_name = file_name

    def translate(self, cmd:str,segment: str, index: int) -> str:
        if cmd == "push":
            return self.push(segment=segment, index=index)
        elif cmd == "pop":
            return self.pop(segment=segment, index=index)
        else:
            raise ValueError(f"Unknown command: {cmd}")

    def get(self,reg: str) -> str:
        return f'''// Get value from {reg}
@{reg}
D=M'''
    
    def pointer_segment(self, index: int) -> str:
        if index == 0:
            segment = 'this'
        elif index == 1:
            segment = 'that'
        else:
            raise ValueError(f"Invalid pointer index: {index}")
        return segment

    def calculate_address(self, segment: str, index: int) -> str:
        return f'''// Calculate address
{self.get(reg=f'{self.MAP[segment]}')}
@{index}
D=D+A'''

    def create_value(self, value: int) -> str:
        return f'''// Create value {value}
@{value}
D=A'''

    def storeD_inaddress(self, address_reg: str) -> str:
        return f'''// Store D in address saved in {address_reg}
@{address_reg}
A=M
M=D'''
    
    def storeD(self, reg: str) -> str:
        return f'''// Store D in reg {reg}
@{reg}
M=D'''


    def pop(self, segment: str, index: int) -> str:
        comment = f'// pop {segment} {index}'
        match segment:
            case "local" | "argument" | "this" | "that":
                return f'''
{comment}
{self.calculate_address(segment, index)}
{self.storeD(reg="R13")}
{self.pop_toD()}
{self.storeD_inaddress(address_reg="R13")}'''
            case "constant":
                raise ValueError("Cannot pop to constant segment")
            case "static":
                return f'''
{comment}
{self.pop_toD()}
{self.storeD(reg=f'{self.file_name}.{index}')}
'''
            case "temp":
                return f'''
{comment}
{self.pop_toD()}
{self.storeD(reg=f'{5 + index}')}
'''
            case "pointer":
                segment = self.pointer_segment(index)
                return f'''
{comment}
{self.pop_toD()}
{self.storeD(reg=f'{self.MAP[segment]}')}'''

            case _ :
                raise ValueError(f"Unknown segment: {segment}")


    def push(self, segment: str, index: int) -> str:
        comment = f'// push {segment} {index}'
        match segment:
            case "local" | "argument" | "this" | "that":
               return f'''
{comment}
{self.calculate_address(segment, index)}
A=D
D=M
{self.push_fromD()}'''
            case "constant":
                return f'''
{comment}
{self.create_value(index)}
{self.push_fromD()}'''

            case "static":
                return f'''
{comment}
{self.get(reg=f'{self.file_name}.{index}')}
{self.push_fromD()}'''
            case "temp":
                return f'''
{comment}
{self.get(reg=f'{5 + index}')}
{self.push_fromD()}'''

            case "pointer":
                segment = self.pointer_segment(index)
                return f'''
{comment}
{self.get(reg=f'{self.MAP[segment]}')}
{self.push_fromD()}'''
            
            case _:
                raise ValueError(f"Unknown segment: {segment}")
