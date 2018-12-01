package vmTranslator;

public class Parser {
	Boolean hVMoreCommands;
	String strVM;
	String strAsm;
	CmdType cmdType;
	static int count=0;
	static int calls=0;
	
	public Parser(String cmd, Boolean blDirectParse) throws Exception {
		if (cmd==null || cmd.startsWith("//") || cmd.startsWith("\n")) cmdType=CmdType.C_IGNORE;
		else
		{
			if (cmd.contains("//")) strVM=cmd.split("//")[0].trim();
			else strVM=cmd.trim();
			if (strVM.startsWith("push")) cmdType=CmdType.C_PUSH;
			else if (strVM.startsWith("pop")) cmdType=CmdType.C_POP;
			else if (strVM.startsWith("add") || strVM.startsWith("sub") || strVM.startsWith("neg") || strVM.startsWith("eq") || strVM.startsWith("gt") || strVM.startsWith("lt") || strVM.startsWith("and") || strVM.startsWith("or") || strVM.startsWith("not")) cmdType=CmdType.C_ARITHMETIC;
			else if (strVM.startsWith("label")) cmdType=CmdType.C_LABEL;
			else if (strVM.startsWith("if-goto")) cmdType=CmdType.C_IF;
			else if (strVM.startsWith("goto")) cmdType=CmdType.C_GOTO;
			else if (strVM.startsWith("function")) cmdType=CmdType.C_FUNCTION;
			else if (strVM.startsWith("call")) cmdType=CmdType.C_CALL;
			else if (strVM.startsWith("return")) cmdType=CmdType.C_RETURN;
			else cmdType=CmdType.C_IGNORE;
			if (blDirectParse) strAsm="// "+strVM+"\n";
			else strAsm="";
		}
	}
	
	static String parseBootStrap() throws Exception
	{
		String	asmBootStrap=new String();
		Parser parserSysInit=new Parser("call Sys.init 0", true);
		asmBootStrap=					
				"@256\n"+
				"D=A\n"+
				"@SP\n"+
				"M=D\n"+
				parserSysInit.parseCall();
		return asmBootStrap;
	}
	 private String nextCount()
	 {
		 count += 1;
		 return Integer.toString(count);
	 }
	  
	public String parseArithmetic() throws Exception
	{
		switch (strVM) {
		case "add":
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"M=D+M\n\n";
			break;
		case "sub":
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"M=M-D\n\n";
			break;
		case "neg":
			strAsm=strAsm+
			"@SP\n"+
			"A=M-1\n"+
			"M=-M\n\n";
			break;
		case "and":
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"M=D&M\n\n";
			break;
		case "or":
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"M=D|M\n\n";
			break;
		case "not":
			strAsm=strAsm+
			"@SP\n"+
			"A=M-1\n"+
			"M=!M\n\n";
			break;
		case "eq":
			String neq = nextCount();
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"D=M-D\n"+
			"@EQ.true."+neq+"\n"+
			"D;JEQ\n"+
			"@SP\n"+
			"A=M-1\n"+
			"M=0\n"+
			"@EQ.after."+neq+"\n"+
			"0;JMP\n"+
		    "(EQ.true." + neq + ")\n" +
		    "@SP\n" +
		    "A=M-1\n" +
		    "M=-1\n" +
		    "(EQ.after." + neq + ")\n\n";
			break;
		case "gt":
			String ngt = nextCount();
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"D=M-D\n"+
			"@GT.true."+ngt+"\n"+
			"D;JGT\n"+
			"@SP\n"+
			"A=M-1\n"+
			"M=0\n"+
			"@GT.after."+ngt+"\n"+
			"0;JMP\n"+
		    "(GT.true." + ngt + ")\n" +
		    "@SP\n" +
		    "A=M-1\n" +
		    "M=-1\n" +
		    "(GT.after." + ngt + ")\n\n";
			break;
		case "lt":
			String nlt = nextCount();
			strAsm=strAsm+
			"@SP\n"+
			"AM=M-1\n"+
			"D=M\n"+
			"A=A-1\n"+
			"D=M-D\n"+
			"@LT.true."+nlt+"\n"+
			"D;JLT\n"+
			"@SP\n"+
			"A=M-1\n"+
			"M=0\n"+
			"@LT.after."+nlt+"\n"+
			"0;JMP\n"+
		    "(LT.true." + nlt + ")\n" +
		    "@SP\n" +
		    "A=M-1\n" +
		    "M=-1\n" +
		    "(LT.after." + nlt + ")\n\n";
			break;
		default:
			throw new Exception(strVM+": bad arithmetic command!");
		}
		return strAsm;
	}
	
