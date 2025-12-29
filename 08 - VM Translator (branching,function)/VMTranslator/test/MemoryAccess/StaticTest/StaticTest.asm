// Assembly code StaticTest.asm

// Translated from StaticTest.vm

// push constant 111
// get address 111
@111
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 333
// get address 333
@333
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 888
// get address 888
@888
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop static 8
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg StaticTest.8
@StaticTest.8
M=D

// pop static 3
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg StaticTest.3
@StaticTest.3
M=D

// pop static 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg StaticTest.1
@StaticTest.1
M=D

// push static 3
// get value from StaticTest.3
@StaticTest.3
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push static 1
// get value from StaticTest.1
@StaticTest.1
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

// push static 8
// get value from StaticTest.8
@StaticTest.8
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
