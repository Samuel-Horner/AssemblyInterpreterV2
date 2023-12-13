import sys

class Component:
    def __init__(self, string: str):
        if string[0] in ['#', 'R']:
            self.adm = string[0]
            try: self.val = int(string[1:])
            except: self.val = string[1:]
        else:
            self.adm = False
            try: self.val = int(string)
            except: self.val = string
    def __str__(self) -> str:
        return self.adm + str(self.val) if self.adm else str(self.val)

class Instruction:
    def __init__(self, string: str):
        if len(string) < 2:
            self.inst = ['']
        elif string[:2] == '//' or string[:2] == '::':
            self.inst = [string]
        else:
            instArr = string.strip().split(' ')
            self.inst = [instArr[0]]
            for i in instArr[1:]:
                self.inst.append(Component(i))
    
    def __getitem__(self, part: int) -> list:
        if part >= len(self.inst):
            raise Exception('Part index out of bounds')
            return

        return self.inst[part]

    def __str__(self) -> str:
        output = self.inst[0] + ' '
        for i in self.inst[1:]:
            output += str(i) + ' '
        return output.strip()

    def __len__(self) -> int:
        return len(self.inst)

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

class Processor:
    def __init__(self, registers: int):
        self.reg = [0 for i in range(0,registers)]
        self.acc = 0
        self.pc = 0
        self.mem = [None] # Emtpy element in index 0 to match arr index with line numbers
        self.displayMsg = ''

    def run(self, fileName: str) -> None:
        self.read(fileName)
        while self.pc != len(self.mem) - 1:
            self.pc += 1
            try: self.exec()
            except:
                print(f'Error at line {self.pc}: {self.mem[self.pc]}')
                exit()
            self.display()
            input('[]: ')
        print('End of memory / HALT reached')

    def read(self, fileName: str) -> None:
        try:
            f = open(fileName, 'r')
        except:
            print('Failed to open file')
            exit()
        
        memArr = f.read().split('\n')
        for i in memArr:
            self.mem.append(Instruction(i))
    
        f.close()

    def exec(self) -> None:
        cir = self.mem[self.pc]
        self.displayMsg = str(cir)
        if str(cir) == 'HALT':
            self.pc = len(self.mem) - 1
            return
        if len(cir) <= 1: return
        self.displayMsg += ' -> '
        match cir[0]:
            case 'VAL':
                self.displayMsg += f'Value {cir[1]}'
            case 'LDR':
                self.reg[cir[1].val] = self.mem[cir[2].val][1].val
                self.displayMsg += f'Loaded value {self.mem[cir[2].val][1].val} into {cir[1]}'
            case 'STR':
                self.mem[cir[2].val] = Instruction(f'VAL {self.reg[cir[1].val]}')
                self.displayMsg = f'Stored value {self.reg[cir[1].val]} ({cir[1]})'
            case 'ADD':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] + val
                self.displayMsg += f'Stored {cir[2]} + {cir[3]} in {cir[1]}'
            case 'SUB':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] - val
                self.displayMsg += f'Stored {cir[2]} - {cir[3]} in {cir[1]}'
            case 'MOV':
                val = self.getVal(cir[2])
                self.reg[cir[1].val] = val
                self.displayMsg += f'Copied {cir[2]} into {cir[1]}'
            case 'CMP': # 1: EQ, 2: LT, 3: GT
                num1 = self.reg[cir[1].val]
                num2 = self.getVal(cir[2])
                if num1 == num2: self.acc = 1
                elif num1 < num2: self.acc = 2
                else: self.acc = 3
                self.displayMsg += f'Compared {cir[1]} to {cir[2]}'
            case 'B':
                print(cir[1].val)
                self.pc = self.find(f'::{cir[1].val}') - 1
                print(self.pc)
                self.displayMsg += f'Branched'
            case 'BEQ':
                if self.acc == 1:
                    self.pc = self.find(f'::{cir[1].val}') - 1
                    self.displayMsg += f'Branched'
                else: self.displayMsg += 'Did not branch'
            case 'BNE':
                if self.acc != 1:
                    self.pc = self.find(f'::{cir[1].val}') - 1
                    self.displayMsg += f'Branched'
                else: self.displayMsg += 'Did not branch'
            case 'BLT':
                if self.acc == 2:
                    self.pc = self.find(f'::{cir[1].val}') - 1
                    self.displayMsg += f'Branched'
                else: self.displayMsg += 'Did not branch'
            case 'BGT':
                if self.acc == 3:
                    self.pc = self.find(f'::{cir[1].val}') - 1
                    self.displayMsg += f'Branched'
                else: self.displayMsg += 'Did not branch'
            case 'AND':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] & val
                self.displayMsg += f'Stored a bitwise AND on {cir[2]}, {cir[3]} in {cir[1]}'
            case 'ORR':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] | val
                self.displayMsg += f'Stored a bitwise OR on {cir[2]}, {cir[3]} in {cir[1]}'
            case 'EOR':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] ^ val
                self.displayMsg += f'Stored a bitwise XOR on {cir[2]}, {cir[3]} in {cir[1]}'
            case 'MVN':
                val = self.getVal(cir[2])
                self.reg[cir[1].val] = ~val
                self.displayMsg += f'Stored a bitwise NOT on {cir[2]} in {cir[1]}'
            case 'LSL':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] << val
                self.displayMsg += f'Stored a logiccal shift left on {cir[2]} by {cir[3]} in {cir[1]}'
            case 'LSR':
                val = self.getVal(cir[3])
                self.reg[cir[1].val] = self.reg[cir[2].val] >> val
                self.displayMsg += f'Stored a logiccal shift right on {cir[2]} by {cir[3]} in {cir[1]}'
            case _:
                print('Unkown command')
                raise Exception()

    def find(self, inst: str) -> int:
        return self.mem.index(Instruction(inst))

    def getVal(self, cmpo: Component) -> int:
        if cmpo.adm == '#': val = cmpo.val
        elif cmpo.adm == 'R': val = self.reg[cmpo.val]
        else: raise Exception('Unidentified address mode')
        return val

    def display(self) -> None:
        print('\x1b[H\x1b[0J' + Processor.fmt([['Reg', 'Val']] + [[index, elem] for index, elem in enumerate(self.reg)] + [['ACC', self.acc], ['PC', self.pc]], 0) + self.displayMsg)

    def fmt(rows: list, titleDepth: int) -> str:        
        maxLength = [0 for i in rows[0]]
        for row in rows:
            for index, elem in enumerate(row):
                maxLength[index] = max(maxLength[index], len(str(elem)) + 2)

        output = ''
        for index, elem in enumerate(rows[:titleDepth+1]):
            output += '| '
            for i, e in enumerate(elem):
                output += f'{str(e).center(maxLength[i])} | '
            output += '\n'
        output += '-' * (sum(maxLength) + 3 * len(maxLength) + 1) + '\n'
        for index, elem in enumerate(rows[titleDepth+1:]):
            output += '| '
            for i, e in enumerate(elem):
                output += f'{str(e).center(maxLength[i])} | '
            output += '\n'
        
        return output
        


if __name__ == '__main__':
    cpu = Processor(8)
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
    else:
        fileName = input('Enter file name:\n')
    cpu.run(fileName)
