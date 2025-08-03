"""
CodeWriter class for translating VM commands to Hack assembly code.
This class handles arithmetic operations, memory access commands, and manages the output file.
It provides methods to write arithmetic operations, push and pop commands, and finalize the assembly code
"""
import os
from parser import CMDType

TEMP_BASE = 5
WORK_REG = "R13"
FRAME_REG = "R14"
RET_REG = "R15"


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
    
    def __init__(self, output_filepath: str):
        full_file_name = os.path.basename(output_filepath)
        self.file_name = os.path.splitext(full_file_name)[0]
        self.file = open(output_filepath, "w")
        self.bool_counter = 0
        self.return_counter = 0
        self.file.write("// Assembly code " + full_file_name + "\n")
        if self.file_name == "Sys":
            self.write_init()

    def set_file_name(self, file_name: str) -> None:
        """
        Sets the file name for the current VM file being translated.
        This is used for static segment handling.
        """
        self.file_name = file_name
        self.file.write("\n// Translated from " + file_name + ".vm\n")

    def write_init(self):
        """
        Generates the initialization code that sets up the VM.
        """
        vm_code =f'''
// Initialization code
{self._load_symbolA(256)}  // Set SP to 256
{self._storeD("SP")}  // SP = 256
'''
        self.file.write(vm_code)
        self.write_call(function_name="Sys.init", num_args=0)

    def write_arithmetic(self, op: str) -> None:
        """
        Translates the given arithmetic VM command into Hack assembly and writes to file.
        """
        match op:
            case "add"| "sub"| "and" | "or":
                assembly_code = self._arithmetic_operation2(op)
            case "neg" | "not":
                assembly_code = self._arithmetic_operation1(op)
            case "eq"| "gt" | "lt":
                assembly_code = self._arithmetic_compare(op)
            case _:
                raise ValueError(f"Unknown arithmetic command: {op}")
        self.file.write("\n" + assembly_code + "\n")


    def write_push_pop(self, cmd: str, segment: str, index: int) -> None:
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

    def write_label(self, label: str) -> None:
        """
        Translates the label VM command into Hack assembly and writes to file.
        """
        self.file.write("\n" + self._label(label) + "\n")    

    def write_goto(self, label: str) -> None:
        """
        Translates the goto VM command into Hack assembly and writes to file.
        """
        self.file.write("\n" + self._goto(label) + "\n")

    def write_if(self, label: str) -> None:
        """Translates the if-goto VM command into Hack assembly and writes to file.
        """
        self.file.write("\n" + self._if_goto(label) + "\n")  

    def write_function(self, function_name: str, num_locals: int) -> None:
        """
        Translates the given function VM command into Hack assembly and writes to file.
        Initializes local variables to 0.
        """
        assembly_code = f'// function {function_name} {num_locals}\n'
        assembly_code += f'({function_name})\n'
        push0='D=0\n' + f'{self._push_fromD()}\n'
        assembly_code += num_locals*push0
        self.file.write("\n" + assembly_code)

    def write_call(self, function_name: str, num_args: int) -> None:
        """
        Translates the given call VM command into Hack assembly and writes to file.
        """
        return_label = f'return_{function_name}$ret.{self.return_counter}'
        self.return_counter += 1
        assembly_code = f'''// call {function_name} {num_args}
{self._push_label(return_label)} 
{self._push_from_reg("LCL")} 
{self._push_from_reg("ARG")} 
{self._push_from_reg("THIS")} 
{self._push_from_reg("THAT")} 
{self._reposition_ARG(num_args)}
{self._reposition_LCL()}
{self._goto(label=function_name)}
({return_label})'''
        
        self.file.write("\n" + assembly_code + "\n")

    def write_return(self) -> None:
        """
        Translates the return VM command into Hack assembly and writes to file.
        It restores the caller's state and returns control to the caller.
        """
        assembly_code = f'''// return
{self._load_reg_value(reg="LCL")}
{self._storeD(reg=FRAME_REG)}
{self._compute_return_address()}
{self._storeD(RET_REG)}            // R15 = RET
{self._pop(segment="argument")}
{self._reposition_SP()}
{self._restore_from_frame(frame_reg=FRAME_REG,store_reg="THAT")}
{self._restore_from_frame(frame_reg=FRAME_REG,store_reg="THIS")}
{self._restore_from_frame(frame_reg=FRAME_REG,store_reg="ARG")}
{self._restore_from_frame(frame_reg=FRAME_REG,store_reg="LCL")}
{self._goto_at_ptr(address_reg=RET_REG)}'''
        self.file.write("\n" + assembly_code + "\n")
        
    def close(self):
        '''Close the output file.'''
        self.file.close()

# --- Stack helpers ---
    def _point_last(self) -> str:
        return f'''// get value from stack
@SP
AM=M-1'''

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
    
    def _load_reg_value(self, reg: str) -> str:
        return f'''// get value from {reg}
@{reg}
D=M'''

    def _load_symbolA(self, symbol: int|str) -> str:
        """Load into D the address or instruction location of a symbol.
        - If it's a number or predefined symbol, D = symbol (memory address).
        - If it's a label, D = address of the instruction after the label (instruction address).
        """
        return f'''// get address {symbol}
@{symbol}
D=A'''

    def _calculate_address(self, index: int) -> str:
        return f'''// calculate address
@{index}
D=D+A'''
    
    def _storeD_at_ptr(self, address_reg: str) -> str:
        return f'''// store D in address saved in {address_reg}
@{address_reg}
A=M
M=D'''

    def _storeD(self, reg: str) -> str:
        return f'''// store D in reg {reg}
@{reg}
M=D'''
    
