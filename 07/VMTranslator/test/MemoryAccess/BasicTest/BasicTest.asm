// Assembly code BasicTest.asm

// push constant 10
// get address 10
@10
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

// push constant 21
// get address 21
@21
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 22
// get address 22
@22
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop argument 2
// get address of argument 2
// get value from ARG
@ARG
D=M
// calculate address
@2
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// pop argument 1
// get address of argument 1
// get value from ARG
@ARG
D=M
// calculate address
@1
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push constant 36
// get address 36
@36
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop this 6
// get address of this 6
// get value from THIS
@THIS
D=M
// calculate address
@6
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push constant 42
// get address 42
@42
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 45
// get address 45
@45
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop that 5
// get address of that 5
// get value from THAT
@THAT
D=M
// calculate address
@5
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// pop that 2
// get address of that 2
// get value from THAT
@THAT
D=M
// calculate address
@2
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push constant 510
// get address 510
@510
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop temp 6
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg 11
@11
M=D

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

// push that 5
// get value from THAT
@THAT
D=M
// calculate address
@5
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

// push this 6
// get value from THIS
@THIS
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

// push this 6
// get value from THIS
@THIS
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

// push temp 6
// get value from 11
@11
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
