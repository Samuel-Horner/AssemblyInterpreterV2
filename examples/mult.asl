// Multiplication program
VAL #10
VAL #7
// Init
LDR R0 2
LDR R1 3
::main
CMP R1 #0
BEQ end
ADD R2 R2 R0
SUB R1 R1 #1
B main
::end
HALT
