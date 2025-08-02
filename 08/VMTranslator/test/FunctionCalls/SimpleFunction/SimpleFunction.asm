//Assembly code for SimpleFunction.asm

// function SimpleFunction.test 2
(SimpleFunction.test)
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push local 0
// get value from LCL
@LCL
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

// push local 1
// get value from LCL
@LCL
D=M
// calculate address
@1
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


// not
// get value from stack
@SP
AM=M-1
M=!M
// increment stack pointer
@SP
M=M+1

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

// push argument 1
// get value from ARG
@ARG
D=M
// calculate address
@1
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
