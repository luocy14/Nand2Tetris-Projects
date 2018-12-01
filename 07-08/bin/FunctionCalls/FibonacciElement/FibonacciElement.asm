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
(Main.fibonacci)
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

// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT.true.1
D;JLT
@SP
A=M-1
M=0
@LT.after.1
0;JMP
(LT.true.1)
@SP
A=M-1
M=-1
(LT.after.1)

// if-goto IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
// goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
// label IF_TRUE
(Main.fibonacci$IF_TRUE)
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
// label IF_FALSE
(Main.fibonacci$IF_FALSE)
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

// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// call Main.fibonacci 1
@Main.fibonacci$RET.1

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
@Main.fibonacci
0;JMP
(Main.fibonacci$RET.1)
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

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// call Main.fibonacci 1
@Main.fibonacci$RET.1

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
@Main.fibonacci
0;JMP
(Main.fibonacci$RET.1)
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
(Sys.init)
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Main.fibonacci 1
@Sys.init$RET.1

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
@Main.fibonacci
0;JMP
(Sys.init$RET.1)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE
0;JMP
