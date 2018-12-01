package assembler;

public class Parser {
	String strAsm;
	CmdType cmdType;
	
	public Parser(String cmd)
	{
		if (cmd==null || cmd.startsWith("//") || cmd.startsWith("\n")) cmdType=CmdType.IGNORE;
		else
		{
			if (cmd.contains("//")) strAsm=cmd.split("//")[0].trim();
			else strAsm=cmd;
			if (strAsm.contains("(")) cmdType=CmdType.LABEL;
			else if (strAsm.contains("@")) cmdType=CmdType.ADDRESS;
			else
			{
				if (strAsm.contains("=") && strAsm.contains(";")) cmdType=CmdType.DCJ;
				else if (strAsm.contains("=")) cmdType=CmdType.DC;
				else if (strAsm.contains(";")) cmdType=CmdType.CJ;
				else if (strAsm.contains("J")) cmdType=CmdType.J;
				else cmdType=CmdType.IGNORE;
			}
		}
	}
	
	public String label()
	{
		return (this.strAsm.replace("(", "")).replace(")", "").trim();
	}
	
	public String address()
	{
		return (this.strAsm.replace("@", "")).trim();
	}
	
	public String comp()
	{
		if (cmdType==CmdType.DC) return strAsm.split("=")[1].trim();
		else if (cmdType==CmdType.CJ) return strAsm.split(";")[0].trim();
		else if (cmdType==CmdType.DCJ) return (strAsm.split("=")[1]).split(";")[0].trim();
		else return null;
	}
	
	public String dest()
	{
		if (cmdType==CmdType.DC || cmdType==CmdType.DCJ) return strAsm.split("=")[0].trim();
		else return null;
	}
	
	public String jump()
	{
		if (cmdType==CmdType.J) return strAsm.trim();
		else if (cmdType==CmdType.CJ) return strAsm.split(";")[1].trim();
		else if (cmdType==CmdType.DCJ) return strAsm.split(";")[1].trim();
		else return null;
	}
}