	public String parsePush() throws Exception
	{
		String[] strArrVM=strVM.split(" ");
		String asmPush=
		"@SP\n" +
		"A=M\n" +
		"M=D\n" +
		"@SP\n" +
		"M=M+1\n\n";
		switch (strArrVM[1]) {
		case "local":
			strAsm=strAsm+
			"@LCL\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"A=D+A\n"+
			"D=M\n"+
			asmPush;
			break;
		case "argument":
			strAsm=strAsm+
			"@ARG\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"A=D+A\n"+
			"D=M\n"+
			asmPush;
			break;
		case "this":
			strAsm=strAsm+
			"@THIS\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"A=D+A\n"+
			"D=M\n"+
			asmPush;
			break;
		case "that":
			strAsm=strAsm+
			"@THAT\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"A=D+A\n"+
			"D=M\n"+
			asmPush;
			break;
		case "temp":
			strAsm=strAsm+
			"@R5\n"+
			"D=A\n"+
			"@"+strArrVM[2]+"\n"+
			"A=D+A\n"+
			"D=M\n"+
			asmPush;
			break;
		case "static":
			strAsm=strAsm+
			"@"+Main.strCurrFileName+"."+strArrVM[2]+"\n"+
			"D=M\n"+
			asmPush;
			break;
		case "constant":
			strAsm=strAsm+
			"@"+strArrVM[2]+"\n"+
			"D=A\n"+
			asmPush;
			break;
		case "pointer":
			if (strArrVM[2].equals("0"))
				strAsm=strAsm+
				"@THIS\n"+
				"D=M\n"+
				asmPush;
			else
				strAsm=strAsm+
				"@THAT\n"+
				"D=M\n"+
				asmPush;
			break;
		default:
			throw new Exception(strVM+": bad push command!");
		}
		return strAsm;
	}
	
	public String parsePop() throws Exception
	{
		String[] strArrVM=strVM.split(" ");
		String asmPop=
		"@R13\n" +
		"M=D\n" +
		"@SP\n" +
		"AM=M-1\n" +
		"D=M\n" +
		"@R13\n" +
		"A=M\n" +
		"M=D\n\n";
		switch (strArrVM[1]) 
		{
		case "local":
			strAsm=strAsm+
			"@LCL\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"D=D+A\n"+
			asmPop;
			break;
		case "argument":
			strAsm=strAsm+
			"@ARG\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"D=D+A\n"+
			asmPop;
			break;
		case "this":
			strAsm=strAsm+
			"@THIS\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"D=D+A\n"+
			asmPop;
			break;
		case "that":
			strAsm=strAsm+
			"@THAT\n"+
			"D=M\n"+
			"@"+strArrVM[2]+"\n"+
			"D=D+A\n"+
			asmPop;
			break;
		case "temp":
			strAsm=strAsm+
			"@R5\n"+
			"D=A\n"+
			"@"+strArrVM[2]+"\n"+
			"D=D+A\n"+
			asmPop;
			break;
		case "static":
			strAsm=strAsm+
			"@"+Main.strCurrFileName+"."+strArrVM[2]+"\n"+
			"D=A\n"+
			asmPop;
			break;
		case "pointer":
			if (strArrVM[2].equals("0"))
				strAsm=strAsm+
			    "@THIS\n" +
			    "D=A\n" +
			    asmPop;
			else
				strAsm=strAsm+
				"@THAT\n" +
				"D=A\n" +
				asmPop;
			break;
		default:
			throw new Exception(strVM+": bad pop command!");
		}
		return strAsm;
	}
	
	public String parseLabel()
	{
		String[] strArrVM=strVM.split(" ");
		if (Main.strCurrFuncName!=null && Main.strCurrFuncName!="") strAsm=strAsm+"("+Main.strCurrFuncName+"$"+strArrVM[1]+")\n";
		else strAsm=strAsm+"("+strArrVM[1]+")\n";
		if (strAsm.contains("($")) strAsm=strAsm.replace("$", "");
		return strAsm;	
	}
	
	public String parseGoto()
	{
		String[] strArrVM=strVM.split(" ");
		if (Main.strCurrFuncName==null || Main.strCurrFuncName=="" || Main.functionTable.get(strArrVM[1])!=null) strAsm=strAsm+"@"+strArrVM[1]+"\n0;JMP\n";
		else strAsm=strAsm+"@"+Main.strCurrFuncName+"$"+strArrVM[1]+"\n0;JMP\n";
		if (strAsm.contains("@$")) strAsm=strAsm.replace("$", "");
		return strAsm;
	}
	
