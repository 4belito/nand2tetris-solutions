//Assembly code for PointerTest.asm

// push constant 3030
// get address 3030
@3030
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D

// push constant 3040
// get address 3040
@3040
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D

// push constant 32
// get address 32
@32
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop this 2
// get address of this 2
// get value from THIS
@THIS
D=M
// calculate address
@2
D=D+A
// store D in reg R13
@R13
M=D // pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push constant 46
// get address 46
@46
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop that 6
// get address of that 6
// get value from THAT
@THAT
D=M
// calculate address
@6
D=D+A
// store D in reg R13
@R13
M=D // pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push pointer 0
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

// push pointer 1
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

// push this 2
// get value from THIS
@THIS
D=M
// calculate address
@2
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

// push that 6
// get value from THAT
@THAT
D=M
// calculate address
@6
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
