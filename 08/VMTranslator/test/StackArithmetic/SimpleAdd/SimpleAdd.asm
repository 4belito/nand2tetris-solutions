// Assembly code SimpleAdd.asm

// Translated from SimpleAdd.vm

// push constant 7
// get address 7
@7
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 8
// get address 8
@8
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
