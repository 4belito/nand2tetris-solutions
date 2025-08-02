//Assembly code for FibonacciSeries.asm

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

// pop pointer 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D

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

// pop that 0
 // pop to THAT
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in THAT
@THAT
A=M
M=D

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

// pop that 1
// get address of that 1
// get value from THAT
@THAT
D=M
// calculate address
@1
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

// if-goto COMPUTE_ELEMENT
// pop to D
// get value from stack
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D;JNE

// goto END
@END
0;JMP

// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)

// push that 0
// get value from THAT
@THAT
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

// push that 1
// get value from THAT
@THAT
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

// pop pointer 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THAT
@THAT
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

// goto LOOP
@LOOP
0;JMP

// label END
(END)
