
// push constant 10
// Create value 10
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

// push constant 21
// Create value 21
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
// Create value 22
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
// Calculate address
// Get value from ARG
@ARG
D=M
@2
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

// pop argument 1
// Calculate address
// Get value from ARG
@ARG
D=M
@1
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

// push constant 36
// Create value 36
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
// Calculate address
// Get value from THIS
@THIS
D=M
@6
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

// push constant 42
// Create value 42
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
// Create value 45
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
// Calculate address
// Get value from THAT
@THAT
D=M
@5
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

// pop that 2
// Calculate address
// Get value from THAT
@THAT
D=M
@2
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

// push constant 510
// Create value 510
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
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in reg 11
@11
M=D


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

// push that 5
// Calculate address
// Get value from THAT
@THAT
D=M
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

// push argument 1
// Calculate address
// Get value from ARG
@ARG
D=M
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

// push this 6
// Calculate address
// Get value from THIS
@THIS
D=M
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
// Calculate address
// Get value from THIS
@THIS
D=M
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

// push temp 6
// Get value from 11
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
// end of execution
(END)
    @END
    0;JMP