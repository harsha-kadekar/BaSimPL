
class DummyRunTime(object):
    def __init__(self, inputfile):
        self._reg_d0 = 0
        self._reg_d1 = 0
        self._reg_a0 = ''
        self._stack = []
        self._labelMapper = {}
        self._frames = []
        self._localStacks = []
        self._globalVariable = {}
        self._globalStacks = {}
        self._IntermediateFile = inputfile
        self._IntermediateCode = []
        self._InstructionPointer = -1
        self._functionMap = {}
        self._debug = 0
        self._returnAddress = []
        self._framePointer = []

    @property
    def IntermediateFile(self):
        return self._IntermediateFile

    @IntermediateFile.setter
    def IntermediateFile(self, value):
        self._IntermediateFile = value

    @property
    def DebugFlag(self):
        return self._debug

    @DebugFlag.setter
    def DebugFlag(self, value):
        self._debug = value

    def readIntermediateFile(self):
        inFile = open(self._IntermediateFile, 'r')
        self._IntermediateCode = inFile.readlines()
        for i in range(0, self._IntermediateCode.__len__()):
            str = self._IntermediateCode[i]
            str = str[:str.__len__() - 1]
            self._IntermediateCode[i] = str

    def SetInstructionPointerToMain(self):
        if self._functionMap.has_key('main'):
            self._InstructionPointer = self._functionMap['main'] + 1

    def GenerateFunctionandLabelMap(self):
        lineNo = 0
        for line in self._IntermediateCode:
            if line.startswith('FUNCT_BEGIN_') and line.endswith(':'):
                function_name = line[12:]
                function_name = function_name[:function_name.__len__() - 1]
                self._functionMap.__setitem__(function_name, lineNo)
            elif line.endswith(':'):
                label_name = line[:line.__len__() - 1]
                self._labelMapper.__setitem__(label_name, lineNo)
            lineNo += 1

    def PrintDebugInfo(self):
        if self._debug == 1:
            print '\n'
            print '+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=++DEBUG INFORMATION++=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+='
            print 'D0:\t' + self._reg_d0.__str__()
            print 'D1:\t' + self._reg_d1.__str__()
            print 'A0:\t' + self._reg_a0.__str__()
            print 'InstructionPointer:\t' + self._InstructionPointer.__str__()
            print 'Instruction To Be Executed:\t' + self._IntermediateCode[self._InstructionPointer]
            print 'STACK:\t' + self._stack.__str__()
            print 'STACKED RETURN ADDRESS:\t' + self._returnAddress.__str__()
            print '\nGLOBAL VARIABLES:'
            print self._globalVariable
            print '\nFUNCTIONS:'
            print self._functionMap
            print '\nLABELS:'
            print self._labelMapper
            print '\nFRAME POINTERS:'
            print self._framePointer
            print '\nFRAME ALLOCATIONS:'
            print self._frames
            print '\nGLOBAL STACK VARIABLES:'
            print self._globalStacks
            print '\nLOCAL STACK VARIABLES:'
            print self._localStacks
            print '+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+='
            print '\n'

    def ALU_LWSW_BRANCH(self, ip):
        instruction = self._IntermediateCode[ip]
        splitInst = instruction.split(' ')
        opcode = splitInst[0]

        if opcode == 'ALOC':
            if splitInst[1].__contains__('GLB'):
                self._globalVariable.__setitem__(ip, 0)
            else:
                localvariable = self._frames[0]
                fp = self._framePointer[0]
                localvariable.__setitem__(ip - fp, 0)

            ip += 1
        elif opcode == 'ALOCSTACK':
            if splitInst[1].__contains__('GLB'):
                newStack = []
                self._globalStacks.__setitem__(ip, newStack)
            else:
                localStacks = self._localStacks[0]
                fp = self._framePointer[0]
                newStack = []
                localStacks.__setitem__(ip - fp, newStack)

            ip += 1
        elif opcode == 'MOVI':
            operands = splitInst[1].split(',')
            self._reg_d0 = int(operands[1].strip())
            ip += 1
        elif opcode == 'PUSH':
            if splitInst[1].__contains__("D0"):
                self._stack.insert(0,self._reg_d0)
            else:
                self._stack.insert(0,self._reg_d0)
            ip += 1
        elif opcode == 'LEA':
            operands = splitInst[1].split(',')
            address = operands[1].strip()
            self._reg_a0 = address

            ip += 1
        elif opcode == 'POP':
            if splitInst[1].__contains__('D0'):
                self._reg_d0 = self._stack[0]
            else:
                self._reg_d1 = self._stack[0]
            self._stack.__delitem__(0)
            ip += 1
        elif opcode == 'MOV':
            operands = splitInst[1].split(',')
            value = None
            if operands[1].strip() == '(A0)':
                if self._reg_a0.__contains__('(PC)'):
                    address = int(self._reg_a0.replace('(PC)', ''))
                    value = self._globalVariable[address]
                else:
                    address = int(self._reg_a0.replace('(FP)', ''))
                    fp = self._framePointer[0]
                    localvariable = self._frames[0]
                    value = localvariable[address - fp]
            elif operands[1].strip() == 'D1':
                value = self._reg_d1
            else:
                value = self._reg_d0

            if operands[0].strip() == '(A0)':
                if self._reg_a0.__contains__('(PC)'):
                    address = int(self._reg_a0.replace('(PC)', ''))
                    self._globalVariable[address] = value
                else:
                    address = int(self._reg_a0.replace('(FP)', ''))
                    fp = self._framePointer[0]
                    localvariable = self._frames[0]
                    localvariable[address - fp] = value
            elif operands[0].strip() == 'D1':
                self._reg_d1 = value
            else:
                self._reg_d0 = value

            ip += 1

        elif opcode == 'CGT':
            if self._reg_d0 > self._reg_d1:
                self._reg_d0 = 1
            else:
                self._reg_d0 = 0

            ip += 1
        elif opcode == 'PUSHST':
            if self._reg_a0.__contains__('PC'):
                address = int(self._reg_a0.replace('(PC+ST)', ''))
                stack = self._globalStacks[address]
                stack.insert(0, self._reg_d0)
            else:
                address = int(self._reg_a0.replace('(FP+ST)', ''))
                fp = self._framePointer[0]
                localStacks = self._localStacks[address - fp]
                stack = localStacks[0]
                stack.insert(0, self._reg_d0)

            ip += 1
        elif opcode == 'POPST':
            if self._reg_a0.__contains__('PC'):
                address = int(self._reg_a0.replace('(PC+ST)', ''))
                stack = self._globalStacks[address]
                self._reg_d0 = stack[0]
                stack.__delitem__(0)
            else:
                address = int(self._reg_a0.replace('(FP+ST)', ''))
                fp = self._framePointer[0]
                localStacks = self._localStacks[address - fp]
                stack = localStacks[0]
                self._reg_d0 = stack[0]
                stack.__delitem__(0)
            ip += 1
        elif opcode == 'STEMPTY':
            if self._reg_a0.__contains__('PC'):
                address = int(self._reg_a0.replace('(PC+ST)', ''))
                stack = self._globalStacks[address]
                if stack.__len__() == 0:
                    self._reg_d0 = 1
                else:
                    self._reg_d0 = 0
            else:
                address = int(self._reg_a0.replace('(FP+ST)', ''))
                fp = self._framePointer[0]
                localStacks = self._localStacks[address - fp]
                stack = localStacks[0]
                if stack.__len__() == 0:
                    self._reg_d0 = 1
                else:
                    self._reg_d0 = 0
            ip += 1
        elif opcode == 'BEQ':
            if self._reg_d0 == 1:
                ip = self._labelMapper[splitInst[1].strip()] + 1
            else:
                ip += 1
        elif opcode == 'BNE':
            if self._reg_d0 == 0:
                ip = self._labelMapper[splitInst[1].strip()] + 1
            else:
                ip += 1
        elif opcode == 'MUL':
            self._reg_d0 = self._reg_d0 * self._reg_d1
            ip += 1
        elif opcode == 'SUB':
            self._reg_d0 = self._reg_d0 - self._reg_d1
            ip += 1
        elif opcode == 'JMP':
            ip = self._labelMapper[splitInst[1].strip()] + 1
        elif opcode == 'CALL':
            returnAddress = ip + 1
            self._returnAddress.insert(0, returnAddress)
            ip = self._functionMap[splitInst[1].strip()] + 1
            NewFrame = {}
            self._frames.insert(0, NewFrame)
            self._framePointer.insert(0, ip - 1)
            NewStacks = {}
            self._localStacks.insert(0, NewStacks)
        elif opcode == 'ret':
            ip = self._returnAddress[0]
            self._returnAddress.__delitem__(0)
            self._framePointer.__delitem__(0)
            self._frames.__delitem__(0)
            self._localStacks.__delitem__(0)
        elif opcode == 'ADD':
            self._reg_d0 = self._reg_d0 + self._reg_d1
            ip += 1
        elif opcode == 'DIV':
            self._reg_d0 = int(self._reg_d0/self._reg_d1)
            ip += 1
        elif opcode == 'OR':
            self._reg_d0 = self._reg_d0 or self._reg_d1
            ip += 1
        elif opcode == 'AND':
            self._reg_d0 = self._reg_d0 and self._reg_d1
            ip += 1
        elif opcode == 'CEQ':
            if self._reg_d0 == self._reg_d1:
                self._reg_d0 = 1
            else:
                self._reg_d0 = 0
            ip += 1
        elif opcode == 'CNE':
            if self._reg_d0 != self._reg_d1:
                self._reg_d0 = 1
            else:
                self._reg_d0 = 0
            ip += 1
        elif opcode == 'CLT':
            if self._reg_d0 < self._reg_d1:
                self._reg_d0 = 1
            else:
                self._reg_d0 = 0
            ip += 1
        elif opcode == 'CGE':
            if self._reg_d0 >= self._reg_d1:
                self._reg_d0 = 1
            else:
                self._reg_d0 = 0
            ip += 1
        elif opcode == 'CLE':
            if self._reg_d0 <= self._reg_d1:
                self._reg_d0 = 1
            else:
                self._reg_d0 = 0

            ip += 1
        elif opcode == 'OUT':
            print self._reg_d0
            ip += 1
        elif opcode == 'IN':
            self._reg_d0 = int(raw_input('ENTER INPUT FOR VARIABLE:'))
            ip += 1
        else:
            ip += 1 # encounted a label
        return ip

    def executecode(self):
        self.readIntermediateFile()
        self.GenerateFunctionandLabelMap()


        self._InstructionPointer = 0
        while self._InstructionPointer < self._IntermediateCode.__len__() and self._IntermediateCode[self._InstructionPointer].split(' ')[0].startswith('FUNCT_BEGIN_') == False:
            self.PrintDebugInfo()
            self._InstructionPointer = self.ALU_LWSW_BRANCH(self._InstructionPointer)

        self.PrintDebugInfo()

        self._reg_d1 = 0
        self._reg_a0 = ''
        self._reg_d0 = 0
        self._stack = []
        self._returnAddress = []
        self._framePointer = []
        self._frames = []
        self._localStacks = []

        self.SetInstructionPointerToMain()
        self._returnAddress.insert(0, -999)
        self._framePointer.insert(0, self._InstructionPointer - 1)
        mainFrame = {}
        main_stackVariables = {}
        self._frames.insert(0, mainFrame)
        self._localStacks.insert(0, main_stackVariables)
        last_instruction_address = self._IntermediateCode.__len__()
        while self._InstructionPointer < last_instruction_address and self._InstructionPointer != -999:
            self.PrintDebugInfo()
            self._InstructionPointer = self.ALU_LWSW_BRANCH(self._InstructionPointer)

        # self.PrintDebugInfo()

        return

