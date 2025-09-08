// Assembly code Main.asm

// Translated from Main.vm

// function Main.fibonacci 0
(Main.fibonacci)

// push argument 0
// get value from ARG
@ARG
D=M
// calculate address
@0
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 2
// get address 2
@2
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// lt
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.0
D;JLT
@SP
A=M
M=0
@END.0
0;JMP
(TRUE.0)
@SP
A=M
M=-1
(END.0)
// increment stack pointer
@SP
M=M+1

// if-goto N_LT_2
// pop to D
// get value from stack
@SP
AM=M-1
D=M
@N_LT_2
D;JNE

// goto N_GE_2
@N_GE_2
0;JMP

// label N_LT_2
(N_LT_2)

// push argument 0
// get value from ARG
@ARG
D=M
// calculate address
@0
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// return
// get value from LCL
@LCL
D=M
// store D in reg R14
@R14
M=D
// save return address
@5
A=D-A
D=M
// store D in reg R15
@R15
M=D            // R15 = RET
// pop argument 0
// pop to ARG
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in ARG
@ARG
A=M
M=D
// reposition SP
@ARG
D=M+1
// store D in reg SP
@SP
M=D            // SP = ARG + 1
@R14
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D
@R14
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D
@R14
AM=M-1
D=M
// store D in reg ARG
@ARG
M=D
@R14
AM=M-1
D=M
// store D in reg LCL
@LCL
M=D
@R15
A=M
0;JMP

// label N_GE_2
(N_GE_2)

// push argument 0
// get value from ARG
@ARG
D=M
// calculate address
@0
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 2
// get address 2
@2
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// sub
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=M-D
// increment stack pointer
@SP
M=M+1

// call Main.fibonacci 1
// push label return_Main.fibonacci$ret.0
// get address return_Main.fibonacci$ret.0
@return_Main.fibonacci$ret.0
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@1
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP
(return_Main.fibonacci$ret.0)

// push argument 0
// get value from ARG
@ARG
D=M
// calculate address
@0
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 1
// get address 1
@1
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// sub
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=M-D
// increment stack pointer
@SP
M=M+1

// call Main.fibonacci 1
// push label return_Main.fibonacci$ret.1
// get address return_Main.fibonacci$ret.1
@return_Main.fibonacci$ret.1
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@1
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP
(return_Main.fibonacci$ret.1)

// add
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D+M
// increment stack pointer
@SP
M=M+1

// return
// get value from LCL
@LCL
D=M
// store D in reg R14
@R14
M=D
// save return address
@5
A=D-A
D=M
// store D in reg R15
@R15
M=D            // R15 = RET
// pop argument 0
// pop to ARG
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in ARG
@ARG
A=M
M=D
// reposition SP
@ARG
D=M+1
// store D in reg SP
@SP
M=D            // SP = ARG + 1
@R14
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D
@R14
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D
@R14
AM=M-1
D=M
// store D in reg ARG
@ARG
M=D
@R14
AM=M-1
D=M
// store D in reg LCL
@LCL
M=D
@R15
A=M
0;JMP

// Translated from Sys.vm

// function Sys.init 0
(Sys.init)

// push constant 4
// get address 4
@4
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// call Main.fibonacci 1
// push label return_Main.fibonacci$ret.2
// get address return_Main.fibonacci$ret.2
@return_Main.fibonacci$ret.2
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@1
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP
(return_Main.fibonacci$ret.2)

// label END
(END)

// goto END
@END
0;JMP
