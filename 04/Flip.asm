// Program: Flip.asm
// flips the values of 
// RAM[0] and RAM[1]

    // temp = R1
    @R1
    D=M
    @temp
    M=D 

    // R1 = R0
    @R0
    D=M
    @R1
    M=D

    // R0 = temp
    @temp
    D=M
    @R0
    M=D

(END)
    @END
    0;JMP




