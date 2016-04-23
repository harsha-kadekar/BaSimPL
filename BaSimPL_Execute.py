# Name: BaSimPL_Execute
# Description: This file will hold all the functions to execute the compiler and interpreter of
#              'Basic Simple Programming Language' (BaSimPL). It will also have functions to text it.

import BaSimPL_Lexxer as Lex
import BaSimPL_Compiler as CC
import BaSimPL_Parser as par
import BaSimPL_Interpreter as interep

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


if __name__=='__main__':
    filename = 'Input.txt'
    file = open(filename)
    characters = file.read()
    file.close()
    Lexxer_Tester(characters)
    # text = '( n / 2 ) * 345 + 34 - ( 4 + 5 ) * 123'
    Parser_Tester(characters)
    Compiler_Tester(filename)