
// push constant 17
// Create value 17
@17
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 17
// Create value 17
@17
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// eq
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
D=M-D
@TRUE2
D;JEQ
@SP
A=M
M=0
@END2
0;JMP
(TRUE2)
    @SP
    A=M
    M=-1
(END2)
// increment stack pointer
@SP
M=M+1

// push constant 17
// Create value 17
@17
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 16
// Create value 16
@16
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// eq
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
D=M-D
@TRUE5
D;JEQ
@SP
A=M
M=0
@END5
0;JMP
(TRUE5)
    @SP
    A=M
    M=-1
(END5)
// increment stack pointer
@SP
M=M+1

// push constant 16
// Create value 16
@16
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 17
// Create value 17
@17
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// eq
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
D=M-D
@TRUE8
D;JEQ
@SP
A=M
M=0
@END8
0;JMP
(TRUE8)
    @SP
    A=M
    M=-1
(END8)
// increment stack pointer
@SP
M=M+1

// push constant 892
// Create value 892
@892
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 891
// Create value 891
@891
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// lt
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
D=M-D
@TRUE11
D;JLT
@SP
A=M
M=0
@END11
0;JMP
(TRUE11)
    @SP
    A=M
    M=-1
(END11)
// increment stack pointer
@SP
M=M+1

// push constant 891
// Create value 891
@891
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 892
// Create value 892
@892
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// lt
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
D=M-D
@TRUE14
D;JLT
@SP
A=M
M=0
@END14
0;JMP
(TRUE14)
    @SP
    A=M
    M=-1
(END14)
// increment stack pointer
@SP
M=M+1

// push constant 891
// Create value 891
@891
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 891
// Create value 891
@891
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// lt
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
D=M-D
@TRUE17
D;JLT
@SP
A=M
M=0
@END17
0;JMP
(TRUE17)
    @SP
    A=M
    M=-1
(END17)
// increment stack pointer
@SP
M=M+1

// push constant 32767
// Create value 32767
@32767
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 32766
// Create value 32766
@32766
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// gt
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
D=M-D
@TRUE20
D;JGT
@SP
A=M
M=0
@END20
0;JMP
(TRUE20)
    @SP
    A=M
    M=-1
(END20)
// increment stack pointer
@SP
M=M+1

// push constant 32766
// Create value 32766
@32766
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 32767
// Create value 32767
@32767
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// gt
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
D=M-D
@TRUE23
D;JGT
@SP
A=M
M=0
@END23
0;JMP
(TRUE23)
    @SP
    A=M
    M=-1
(END23)
// increment stack pointer
@SP
M=M+1

// push constant 32766
// Create value 32766
@32766
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 32766
// Create value 32766
@32766
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// gt
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
D=M-D
@TRUE26
D;JGT
@SP
A=M
M=0
@END26
0;JMP
(TRUE26)
    @SP
    A=M
    M=-1
(END26)
// increment stack pointer
@SP
M=M+1

// push constant 57
// Create value 57
@57
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 31
// Create value 31
@31
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 53
// Create value 53
@53
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

// push constant 112
// Create value 112
@112
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

// neg
// Get value from stack
@SP
M=M-1
A=M
M=-M
// increment stack pointer
@SP
M=M+1

// and
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
M=D&M
// increment stack pointer
@SP
M=M+1

// push constant 82
// Create value 82
@82
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// or
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
M=D|M
// increment stack pointer
@SP
M=M+1

// not
// Get value from stack
@SP
M=M-1
A=M
M=!M
// increment stack pointer
@SP
M=M+1
// end of execution
(END)
    @END
    0;JMP