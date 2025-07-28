// Program: Add2.asm
// Computes: RAM[2] = RAM[0]+RAM[1]

// D=RAM[0]
@0
D=M

// Extract D=D+RAM[1]
@1
D=D+M

// RAM[2]=D
@2
M=D

// END
@6
0;JMP



