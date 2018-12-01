@256
D=A
@SP
M=D
// call Sys.init 0
@RET.0

D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
	//ARG=SP-n-5
D=M
@5
D=D-A
@ARG
M=D
	//LCL=SP
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RET.0)
(Sys.init)
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@THIS
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@THAT
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// call Sys.main 0
@Sys.init$RET.0

D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
	//ARG=SP-n-5
D=M
@5
D=D-A
@ARG
M=D
	//LCL=SP
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.init$RET.0)
// pop temp 1
@R5
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// label LOOP
(Sys.init$LOOP)
// goto LOOP
@Sys.init$LOOP
0;JMP
(Sys.main)
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@THIS
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@THAT
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 2
@LCL
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 3
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Sys.add12 1
@Sys.main$RET.1

D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
	//ARG=SP-n-5
D=M
@6
D=D-A
@ARG
M=D
	//LCL=SP
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.main$RET.1)
// pop temp 0
@R5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 1
@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 4
@LCL
D=M
@4
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// return
	//FRAME=LCL
@LCL
D=M
@FRAME
M=D
	//RET=*(FRAME-5)
@5
D=D-A
A=D
D=M
@RET
M=D
	//*ARG=pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
	//SP=ARG+1
@ARG
D=M+1
@SP
M=D
	//THAT=*(FRAME-1); FRAME--
@FRAME
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
	//THIS=*(FRAME-2); LCL--
@FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
	//ARG=*(FRAME-3); LCL--
@FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
	//LCL=*(FRAME-4)
@FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
	//goto RET
@RET
A=M
0;JMP
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@THIS
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@THAT
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 12
@12
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// return
	//FRAME=LCL
@LCL
D=M
@FRAME
M=D
	//RET=*(FRAME-5)
@5
D=D-A
A=D
D=M
@RET
M=D
	//*ARG=pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
	//SP=ARG+1
@ARG
D=M+1
@SP
M=D
	//THAT=*(FRAME-1); FRAME--
@FRAME
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
	//THIS=*(FRAME-2); LCL--
@FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
	//ARG=*(FRAME-3); LCL--
@FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
	//LCL=*(FRAME-4)
@FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
	//goto RET
@RET
A=M
0;JMP