	public String parseIf()
	{
		String[] strArrVM=strVM.split(" ");
		strAsm=strAsm+
		"@SP\n"+
		"AM=M-1\n" +
		"D=M\n"+
		"@"+Main.strCurrFuncName+"$"+strArrVM[1]+"\n"+
		"D;JNE\n";
		if (strAsm.contains("@$")) strAsm=strAsm.replace("$", "");
		return strAsm;
	}
	
	public String parseFunction() throws Exception
	{
		String[] strArrVM=strVM.split(" ");
		int k=Integer.valueOf(strArrVM[2]);
		strAsm=
		"("+strArrVM[1]+")\n";
		for (int i=0; i<k; i++) 
		{
			Parser parserZero=new Parser("push constant 0", false);
			strAsm.concat(parserZero.parsePush());
		}
		return strAsm;
	}
	
	public String parseCall() throws Exception
	{
		String[] strArrVM=strVM.split(" ");
		int n=Integer.valueOf(strArrVM[2]);
		Parser parserGoto=new Parser(strVM, false);
		Parser parserRET=new Parser("label RET."+String.valueOf(n), false);
		String asmPushInternal=
		"@SP\n" +
		"A=M\n" +
		"M=D\n" +
		"@SP\n" +
		"M=M+1\n";
		String asmRET=parserRET.parseLabel();
		String asmPushRET=
		"@"+asmRET.replace("(", "").replace(")", "")+"\n"+
		"D=A\n"+
		asmPushInternal;
		String asmPushLCL=
		"@LCL\n"+
		"D=M\n"+
		asmPushInternal;
		String asmPushARG=
		"@ARG\n"+
		"D=M\n"+
		asmPushInternal;
		String asmPushTHIS=
		"@THIS\n"+
		"D=M\n"+
		asmPushInternal;
		String asmPushTHAT=
		"@THAT\n"+
		"D=M\n"+
		asmPushInternal;
		strAsm=strAsm+
		asmPushRET+
		asmPushLCL+
		asmPushARG+
		asmPushTHIS+
		asmPushTHAT+
		"\t//ARG=SP-n-5\n"+
		"D=M\n"+
		"@"+String.valueOf(n+5)+"\n"+
		"D=D-A\n"+
		"@ARG\n"+
		"M=D\n"+
		"\t//LCL=SP\n"+
		"@SP\n"+
		"D=M\n"+
		"@LCL\n"+
		"M=D\n"+
		parserGoto.parseGoto()+
		asmRET;	
		return strAsm;
	}
	
	public String parseReturn()
	{
		strAsm=strAsm+
		"\t//FRAME=LCL\n"+
		"@LCL\n"+
		"D=M\n"+
		"@FRAME\n"+
		"M=D\n"+
		"\t//RET=*(FRAME-5)\n"+
		"@5\n"+
		"D=D-A\n"+
		"A=D\n"+
		"D=M\n"+
		"@RET\n"+
		"M=D\n"+
		"\t//*ARG=pop()\n"+
		"@SP\n"+
		"M=M-1\n"+
		"A=M\n"+
		"D=M\n"+
		"@ARG\n"+
		"A=M\n"+
		"M=D\n"+
		"\t//SP=ARG+1\n"+
		"@ARG\n"+
		"D=M+1\n"+
		"@SP\n"+
		"M=D\n"+
		"\t//THAT=*(FRAME-1); FRAME--\n"+
		"@FRAME\n"+
		"D=M\n"+
		"@1\n"+
		"D=D-A\n"+
		"A=D\n"+
		"D=M\n"+
		"@THAT\n"+
		"M=D\n"+
		"\t//THIS=*(FRAME-2); LCL--\n"+
		"@FRAME\n"+
		"D=M\n"+
		"@2\n"+
		"D=D-A\n"+
		"A=D\n"+
		"D=M\n"+
		"@THIS\n"+
		"M=D\n"+
		"\t//ARG=*(FRAME-3); LCL--\n"+
		"@FRAME\n"+
		"D=M\n"+
		"@3\n"+
		"D=D-A\n"+
		"A=D\n"+
		"D=M\n"+
		"@ARG\n"+
		"M=D\n"+
		"\t//LCL=*(FRAME-4)\n"+
		"@FRAME\n"+
		"D=M\n"+
		"@4\n"+
		"D=D-A\n"+
		"A=D\n"+
		"D=M\n"+
		"@LCL\n"+
		"M=D\n"+
		"\t//goto RET\n"+
		"@RET\n"+
		"A=M\n"+
		"0;JMP\n";
		return strAsm;
	}
	
}
