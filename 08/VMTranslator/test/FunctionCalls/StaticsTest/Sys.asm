// Assembly code Sys.asm

// Initialization code
// get address 256
@256
D=A  // Set SP to 256
// store D in reg SP
@SP
M=D  // SP = 256

// call Sys.init 0
// push label return_Sys.init$ret.0
// get address return_Sys.init$ret.0
@return_Sys.init$ret.0
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@0
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Sys.init
@Sys.init
0;JMP
(return_Sys.init$ret.0)

// Translated from Class1.vm

// function Class1.set 0
(Class1.set)

// push argument 0
// get value from ARG
@ARG
D=M
// calculate address
@0
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop static 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg Class1.0
@Class1.0
M=D

// push argument 1
// get value from ARG
@ARG
D=M
// calculate address
@1
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop static 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg Class1.1
@Class1.1
M=D

// push constant 0
// get address 0
@0
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// return
// get value from LCL
@LCL
D=M
// store D in reg R14
@R14
M=D
// save return address
@5
A=D-A
D=M
// store D in reg R15
@R15
M=D            // R15 = RET
// pop argument 0
// pop to ARG
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in ARG
@ARG
A=M
M=D
// reposition SP
@ARG
D=M+1
// store D in reg SP
@SP
M=D            // SP = ARG + 1
@R14
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D
@R14
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D
@R14
AM=M-1
D=M
// store D in reg ARG
@ARG
M=D
@R14
AM=M-1
D=M
// store D in reg LCL
@LCL
M=D
@R15
A=M
0;JMP

// function Class1.get 0
(Class1.get)

// push static 0
// get value from Class1.0
@Class1.0
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push static 1
// get value from Class1.1
@Class1.1
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// sub
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=M-D
// increment stack pointer
@SP
M=M+1

// return
// get value from LCL
@LCL
D=M
// store D in reg R14
@R14
M=D
// save return address
@5
A=D-A
D=M
// store D in reg R15
@R15
M=D            // R15 = RET
// pop argument 0
// pop to ARG
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in ARG
@ARG
A=M
M=D
// reposition SP
@ARG
D=M+1
// store D in reg SP
@SP
M=D            // SP = ARG + 1
@R14
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D
@R14
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D
@R14
AM=M-1
D=M
// store D in reg ARG
@ARG
M=D
@R14
AM=M-1
D=M
// store D in reg LCL
@LCL
M=D
@R15
A=M
0;JMP

// Translated from Sys.vm

// function Sys.init 0
(Sys.init)

// push constant 6
// get address 6
@6
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

// call Class1.set 2
// push label return_Class1.set$ret.1
// get address return_Class1.set$ret.1
@return_Class1.set$ret.1
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@2
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Class1.set
@Class1.set
0;JMP
(return_Class1.set$ret.1)

// pop temp 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg 5
@5
M=D

// push constant 23
// get address 23
@23
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 15
// get address 15
@15
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// call Class2.set 2
// push label return_Class2.set$ret.2
// get address return_Class2.set$ret.2
@return_Class2.set$ret.2
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@2
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Class2.set
@Class2.set
0;JMP
(return_Class2.set$ret.2)

// pop temp 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg 5
@5
M=D

// call Class1.get 0
// push label return_Class1.get$ret.3
// get address return_Class1.get$ret.3
@return_Class1.get$ret.3
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@0
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Class1.get
@Class1.get
0;JMP
(return_Class1.get$ret.3)

// call Class2.get 0
// push label return_Class2.get$ret.4
// get address return_Class2.get$ret.4
@return_Class2.get$ret.4
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register LCL
// get value from LCL
@LCL
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register ARG
// get value from ARG
@ARG
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THIS
// get value from THIS
@THIS
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// push register THAT
// get value from THAT
@THAT
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1 
// update ARG after call
// get value from SP
@SP
D=M
@5
D=D-A
@0
D=D-A
// store D in reg ARG
@ARG
M=D
// update LCL
// get value from SP
@SP
D=M
// store D in reg LCL
@LCL
M=D
// goto Class2.get
@Class2.get
0;JMP
(return_Class2.get$ret.4)

// label END
(END)

// goto END
@END
0;JMP

// Translated from Class2.vm

// function Class2.set 0
(Class2.set)

// push argument 0
// get value from ARG
@ARG
D=M
// calculate address
@0
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop static 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg Class2.0
@Class2.0
M=D

// push argument 1
// get value from ARG
@ARG
D=M
// calculate address
@1
D=D+A
A=D
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop static 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg Class2.1
@Class2.1
M=D

// push constant 0
// get address 0
@0
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// return
// get value from LCL
@LCL
D=M
// store D in reg R14
@R14
M=D
// save return address
@5
A=D-A
D=M
// store D in reg R15
@R15
M=D            // R15 = RET
// pop argument 0
// pop to ARG
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in ARG
@ARG
A=M
M=D
// reposition SP
@ARG
D=M+1
// store D in reg SP
@SP
M=D            // SP = ARG + 1
@R14
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D
@R14
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D
@R14
AM=M-1
D=M
// store D in reg ARG
@ARG
M=D
@R14
AM=M-1
D=M
// store D in reg LCL
@LCL
M=D
@R15
A=M
0;JMP

// function Class2.get 0
(Class2.get)

// push static 0
// get value from Class2.0
@Class2.0
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push static 1
// get value from Class2.1
@Class2.1
D=M
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// sub
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=M-D
// increment stack pointer
@SP
M=M+1

// return
// get value from LCL
@LCL
D=M
// store D in reg R14
@R14
M=D
// save return address
@5
A=D-A
D=M
// store D in reg R15
@R15
M=D            // R15 = RET
// pop argument 0
// pop to ARG
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in ARG
@ARG
A=M
M=D
// reposition SP
@ARG
D=M+1
// store D in reg SP
@SP
M=D            // SP = ARG + 1
@R14
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D
@R14
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D
@R14
AM=M-1
D=M
// store D in reg ARG
@ARG
M=D
@R14
AM=M-1
D=M
// store D in reg LCL
@LCL
M=D
@R15
A=M
0;JMP
