VAL 66
// Init
LDR R0 1
AND R1 R0 #15
AND R2 R0 #240
MOV R3 R1
::getDigit
CMP R3 #10
BLT decimal
SUB R3 R3 #9
ORR R3 R3 #64
B skip
::decimal
ORR R3 R3 #48
::skip
CMP R1 #255
BEQ leftDigit
MOV R7 R3
LSR R2 R2 #4
MOV R3 R2
MOV R1 #255
B getDigit
::leftDigit
MOV R6 R3
HALT
