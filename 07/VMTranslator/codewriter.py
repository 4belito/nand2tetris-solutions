"""
CodeWriter class for translating VM commands to Hack assembly code.
This class handles arithmetic operations, memory access commands, and manages the output file.
It provides methods to write arithmetic operations, push and pop commands, and finalize the assembly code
"""

import os

class CodeWriter:
    """A class to write Hack assembly code from VM commands."""

    ARITH_MAP = {
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
    SEG_MAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file_name = os.path.basename(filepath)
        self.file = open(filepath, "w")
        self.line_counter = 0

    def writeArithmetic(self, op: str) -> None:
        """
        Translates the given arithmetic VM command into Hack assembly and writes to file.
        """
        match op:
            case "add":
                assembly_code = self._arithmetic_operation2(op="add")
            case "sub":
                assembly_code = self._arithmetic_operation2(op="sub")
            case "neg":
                assembly_code = self._arithmetic_operation1(op="neg")
            case "eq":
                assembly_code = self._arithmetic_compare("eq")
            case "gt":
                assembly_code = self._arithmetic_compare("gt")
            case "lt":
                assembly_code = self._arithmetic_compare("lt")
            case "and":
                assembly_code = self._arithmetic_operation2(op="and")
            case "or":
                assembly_code = self._arithmetic_operation2(op="or")
            case "not":
                assembly_code = self._arithmetic_operation1(op="not")
            case _:
                raise ValueError(f"Unknown arithmetic command: {op}")
        self.file.write(assembly_code + "\n")


    def writePushPop(self, cmd: str, segment: str, index: int) -> None:
        """
        Translates the given push or pop VM command into Hack assembly and writes to file.
        """
        if cmd == "push":
            assembly_code = self._push(segment=segment, index=index)
        elif cmd == "pop":
            assembly_code = self._pop(segment=segment, index=index)
        else:
            raise ValueError(f"Unknown command: {cmd}")
        self.file.write(assembly_code + "\n")


    def close(self):
        '''Finalizes the assembly code by adding an END loop and closes the output file.'''
        self.file.write(self._end() + "\n") 
        self.file.close()


    # --- Stack helpers ---
    def _point_last(self) -> str:
        return f'''// Get value from stack
@SP
M=M-1
A=M'''

    def _increment(self) -> str:
        return '''// increment stack pointer
@SP
M=M+1'''

    def _push_fromD(self) -> str:
        return f'''// push from D
@SP
A=M
M=D
{self._increment()}'''

    def _pop_toD(self) -> str:
        return f'''// pop to D
{self._point_last()}
D=M'''

    def _end(self) -> str:
        return '''// end of execution
(END)
    @END
    0;JMP'''

    # --- Arithmetic helpers ---
    def _arithmetic_compare(self, op: str) -> str:
        # eq, gt, lt
        compare_asm = f'''
// {op}
{self._pop_toD()}
{self._point_last()}
D=M-D
@TRUE{self.line_counter}
D;{self.ARITH_MAP[op]}
@SP
A=M
M=0
@END{self.line_counter}
0;JMP
(TRUE{self.line_counter})
    @SP
    A=M
    M=-1
(END{self.line_counter})
{self._increment()}'''
        self.line_counter += 1
        return compare_asm

    def _arithmetic_operation1(self, op: str) -> str:
        # neg, not
        return f'''
// {op}
{self._point_last()}
M={self.ARITH_MAP[op]}M
{self._increment()}'''

    def _arithmetic_operation2(self, op: str) -> str:
        # add, sub, and, or
        return f'''
// {op}
{self._pop_toD()}
{self._point_last()}
M={'M-D' if op == "sub" else f'D{self.ARITH_MAP[op]}M'}
{self._increment()}'''


    # --- Memory helpers ---
    def _get(self, reg: str) -> str:
        return f'''// Get value from {reg}
@{reg}
D=M'''

    def _pointer_segment(self, index: int) -> str:
        if index == 0:
            segment = 'this'
        elif index == 1:
            segment = 'that'
        else:
            raise ValueError(f"Invalid pointer index: {index}")
        return segment

    def _calculate_address(self, segment: str, index: int) -> str:
        return f'''// Calculate address
{self._get(reg=f'{self.SEG_MAP[segment]}')}
@{index}
D=D+A'''

    def _create_value(self, value: int) -> str:
        return f'''// Create value {value}
@{value}
D=A'''

    def _storeD_inaddress(self, address_reg: str) -> str:
        return f'''// Store D in address saved in {address_reg}
@{address_reg}
A=M
M=D'''

    def _storeD(self, reg: str) -> str:
        return f'''// Store D in reg {reg}
@{reg}
M=D'''

    # --- Memory translation ---
    def _pop(self, segment: str, index: int) -> str:
        comment = f'// pop {segment} {index}'
        match segment:
            case "local" | "argument" | "this" | "that":
                return f'''
{comment}
{self._calculate_address(segment, index)}
{self._storeD(reg="R13")}
{self._pop_toD()}
{self._storeD_inaddress(address_reg="R13")}'''
            case "constant":
                raise ValueError("Cannot pop to constant segment")
            case "static":
                return f'''
{comment}
{self._pop_toD()}
{self._storeD(reg=f'{self.file_name}.{index}')}
'''
            case "temp":
                return f'''
{comment}
{self._pop_toD()}
{self._storeD(reg=f'{5 + index}')}
'''
            case "pointer":
                segment_ptr = self._pointer_segment(index)
                return f'''
{comment}
{self._pop_toD()}
{self._storeD(reg=f'{self.SEG_MAP[segment_ptr]}')}'''
            case _ :
                raise ValueError(f"Unknown segment: {segment}")

    def _push(self, segment: str, index: int) -> str:
        comment = f'// push {segment} {index}'
        match segment:
            case "local" | "argument" | "this" | "that":
                return f'''
{comment}
{self._calculate_address(segment, index)}
A=D
D=M
{self._push_fromD()}'''
            case "constant":
                return f'''
{comment}
{self._create_value(index)}
{self._push_fromD()}'''
            case "static":
                return f'''
{comment}
{self._get(reg=f'{self.file_name}.{index}')}
{self._push_fromD()}'''
            case "temp":
                return f'''
{comment}
{self._get(reg=f'{5 + index}')}
{self._push_fromD()}'''
            case "pointer":
                segment_ptr = self._pointer_segment(index)
                return f'''
{comment}
{self._get(reg=f'{self.SEG_MAP[segment_ptr]}')}
{self._push_fromD()}'''
            case _:
                raise ValueError(f"Unknown segment: {segment}")