# --- Arithmetic helpers ---
    def _arithmetic_compare(self, op: str) -> str:
        # eq, gt, lt
        compare_asm = f'''// {op}
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
{self._increment()}'''
        self.bool_counter += 1
        return compare_asm

    def _arithmetic_operation1(self, op: str) -> str:
        # neg, not
        return f'''// {op}
{self._point_last()}
M={self.ARITH_MAP[op]}M
{self._increment()}'''

    def _arithmetic_operation2(self, op: str) -> str:
        if op == "sub":
            operation = "M-D"
        else:
            operation = f"D{self.ARITH_MAP[op]}M"
        # add, sub, and, or
        return f'''// {op}
{self._pop_toD()}
{self._point_last()}
M={operation}
{self._increment()}'''


# --- Memory helpers ---
    def _pointer_segment(self, index: int) -> str:
        if index == 0:
            segment = 'this'
        elif index == 1:
            segment = 'that'
        else:
            raise ValueError(f"Invalid pointer index: {index}")
        return segment

    def _pop(self, segment: str, index: int = 0, temp_reg: str = WORK_REG) -> str:
        comment = f'// pop {segment} {index}'
        match segment:
            case "local" | "argument" | "this" | "that":
                assembly_code = f'{comment}\n'
                if index == 0:
                    temp_reg = self.SEG_MAP[segment]
                else:
                    assembly_code += f'''// get address of {segment} {index}
{self._load_reg_value(reg=self.SEG_MAP[segment])}
{self._calculate_address(index=index)}
{self._storeD(reg=temp_reg)}
'''
                assembly_code += f'''// pop to {temp_reg}
{self._pop_toD()}
{self._storeD_at_ptr(address_reg=temp_reg)}'''
                return assembly_code
            case "constant":
                raise ValueError("Cannot pop to constant segment")
            case "static":
                return f'''{comment}
{self._pop_toD()}
{self._storeD(reg=f'{self.file_name}.{index}')}'''
            case "temp":
                return f'''{comment}
{self._pop_toD()}
{self._storeD(reg=f'{TEMP_BASE + index}')}'''
            case "pointer":
                segment_ptr = self._pointer_segment(index)
                return f'''{comment}
{self._pop_toD()}
{self._storeD(reg=f'{self.SEG_MAP[segment_ptr]}')}'''
            case _:
                raise ValueError(f"Unknown segment: {segment}")

    def _push(self, segment: str, index: int) -> str:
        comment = f'// push {segment} {index}'
        match segment:
            case "local" | "argument" | "this" | "that":
                return f'''{comment}
{self._load_reg_value(reg=self.SEG_MAP[segment])}
{self._calculate_address(index=index)}
A=D
D=M
{self._push_fromD()}'''
            case "constant":
                return f'''{comment}
{self._load_symbolA(index)}
{self._push_fromD()}'''
            case "static":
                return f'''{comment}
{self._load_reg_value(reg=f'{self.file_name}.{index}')}
{self._push_fromD()}'''
            case "temp":
                return f'''{comment}
{self._load_reg_value(reg=f'{TEMP_BASE + index}')}
{self._push_fromD()}'''
            case "pointer":
                segment_ptr = self._pointer_segment(index)
                return f'''{comment}
{self._load_reg_value(reg=f'{self.SEG_MAP[segment_ptr]}')}
{self._push_fromD()}'''
            case _:
                raise ValueError(f"Unknown segment: {segment}")
            
# --- Branching helpers ---
    def _label(self, label: str) -> str:
        """
        Translates a label command into Hack assembly.
        """
        return f'''// label {label}
({label})'''
    
    def _goto(self, label: str) -> str:
        """
        Translates a goto command into Hack assembly.
        """
        return f'''// goto {label}
@{label}
0;JMP'''

    def _if_goto(self, label: str) -> str:
        """
        Translates an if-goto command into Hack assembly.
        """
        return f'''// if-goto {label}
{self._pop_toD()}
@{label}
D;JNE'''    

# --- function helpers ---
    def _goto_at_ptr(self, address_reg: str) -> str:
        """
        Get the address stored in the given register and jump to it.
        """
        return f'''@{address_reg}
A=M
0;JMP'''
    
    def _dec_and_load_from(self, reg: str) -> str:
        """
        Decrease the value of the given register by 1.
        """
        return f'''@{reg}
AM=M-1
D=M'''

    def _restore_from_frame(self, frame_reg: str, store_reg: str) -> str:
        """
        Get the address of the frame less 1 and store it in the given register.
        """
        return f'''{self._dec_and_load_from(frame_reg)}
{self._storeD(store_reg)}'''

    def _push_from_reg(self, reg: str) -> str:
        """
        Push a register content onto the stack.
        """
        return f'''// push register {reg}
{self._load_reg_value(reg=reg)}
{self._push_fromD()}'''

    def _push_label(self, label: str) -> str:
        """
        Push a label (address) onto the stack.
        """
        return f'''// push label {label}
{self._load_symbolA(label)}
{self._push_fromD()}'''

    def _reposition_ARG(self, num_args: int) -> str:
        """
        Update the ARG register after a function call.
        """
        return f'''// update ARG after call
{self._load_reg_value("SP")}
@5
D=D-A
@{num_args}
D=D-A
{self._storeD(reg="ARG")}'''

    def _reposition_LCL(self) -> str:
        """
        Update the LCL register to point to the current stack pointer.
        """
        return f'''// update LCL
{self._load_reg_value("SP")}
{self._storeD(reg="LCL")}'''
    
    def _compute_return_address(self) -> str:
        """
        Save the return address for a function call.
        """
        return f'''// save return address
@5
A=D-A
D=M'''    
    def _reposition_SP(self) -> str:
        """
        Reposition the stack pointer after a function call.
        """
        return f'''// reposition SP
@ARG
D=M+1
{self._storeD("SP")}            // SP = ARG + 1''' 

