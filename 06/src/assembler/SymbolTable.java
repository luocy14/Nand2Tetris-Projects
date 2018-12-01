package assembler;
import java.util.*;

public class SymbolTable extends HashMap<String, Integer>{
	
	public SymbolTable()
	{
		this.put("SP", 0);
		this.put("LCL", 1);
		this.put("ARG", 2);
		this.put("THIS", 3);
		this.put("THAT", 4);
		this.put("R0", 0);
		this.put("R1", 1);
		this.put("R2", 2);
		this.put("R3", 3);
		this.put("R4", 4);
		this.put("R5", 5);
		this.put("R6", 6);
		this.put("R7", 7);
		this.put("R8", 8);
		this.put("R9", 9);
		this.put("R10", 10);
		this.put("R11", 11);
		this.put("R12", 12);
		this.put("R13", 13);
		this.put("R14", 14);
		this.put("R15", 15);
		this.put("SCREEN", 16384);
		this.put("KBD", 24576);
	}
	
	

}
