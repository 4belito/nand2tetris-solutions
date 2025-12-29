// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    // Initiate variables
    @mult
    M=0 // mult = 0

// for i = 1 to R1
    @i
    M=1 // i = 1 

(LOOP)
    @i
    D=M
    @R1
    D=D-M
    @STOP
    D;JGT // if i>R1 goto STOP

    // mult+=R0
    @R0
    D=M
    @mult
    M=D+M

    // i++
    @i
    M=M+1
    @LOOP
    0;JMP

(STOP)
    @mult
    D=M
    @R2
    M=D //RAM[1]=sum

(END)
    @END
    0;JMP






