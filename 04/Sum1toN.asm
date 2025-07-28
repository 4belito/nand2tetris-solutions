// Program: Sum1toN.asm
// Computes RAM[1] = 1+2+...+n 

    // Initiate variables
    @R0 
    D=M
    @n
    M=D // n=R0 
    
    @sum
    M=0 // sum = 0

// for i = 1 to n
    @i
    M=1 // i = 1

(LOOP)
    @i
    D=M
    @n
    D=D-M
    @STOP
    D;JGT // if i>n goto STOP

    // sum+=i
    @i
    D=M
    @sum
    D=D+M
    @sum
    M=D

    // i++
    @i
    M=M+1
    @LOOP
    0;JMP

(STOP)
    @sum
    D=M
    @R1
    M=D //RAM[1]=sum

(END)
    @END
    0;JMP






