// Assembly code BasicLoop.asm

// Translated from BasicLoop.vm

// push constant 0
// get address 0
@0
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop local 0
// pop to LCL
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in LCL
@LCL
A=M
M=D

// label LOOP
(LOOP)

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

// pop local 0
// pop to LCL
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in LCL
@LCL
A=M
M=D

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

// if-goto LOOP
// pop to D
// get value from stack
@SP
AM=M-1
D=M
@LOOP
D;JNE

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
