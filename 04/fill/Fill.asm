// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP) // Macro loop for continuously awaiting keyboard input
	@SCREEN
	D=A
	@address
	M=D
	@KBD
	D=M
	@FILL
	D;JNE // IF KBD!=0 goto FILL
	@CLEAR
	D;JEQ // IF KBD==0 goto CLEAR

(FILL) // Loop for filling all pixels
	@24576 // 16384+32*256
	D=A
	@address
	D=M-D
	@LOOP
	D;JGE // If address>=24576 goto LOOP to keep on awaiting keyboard input
	@address
	A=M // Find the memory location of the pixel
	M=-1 // 1111111111111111 in binary
	@address
	M=M+1 // Next address
	@FILL
	0;JMP

(CLEAR) // Loop for clearing all pixels
	@24576
	D=A
	@address
	D=M-D
	@LOOP
	D;JGE // If address>=24576 goto LOOP to keep on awaiting keyboard input
	@address
	A=M // Find the memory location of the pixel
	M=0 // 1111111111111111 in binary
	@address
	M=M+1 // Next address
	@CLEAR
	0;JMP
