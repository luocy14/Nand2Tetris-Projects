package assembler;
import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Main {
	static ArrayList<String> arrStrAsm;
	static ArrayList<String> arrStrBin;
	static SymbolTable symbolTable;
	static int intRom,intRam;
	
    public static boolean judgeContainsLtr(String address) {
    	String regex=".*[a-zA-Z]+.*";
	    Matcher m=Pattern.compile(regex).matcher(address);
	    return m.matches();
    }

	public static void readAsm(String strAsmPath) throws IOException
	{
		FileInputStream fisAsm=new FileInputStream(strAsmPath);
		BufferedReader brAsm=new BufferedReader(new InputStreamReader(fisAsm));
		String strAsm=new String();
		while ((strAsm=brAsm.readLine())!=null) arrStrAsm.add(strAsm);
		brAsm.close();
		fisAsm.close();
	}
	
	public static void asmToBin()
	{
		symbolTable=new SymbolTable();
		intRom=0;
		for (int i=0; i<arrStrAsm.size();i++)
		{
			Parser parser = new Parser(arrStrAsm.get(i));
			if (parser.cmdType!=CmdType.LABEL && parser.cmdType!=CmdType.IGNORE) intRom++;
			if (parser.cmdType==CmdType.LABEL) symbolTable.put(parser.label(), intRom);
		}
		intRam=16;
		for (int i=0; i<arrStrAsm.size();i++)
		{
			Parser parser = new Parser(arrStrAsm.get(i));
			if (parser.cmdType!=CmdType.LABEL && parser.cmdType!=CmdType.IGNORE)
			{
				String strBin=new String();
				switch (parser.cmdType) {
				case ADDRESS:
					if (judgeContainsLtr(parser.address()))
					{
						if (symbolTable.get(parser.address())!=null) strBin="0"+Code.address(String.valueOf(symbolTable.get(parser.address())));
						else
						{
							symbolTable.put(parser.address(), intRam);
							intRam++;
							strBin="0"+Code.address(String.valueOf(symbolTable.get(parser.address())));
						}
					}
					else strBin="0"+Code.address(parser.address());
					break;
				case DCJ:
					strBin="111"+Code.comp(parser.comp())+Code.dest(parser.dest())+Code.jump(parser.jump());
					break;
				case DC:
					strBin="111"+Code.comp(parser.comp())+Code.dest(parser.dest())+"000";
					break;
				case CJ:
					strBin="111"+Code.comp(parser.comp())+"000"+Code.jump(parser.jump());
					break;
				case J:
					strBin="1110000000000"+Code.jump(parser.jump());
					break;
				default:
					break;
				}
				arrStrBin.add(strBin);
			}
		}
	}
	
	public static void writeBin(String strAsmPath) throws IOException
	{
		File fileBin=new File(strAsmPath.replace(".asm", ".hack"));
		BufferedWriter bwBin=new BufferedWriter(new FileWriter(fileBin));
		for (int i=0; i<arrStrBin.size(); i++) bwBin.write(arrStrBin.get(i)+"\n");
		bwBin.close();
	}
	
	public static void main(String[] args) throws IOException
	{
		arrStrAsm=new ArrayList<String>();
		arrStrBin=new ArrayList<String>();
		readAsm(args[0]);
		asmToBin();
		writeBin(args[0]);
	}
}
