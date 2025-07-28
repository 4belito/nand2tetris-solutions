// Program getkey.asm
// Save Prssed key in RO
// esc key ends the program

// save esc value
@140
D=A
@esc
M=D

(LOOP)
    @KBD
    D=M
    @R0
    M=D

    @esc
    D=D-M
    @END
    D;JEQ

    @LOOP
    0;JMP

(END)
    0;JMP
    