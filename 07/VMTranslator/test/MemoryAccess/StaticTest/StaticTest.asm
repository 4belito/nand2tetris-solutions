//Assembly code for StaticTest.asm

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
// store D in reg StaticTest.asm.8
@StaticTest.asm.8
M=D

// pop static 3
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg StaticTest.asm.3
@StaticTest.asm.3
M=D

// pop static 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg StaticTest.asm.1
@StaticTest.asm.1
M=D

// push static 3
// get value from StaticTest.asm.3
@StaticTest.asm.3
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push static 1
// get value from StaticTest.asm.1
@StaticTest.asm.1
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
// get value from StaticTest.asm.8
@StaticTest.asm.8
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
