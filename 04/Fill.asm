// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Get Number of words in the screen(8192=512*256/16)

//Get SCREEN last address(n)

@SCREEN
D=A
@8192
D=D+A
@screen_end
M=D

//initiate Screen color white
@color
M=0

(READKEY)
    // reset address
    @SCREEN
    D=A
    @address
    M=D

    // read keyboard
    @KBD
    D=M

    // if key pressed
    @KEY
    D;JNE

    // if no key and color==-1(black)
    @color
    D=M
    @CHANGE
    D;JNE

    @READKEY
    0;JMP


(KEY)
    @color
    D=M
    // if color == 0(white)
    @CHANGE
    D;JEQ

    // goto READKEY
    @READKEY
    0;JMP

(CHANGE)
    // Change ith world color
    @color
    D=M
    @address
    A=M
    M=!D

    //address++
    @address
    M=M+1
    
    // if (address<screen_end) change next world
    D=M
    @screen_end
    D=M-D
    @CHANGE
    D;JGT

    // update color variable
    @color
    M=!M

    // goto READKEY
    @READKEY
    0;JMP