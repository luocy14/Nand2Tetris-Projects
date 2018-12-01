package vmTranslator;

import java.io.*;
import java.util.ArrayList;

public class Main {
	static ArrayList<String> arrStrVM;
	static ArrayList<String> arrStrAsm;
	static FunctionTable functionTable;
	static String strCurrFuncName;
	static String strCurrFileName;
	
	public static void readVM(String strVMPath) throws Exception
	{
		if (!strVMPath.contains("."))
		{
			File fileDir=new File(strVMPath);
			File[] fileVMs=fileDir.listFiles();
			for (File fileVM: fileVMs) readVM(fileVM.getAbsolutePath());
		}
		else if (strVMPath.endsWith(".vm"))
		{
			FileInputStream fisVM=new FileInputStream(strVMPath);
			BufferedReader brVM=new BufferedReader(new InputStreamReader(fisVM));
			String strVM=new String();
			while ((strVM=brVM.readLine())!=null) arrStrVM.add(strVM);
			brVM.close();
			fisVM.close();
		}
	}
	
	public static void vmToAsm() throws Exception
	{
		for (int i=0; i<arrStrVM.size();i++)
		{
			Parser parser = new Parser(arrStrVM.get(i), true);
			if (parser.cmdType==CmdType.C_FUNCTION)
			{
				String[] arrStrFunction=arrStrVM.get(i).trim().split(" ");
				functionTable.put(arrStrFunction[1], Integer.valueOf(arrStrFunction[2]));
			}
		}
		if (functionTable.get("Sys.init")!=null) arrStrAsm.add(Parser.parseBootStrap());
		for (int i=0; i<arrStrVM.size();i++)
		{
			if (arrStrVM.get(i).startsWith("//") && arrStrVM.get(i).endsWith(".vm")) 
			{
				String[] arrCurrFileName=arrStrVM.get(i).replace("//", "").replace(".vm", "").split("/");
				strCurrFileName=arrCurrFileName[arrCurrFileName.length-1];
			}
			Parser parser = new Parser(arrStrVM.get(i), true);
			if (parser.cmdType!=CmdType.C_IGNORE)
			{
				String strAsm=new String();
				switch (parser.cmdType) {
				case C_ARITHMETIC:
					strAsm=parser.parseArithmetic();
					break;
				case C_PUSH:
					strAsm=parser.parsePush();
					break;
				case C_POP:
					strAsm=parser.parsePop();
					break;
				case C_FUNCTION:
					strAsm=parser.parseFunction();
					strCurrFuncName=arrStrVM.get(i).trim().split(" ")[1];
					break;
				case C_LABEL:
					strAsm=parser.parseLabel();
					break;
				case C_GOTO:
					strAsm=parser.parseGoto();
					break;
				case C_IF:
					strAsm=parser.parseIf();
					break;
				case C_RETURN:
					strAsm=parser.parseReturn();
					break;
				case C_CALL:
					strAsm=parser.parseCall();
					break;
				default:
					break;
				}
				arrStrAsm.add(strAsm);
			}
		}
	}
	
	public static void writeAsm(String strVMPath) throws IOException
	{
		String strAsmPath=new String();
		String strDir=strVMPath.split("/")[strVMPath.split("/").length-1];
		if (!strVMPath.contains(".")) strAsmPath=strVMPath+"/"+strDir+".asm";
		else strAsmPath=strVMPath.replace(".vm", ".asm");
		File fileAsm=new File(strAsmPath);
		BufferedWriter bwAsm=new BufferedWriter(new FileWriter(fileAsm));
		for (int i=0; i<arrStrAsm.size(); i++) bwAsm.write(arrStrAsm.get(i));
		bwAsm.close();
	}
	
	public static void main(String[] args) throws Exception
	{
		arrStrAsm=new ArrayList<String>();
		arrStrVM=new ArrayList<String>();
		functionTable=new FunctionTable();
		strCurrFileName=new String();
		strCurrFuncName=new String();
		readVM(args[0]);
		vmToAsm();
		writeAsm(args[0]);
	}
}
