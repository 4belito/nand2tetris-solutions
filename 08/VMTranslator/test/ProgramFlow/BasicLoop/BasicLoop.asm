
// push constant 0
// Create value 0
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
// Calculate address
// Get value from LCL
@LCL
D=M
@0
D=D+A
// Store D in reg R13
@R13
M=D
// pop to D
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in address saved in R13
@R13
A=M
M=D

(LOOP)

// push argument 0
// Calculate address
// Get value from ARG
@ARG
D=M
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
// Calculate address
// Get value from LCL
@LCL
D=M
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
// Get value from stack
@SP
M=M-1
A=M
D=M
// Get value from stack
@SP
M=M-1
A=M
M=D+M
// increment stack pointer
@SP
M=M+1

// pop local 0
// Calculate address
// Get value from LCL
@LCL
D=M
@0
D=D+A
// Store D in reg R13
@R13
M=D
// pop to D
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in address saved in R13
@R13
A=M
M=D

// push argument 0
// Calculate address
// Get value from ARG
@ARG
D=M
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
// Create value 1
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
// Get value from stack
@SP
M=M-1
A=M
D=M
// Get value from stack
@SP
M=M-1
A=M
M=M-D
// increment stack pointer
@SP
M=M+1

// pop argument 0
// Calculate address
// Get value from ARG
@ARG
D=M
@0
D=D+A
// Store D in reg R13
@R13
M=D
// pop to D
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in address saved in R13
@R13
A=M
M=D

// push argument 0
// Calculate address
// Get value from ARG
@ARG
D=M
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
// Get value from stack
@SP
M=M-1
A=M
D=M
@LOOP
D;JNE

// push local 0
// Calculate address
// Get value from LCL
@LCL
D=M
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
// end of execution
(END)
    @END
    0;JMP
