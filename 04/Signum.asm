// Program: Signum.asm
// Computes: if R0>0
//              R1=1
//           else
//              R1=0

    // D=RAM[0]
    @R0
    D=M

    // if D>0 (POSITIVE)
    @POSITIVE
    D;JGT

    // else (NOPOSITIVE)
    @NOPOSITIVE
    0;JMP

(POSITIVE)
    @R1
    M=1
    @END
    0;JMP

(NOPOSITIVE)
    @R1
    M=0
    @END
    0;JMP

(END)
    @END
    0;JMP







