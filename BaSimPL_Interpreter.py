# Name: BaSimPL_Interpreter
# Description: This file holds the classes and functions which help in interpreting the intermediate code of
#              'Basic Simple Programming Language' (BaSimPL).
# References: http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
#             https://ruslanspivak.com/lsbasi-part1/

######################################################################################################################
#                       Intermediate Machine - Target Machine instruction                                            #
######################################################################################################################
#
# Registers:
# D0 - General Purpose Register
# D1 - General Purpose Register
# A0 - Register that holds address
#
# Instructions
# MOVI - Used to load an intermediate value to a register. Example if we want to load integer constant 5 to register D0 then we use MOVI D0, 5 . After executing this instruction D0 will have value 5.
#
# PUSH - Used to put value into the stack. Suppose we want to put the value in register D0 to stack then we use PUSH D0.
#
# POP - Used to take a value out of the stack. POP D0, here whatever value was present at the top of the stack will be put in register D0.
#
# LEA - This will load the address to register A0. Suppose we are trying to assign some value to a variable, then that value will be stored in the address allocated to the variable. LEA will help to load the address location of that variable. LEA A0, n(PC)
#
# MOV - This instruction will help to move the value from one register location another another register. Example MOV D0, D1 - This will move the value in D1 to D0. Similarly if we want to move the value in a memory location that is variable to a register also we use MOV. Suppose we want to move the value of variable n to register D0 then, First we need to get the address of the variable n using LEA that is LEA A0, n(PC). Now we use MOV D0, (A0) to move the value to register D0.
#
# CGT - This instruction will be used to check for greater than condition between two registers. CGT D0, D1 - Here if D0 > D1 then value 1 will be stored in register D0, else 0 will be stored in the register D0.
#
# CNE - This instruction will be used to check for not equal to condition between two registers. CNE D0, D1 - Here if D0 is not equal to D1 then value 1 will be stored in register D0, else 0 will be stored in the register D0
#
# CEQ - This instruction will be used to check for equal to condition between two registers. CEQ D0, D1 - Here if D0 is equal to D1 then value 1 will be stored in register D0, else 0 will be stored in the register D0
#
# CGE - This instruction will be used to check for greater than or equal to condition between two registers. CGE D0, D1 - Here if D0 is greater than or equal to D1 then value 1 will be stored in register D0, else 0 will be stored in the register D0.
#
# CLE  - This instruction will be used to check for lesser than or equal to condition between two registers. CLE D0,D1 - Here if D0 is lesser than or equal to D1 then value 1 will be stored in register D0, else 0 will be stored in the register D0.
#
# CLT - This instruction will be used to check for lesser than condition between two registers. CLT D0, D1 - Here if D0 is lesser than D1 then value 1 will be stored in register D0, else 0 will be stored in the register D0.
#
# ADD - This instruction will add the values of two registers. ADD D0,D1 - Here we will be adding two registers values D0 and D1 and result will be stored back to D0.
#
# SUB - This instruction will subtract values of two registers. SUB D0,D1 - Here we will be subtraction D0 from D1 that is D0-D1 and result will be stored back to D0.
#
# MUL - This instruction will multiply values of two registers. MUL D0,D1 - Here we will be multiplying D0 and D1 and product will be stored back to D0.
#
# DIV - This instruction will divide values of two registers. DIV D0,D1 - Here D0 will be divided by D1 and quotient will be stored back to D0.
#
# CALL - this instruction is used for calling/executing a function. CALL func1 - here we are calling function func1
#
# BEQ label - This instruction is used for branching. Here if 0 is stored in register D0, then branching will take place and next instruction will be after label. If 1 or any value other than 0 is stored then no branching will occur as a result, next instruction will be immediately after BEQ instruction.
#
# BNE label - This instruction is used for branching. It is opposite of BEQ. If 0 is stored in register D0 then branching will not take placed so next instruction is the instruction which is immediate to the BNE. If 1 or any value other than 0 is stored in D0, then branch will take place and next instruction is the one after label.
#
# JMP label - This instruction is used for branching without condition. When used next instruction will be the instruction following label and not the instruction which is next to JMP instruction.
#
# OR - this will do a logical or of two values. That is D0 || D1. If D0 0 and D1 is 100 then after OR D0, D1 instruction D0 will have 1 as any value other than 0 is considered as logical 1.
#
# AND - this will do a logical and of two values. That is D0 && D1. If D0 0 and D1 is 100 then after AND D0, D1 instruction D0 will have 0. Similarly if D0 100 and D1 is 1 then after operation D1 will have 1 as any value other than 0 is considered as 1.

######################################################################################################################
######################################################################################################################
import BaSimPL_Compiler as compiler
import BaSimPL_DummyRuntime as runtime
import BaSimPL_Parser as parser
import BaSimPL_Execute as executor


class SimpleInterpreter(object):
    def __init__(self):
        self._inputFile = ''
        self._outputFile = ''
        self._debugMode = 0

    @property
    def InputFile(self):
        return self._inputFile

    @InputFile.setter
    def InputFile(self, value):
        self._inputFile = value

    @property
    def IntermediateFile(self):
        return self._outputFile

    @IntermediateFile.setter
    def IntermediateFile(self, value):
        self._outputFile = value

    @property
    def DebugFlag(self):
        return self._debugMode

    @DebugFlag.setter
    def DebugFlag(self, value):
        self._debugMode = value

    def runTests(self):
        if self._debugMode == 1:
            print 'Execute the sample programs with debug mode ON'
            executor.RunTestWithDebug()
            print 'Finished execution of sample programs'
        else:
            print 'Execute the sample program with debug mode OFF'
            executor.RunTestWithoutDebug()
            print 'Finished execution of sample programs'

    def interpret(self):
        if self._inputFile == '':
            print 'ERROR:: No input program file is provided. USAGE:: BaSimpPL_Execute inputfile=filename.smpl debug=1 outputfile=bytecodefilename.bspl'
            return
        else:
            outputFile = ''
            if self._outputFile == '':
                print 'WARNING:: No intermediate file name provided so default output file name = intermediateFile.bspl will be assumed'
                outputFile = 'intermediateFile.bspl'
            else:
                outputFile = self._outputFile

            if self._debugMode == 1:
                print 'DEBUG MODE IS ON'

            Basimplcc = compiler.Compiler(self._inputFile)
            Basimplcc.DebugState = self._debugMode
            Basimplcc.OutputIntermediateFile = outputFile
            Basimplcc.generate_intermediate_file()
            Basimplip = runtime.DummyRunTime(Basimplcc.OutputIntermediateFile)
            Basimplip.DebugFlag = self._debugMode
            Basimplip.executecode()

            print 'DONE with the execution... now exiting'


