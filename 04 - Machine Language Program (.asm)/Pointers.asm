// Program: Pointers.arm
// arr is in RAM[address], address=100
// arr length n=10
// for (i=0;i<n;;i++){
//      arr[i]=-1
//  }

    // initialize address
    @100
    D=A
    @address
    M=D

    // initialize n
    @10
    D=A
    @n
    M=D

    // initialize i = 0
    @i
    M=0

(LOOP)
    // if (i==n) goto END
    @i
    D=M
    @n
    D=D-M
    @END
    D;JEQ

    // RAM[address+i]=-1
    @address
    D=M
    @i
    A=D+M //Get the address(M=RAM[A])
    M=-1


    //i++
    @i
    M=M+1
    @LOOP
    0;JMP

(END)
    @END
    0;JMP
