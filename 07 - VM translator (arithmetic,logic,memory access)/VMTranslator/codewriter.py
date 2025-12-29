"""
CodeWriter class for translating VM commands to Hack assembly code.
This class handles arithmetic operations, memory access commands, and manages the output file.
It provides methods to write arithmetic operations, push and pop commands, and finalize the assembly code.
"""

import os

from parser import CMDType

TEMP_BASE = 5
WORK_REG = "R13"


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
        "not": "!",
    }
    SEG_MAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

    def __init__(self, output_filepath: str):
        full_file_name = os.path.basename(output_filepath)
        self.file_name = os.path.splitext(full_file_name)[0]
        self.file = open(output_filepath, "w")
        self.bool_counter = 0
        self.file.write("// Assembly code " + full_file_name + "\n")

    def write_arithmetic(self, op: str) -> None:
        """
        Translates the given arithmetic VM command into Hack assembly and writes to file.
        """
        match op:
            case "add" | "sub" | "and" | "or":
                assembly_code = self._arithmetic_operation2(op)
            case "neg" | "not":
                assembly_code = self._arithmetic_operation1(op)
            case "eq" | "gt" | "lt":
                assembly_code = self._arithmetic_compare(op)
            case _:
                raise ValueError(f"Unknown arithmetic command: {op}")
        self.file.write("\n" + assembly_code + "\n")

    def write_push_pop(self, cmd: CMDType, segment: str, index: int) -> None:
        """
        Translates the given push or pop VM command into Hack assembly and writes to file.
        """
        if cmd == CMDType.C_PUSH:
            assembly_code = self._push(segment=segment, index=index)
        elif cmd == CMDType.C_POP:
            assembly_code = self._pop(segment=segment, index=index)
        else:
            raise ValueError(f"Unknown command: {cmd}")
        self.file.write("\n" + assembly_code + "\n")

    def close(self):
        """Close the output file."""
        self.file.close()

    # --- Stack helpers ---
    def _point_last(self) -> str:
        return f"""// get value from stack
@SP
AM=M-1"""

    def _increment(self) -> str:
        return """// increment stack pointer
@SP
M=M+1"""

    def _push_fromD(self) -> str:
        return f"""// push from D
@SP
A=M
M=D
{self._increment()}"""

    def _pop_toD(self) -> str:
        return f"""// pop to D
{self._point_last()}
D=M"""

    def _load_reg_value(self, reg: str) -> str:
        return f"""// get value from {reg}
@{reg}
D=M"""

    def _load_symbolA(self, symbol: int | str) -> str:
        """
        Load into D the address or instruction location of a symbol.
        - If it's a number or predefined symbol, D = symbol (memory address).
        - If it's a label, D = address of the instruction after the label (instruction address).
        """
        return f"""// get address {symbol}
@{symbol}
D=A"""

    def _calculate_address(self, index: int) -> str:
        return f"""// calculate address
@{index}
D=D+A"""

    def _storeD_at_ptr(self, address_reg: str) -> str:
        return f"""// store D in address saved in {address_reg}
@{address_reg}
A=M
M=D"""

    def _storeD(self, reg: str) -> str:
        return f"""// store D in reg {reg}
@{reg}
M=D"""

    # --- Arithmetic helpers ---
    def _arithmetic_compare(self, op: str) -> str:
        # eq, gt, lt
        compare_asm = f"""// {op}
{self._pop_toD()}
{self._point_last()}
D=M-D
@TRUE.{self.bool_counter}
D;{self.ARITH_MAP[op]}
@SP
A=M
M=0
@END.{self.bool_counter}
0;JMP
(TRUE.{self.bool_counter})
@SP
A=M
M=-1
(END.{self.bool_counter})
{self._increment()}"""
        self.bool_counter += 1
        return compare_asm

    def _arithmetic_operation1(self, op: str) -> str:
        # neg, not
        return f"""// {op}
{self._point_last()}
M={self.ARITH_MAP[op]}M
{self._increment()}"""

    def _arithmetic_operation2(self, op: str) -> str:
        if op == "sub":
            operation = "M-D"
        else:
            operation = f"D{self.ARITH_MAP[op]}M"
        # add, sub, and, or
        return f"""// {op}
{self._pop_toD()}
{self._point_last()}
M={operation}
{self._increment()}"""

    # --- Memory helpers ---
    def _pointer_segment(self, index: int) -> str:
        if index == 0:
            segment = "this"
        elif index == 1:
            segment = "that"
        else:
            raise ValueError(f"Invalid pointer index: {index}")
        return segment

    def _pop(self, segment: str, index: int = 0, temp_reg: str = WORK_REG) -> str:
        comment = f"// pop {segment} {index}"
        match segment:
            case "local" | "argument" | "this" | "that":
                assembly_code = f"{comment}\n"
                if index == 0:
                    temp_reg = self.SEG_MAP[segment]
                else:
                    assembly_code += f"""// get address of {segment} {index}
{self._load_reg_value(reg=self.SEG_MAP[segment])}
{self._calculate_address(index=index)}
{self._storeD(reg=temp_reg)}
"""
                assembly_code += f"""// pop to {temp_reg}
{self._pop_toD()}
{self._storeD_at_ptr(address_reg=temp_reg)}"""
                return assembly_code
            case "constant":
                raise ValueError("Cannot pop to constant segment")
            case "static":
                return f"""{comment}
{self._pop_toD()}
{self._storeD(reg=f'{self.file_name}.{index}')}"""
            case "temp":
                return f"""{comment}
{self._pop_toD()}
{self._storeD(reg=f'{TEMP_BASE + index}')}"""
            case "pointer":
                segment_ptr = self._pointer_segment(index)
                return f"""{comment}
{self._pop_toD()}
{self._storeD(reg=f'{self.SEG_MAP[segment_ptr]}')}"""
            case _:
                raise ValueError(f"Unknown segment: {segment}")

    def _push(self, segment: str, index: int) -> str:
        comment = f"// push {segment} {index}"
        match segment:
            case "local" | "argument" | "this" | "that":
                return f"""{comment}
{self._load_reg_value(reg=self.SEG_MAP[segment])}
{self._calculate_address(index=index)}
A=D
D=M
{self._push_fromD()}"""
            case "constant":
                return f"""{comment}
{self._load_symbolA(index)}
{self._push_fromD()}"""
            case "static":
                return f"""{comment}
{self._load_reg_value(reg=f'{self.file_name}.{index}')}
{self._push_fromD()}"""
            case "temp":
                return f"""{comment}
{self._load_reg_value(reg=f'{TEMP_BASE + index}')}
{self._push_fromD()}"""
            case "pointer":
                segment_ptr = self._pointer_segment(index)
                return f"""{comment}
{self._load_reg_value(reg=f'{self.SEG_MAP[segment_ptr]}')}
{self._push_fromD()}"""
            case _:
                raise ValueError(f"Unknown segment: {segment}")
