// Program: Rectangle.asm
// Draws a filled rectangle at screen's top left corner.
// The rectangles's width is 16 pixeles, and its height is RAM[0].
// Usage: put a non-negative number (rectangle's height) in RAM[0].

    //n = RAM[0]
    @R0
    D=M
    @n
    M=D

    // i = 0
    @i
    M=0

    // address-> SCREEN Address
    @SCREEN
    D=A
    @address
    M=D

(LOOP)
    // i (i=n) goto END
    @i
    D=M
    @n
    D=D-M
    @END
    D;JEQ

    //RAM[address]=-1 (16 pixeles black)
    @address
    A=M // get address
    M=-1 // RAM[address]=-1

    // address+=32
    @32
    D=A
    @address
    M=D+M

    // i++
    @i
    M=M+1
    @LOOP
    0;JMP

    

(END)
    @END
    0;JMP








