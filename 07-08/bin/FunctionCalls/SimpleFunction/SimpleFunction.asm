(SimpleFunction.test)
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

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// not
@SP
A=M-1
M=!M

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

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// push argument 1
@ARG
D=M
@1
A=D+A
D=M
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
