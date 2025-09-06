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

// Translated from Sys.vm

// function Sys.init 0
(Sys.init)

// push constant 4000
// get address 4000
@4000
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D

// push constant 5000
// get address 5000
@5000
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D

// call Sys.main 0
// push label return_Sys.main$ret.1
// get address return_Sys.main$ret.1
@return_Sys.main$ret.1
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
// goto Sys.main
@Sys.main
0;JMP
(return_Sys.main$ret.1)

// pop temp 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg 6
@6
M=D

// label LOOP
(LOOP)

// goto LOOP
@LOOP
0;JMP

// function Sys.main 5
(Sys.main)
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1
D=0
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// push constant 4001
// get address 4001
@4001
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D

// push constant 5001
// get address 5001
@5001
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D

// push constant 200
// get address 200
@200
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop local 1
// get address of local 1
// get value from LCL
@LCL
D=M
// calculate address
@1
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push constant 40
// get address 40
@40
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop local 2
// get address of local 2
// get value from LCL
@LCL
D=M
// calculate address
@2
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

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

// pop local 3
// get address of local 3
// get value from LCL
@LCL
D=M
// calculate address
@3
D=D+A
// store D in reg R13
@R13
M=D
// pop to R13
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in address saved in R13
@R13
A=M
M=D

// push constant 123
// get address 123
@123
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// call Sys.add12 1
// push label return_Sys.add12$ret.2
// get address return_Sys.add12$ret.2
@return_Sys.add12$ret.2
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
@1
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
// goto Sys.add12
@Sys.add12
0;JMP
(return_Sys.add12$ret.2)

// pop temp 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg 5
@5
M=D

// push local 0
// get value from LCL
@LCL
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

// push local 1
// get value from LCL
@LCL
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

// push local 2
// get value from LCL
@LCL
D=M
// calculate address
@2
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

// push local 3
// get value from LCL
@LCL
D=M
// calculate address
@3
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

// push local 4
// get value from LCL
@LCL
D=M
// calculate address
@4
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

// add
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D+M
// increment stack pointer
@SP
M=M+1

// add
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D+M
// increment stack pointer
@SP
M=M+1

// add
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D+M
// increment stack pointer
@SP
M=M+1

// add
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D+M
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

// function Sys.add12 0
(Sys.add12)

// push constant 4002
// get address 4002
@4002
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 0
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THIS
@THIS
M=D

// push constant 5002
// get address 5002
@5002
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// pop pointer 1
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// store D in reg THAT
@THAT
M=D

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

// push constant 12
// get address 12
@12
D=A
// push from D
@SP
A=M
M=D
// increment stack pointer
@SP
M=M+1

// add
// pop to D
// get value from stack
@SP
AM=M-1
D=M
// get value from stack
@SP
AM=M-1
M=D+M
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
