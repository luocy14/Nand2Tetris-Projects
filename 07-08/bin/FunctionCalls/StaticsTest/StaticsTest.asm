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
(Class1.set)
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

// pop static 0
@Class1.0
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

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

// pop static 1
@Class1.1
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 0
@0
D=A
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
(Class1.get)
// push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class1.1
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
(Class2.set)
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

// pop static 0
@Class2.0
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

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

// pop static 1
@Class2.1
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 0
@0
D=A
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
(Class2.get)
// push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class2.1
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
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class1.set 2
@Sys.init$RET.2

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
@7
D=D-A
@ARG
M=D
	//LCL=SP
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Sys.init$RET.2)
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

// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class2.set 2
@Sys.init$RET.2

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
@7
D=D-A
@ARG
M=D
	//LCL=SP
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Sys.init$RET.2)
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

// call Class1.get 0
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
@Class1.get
0;JMP
(Sys.init$RET.0)
// call Class2.get 0
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
@Class2.get
0;JMP
(Sys.init$RET.0)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE
0;JMP
