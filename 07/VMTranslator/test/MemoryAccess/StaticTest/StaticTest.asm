
// push constant 111
// Create value 111
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
// Create value 333
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
// Create value 888
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
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in reg StaticTest.8
@StaticTest.8
M=D


// pop static 3
// pop to D
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in reg StaticTest.3
@StaticTest.3
M=D


// pop static 1
// pop to D
// Get value from stack
@SP
M=M-1
A=M
D=M
// Store D in reg StaticTest.1
@StaticTest.1
M=D


// push static 3
// Get value from StaticTest.3
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
// Get value from StaticTest.1
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

// push static 8
// Get value from StaticTest.8
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