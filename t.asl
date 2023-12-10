//Division program
//Num1 / Num2
//Num1
VAL #128
//Num2
VAL #7
//Init
LDR R0 4
LDR R1 6
MOV R2 R0
MOV R3 #0
CMP R1 #0
BEQ end
::main
SUB R2 R2 R1
ADD R3 R3 #1
CMP R1 R2
BEQ main
BLT main
STR R3 24
STR R2 25
::end

VAL #0
VAL #0
HALT