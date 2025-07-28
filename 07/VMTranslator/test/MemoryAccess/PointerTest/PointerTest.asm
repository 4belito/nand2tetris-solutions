
// push constant 3030
// Create value 3030
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
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in reg THIS
@THIS
M=D

// push constant 3040
// Create value 3040
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
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in reg THAT
@THAT
M=D

// push constant 32
// Create value 32
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
// Calculate address
// Get value from THIS
@THIS
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

// push constant 46
// Create value 46
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
// Calculate address
// Get value from THAT
@THAT
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

// push pointer 0
// Get value from THIS
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
// Get value from THAT
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

// push this 2
// Calculate address
// Get value from THIS
@THIS
D=M
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

// push that 6
// Calculate address
// Get value from THAT
@THAT
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
// end of execution
(END)
    @END
    0;JMP