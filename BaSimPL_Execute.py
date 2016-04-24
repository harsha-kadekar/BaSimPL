# Name: BaSimPL_Execute
# Description: This file will hold all the functions to execute the compiler and interpreter of
#              'Basic Simple Programming Language' (BaSimPL). It will also have functions to text it.

import BaSimPL_Lexxer as Lex
import BaSimPL_Compiler as CC
import BaSimPL_Parser as par
import BaSimPL_Interpreter as interep
import BaSimPL_DummyRuntime as runTime

def Lexxer_Tester(text_of_program):
    lexAnalysis = Lex.Lexxer(text_of_program)
    lexAnalysis.generate_Tokens()
    for tok in lexAnalysis.List_Of_Generated_Tokens:
        print tok

def Parser_Tester(text_of_program):
    parser = par.Parser()
    lexAnalysis = Lex.Lexxer(text_of_program)
    lexAnalysis.generate_Tokens()
    parser.List_Of_Tokens = lexAnalysis.List_Of_Generated_Tokens
    parser.ParseIt()
    for line in parser._IntermediateCode:
        print line

def Compiler_Tester(file_name):
    Basimplcc = CC.Compiler(file_name)
    Basimplcc.DebugState = 1
    Basimplcc.generate_intermediate_file()

def Interpreter_Test(file_name, debug=0, outputfile='intermediate.bspl'):
    Basimplcc = CC.Compiler(file_name)
    Basimplcc.DebugState = debug
    Basimplcc.OutputIntermediateFile = outputfile
    Basimplcc.generate_intermediate_file()
    Basimplip = runTime.DummyRunTime(Basimplcc.OutputIntermediateFile)
    Basimplip.DebugFlag = debug
    Basimplip.executecode()


if __name__=='__main__':
    # filename = 'Input_1.txt'
    inFile1 = 'factorial_iterative.smpl'
    inFile2 = 'factorial_recursive.smpl'
    inFile3 = 'hemachandra_fibonacci.smpl'

    outFile1 = 'factorial_iterative.bspl'
    outFile2 = 'factorial_recursive.bspl'
    outFile3 = 'hemachandra_fibonacci.bspl'

    # file = open(filename)
    # characters = file.read()
    # file.close()
    # Lexxer_Tester(characters)
    # text = '( n / 2 ) * 345 + 34 - ( 4 + 5 ) * 123'
    # Parser_Tester(characters)
    # Compiler_Tester(filename)

    #Interpreter_Test(inFile1, 1, outFile1)
    #Interpreter_Test(inFile2, 1, outFile2)
    #Interpreter_Test(inFile3, 1, outFile3)

    Interpreter_Test(inFile1, 0, outFile1)
    Interpreter_Test(inFile2, 0, outFile2)
    Interpreter_Test(inFile3, 0, outFile3)
    str = 'done'