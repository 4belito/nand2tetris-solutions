// Assembly code StackTest.asm

// Translated from StackTest.vm

// push constant 17
// get address 17
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
// get address 17
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.0
D;JEQ
@SP
A=M
M=0
@END.0
0;JMP
(TRUE.0)
@SP
A=M
M=-1
(END.0)
// increment stack pointer
@SP
M=M+1

// push constant 17
// get address 17
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
// get address 16
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.1
D;JEQ
@SP
A=M
M=0
@END.1
0;JMP
(TRUE.1)
@SP
A=M
M=-1
(END.1)
// increment stack pointer
@SP
M=M+1

// push constant 16
// get address 16
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
// get address 17
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.2
D;JEQ
@SP
A=M
M=0
@END.2
0;JMP
(TRUE.2)
@SP
A=M
M=-1
(END.2)
// increment stack pointer
@SP
M=M+1

// push constant 892
// get address 892
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
// get address 891
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.3
D;JLT
@SP
A=M
M=0
@END.3
0;JMP
(TRUE.3)
@SP
A=M
M=-1
(END.3)
// increment stack pointer
@SP
M=M+1

// push constant 891
// get address 891
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
// get address 892
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.4
D;JLT
@SP
A=M
M=0
@END.4
0;JMP
(TRUE.4)
@SP
A=M
M=-1
(END.4)
// increment stack pointer
@SP
M=M+1

// push constant 891
// get address 891
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
// get address 891
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.5
D;JLT
@SP
A=M
M=0
@END.5
0;JMP
(TRUE.5)
@SP
A=M
M=-1
(END.5)
// increment stack pointer
@SP
M=M+1

// push constant 32767
// get address 32767
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
// get address 32766
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.6
D;JGT
@SP
A=M
M=0
@END.6
0;JMP
(TRUE.6)
@SP
A=M
M=-1
(END.6)
// increment stack pointer
@SP
M=M+1

// push constant 32766
// get address 32766
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
// get address 32767
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.7
D;JGT
@SP
A=M
M=0
@END.7
0;JMP
(TRUE.7)
@SP
A=M
M=-1
(END.7)
// increment stack pointer
@SP
M=M+1

// push constant 32766
// get address 32766
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
// get address 32766
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
D=M-D
@TRUE.8
D;JGT
@SP
A=M
M=0
@END.8
0;JMP
(TRUE.8)
@SP
A=M
M=-1
(END.8)
// increment stack pointer
@SP
M=M+1

// push constant 57
// get address 57
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
// get address 31
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
// get address 53
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

// push constant 112
// get address 112
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

// neg
// get value from stack
@SP
AM=M-1
M=-M
// increment stack pointer
@SP
M=M+1

// and
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D&M
// increment stack pointer
@SP
M=M+1

// push constant 82
// get address 82
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
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D|M
// increment stack pointer
@SP
M=M+1

// not
// get value from stack
@SP
AM=M-1
M=!M
// increment stack pointer
@SP
M=M+1
