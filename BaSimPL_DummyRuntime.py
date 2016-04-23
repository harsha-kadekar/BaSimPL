
class DummyRunTime(object):
    def __init__(self, inputfile):
        self._reg_d0 = None
        self._reg_d1 = None
        self._reg_a0 = None
        self._stack = []
        self._labelMapper = {}
        self._variableMapper = {}
        self._IntermediateFile = inputfile
        self._IntermediateCode = []
        self._InstructionPointer = -1
        self._functionMap = {}
        self._debug = 0

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

    def executecode(self):
        self.readIntermediateFile()
        self.GenerateFunctionandLabelMap()
        self.SetInstructionPointerToMain()

        last_instruction_address = self._IntermediateCode.__len__()
        while self._InstructionPointer < last_instruction_address:
            instruction = self._IntermediateCode[self._InstructionPointer]
            splitInst = instruction.split(' ')
            opcode = splitInst[0]

            if opcode == 'ALOC':
                x = 0
            elif opcode == 'MOVI':
                x = 0
            elif opcode == 'PUSH':
                x = 0
            elif opcode == 'LEA':
                x = 1
            elif opcode == 'POP':
                x = 2
            elif opcode == 'MOV':
                x = 3
            elif opcode == 'CGT':
                x = 4
            elif opcode == 'BEQ':
                x = 5
            elif opcode == 'MUL':
                x = 6
            elif opcode == 'SUB':
                x = 7
            elif opcode == 'JMP':
                x = 8
            elif opcode == 'CALL':
                x = 9
            elif opcode == 'ret':
                x = 0
            elif opcode == 'ADD':
                x = 1
            elif opcode == 'DIV':
                x = 2
            elif opcode == 'OR':
                x = 2
            elif opcode == 'AND':
                x = 3
            elif opcode == 'CEQ':
                x = 4
            elif opcode == 'CNE':
                x = 1
            elif opcode == 'CLT':
                x = 2
            elif opcode == 'CGE':
                x = 3
            elif opcode == 'CLE':
                x = 4
            else:
                x = 5




        return

