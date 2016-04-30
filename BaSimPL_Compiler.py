# Name: BaSimPL_Compiler
# Description: This file holds the classes and functions which help in compiling the 'Basic Simple Programming Language'
#              (BaSimPL). It uses the lexxer and parser to generate an intermediate byte code.
# References: http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
#             https://ruslanspivak.com/lsbasi-part1/

import BaSimPL_Lexxer as Lex
import BaSimPL_Parser as parser


class Compiler(object):
    def __init__(self, inputFile):
        self._text = ''
        self._List_Of_Tokens = []
        self._IntermediateCode = []
        self._InputFile = inputFile
        self._debug = 0
        self._outputfile = 'intermedate.bspl'

    @property
    def InputProgramFile(self):
        return self._InputFile

    @InputProgramFile.setter
    def InputProgramFile(self, value):
        self._InputFile = value
        self._text = ''

    @property
    def DebugState(self):
        return self._debug

    @DebugState.setter
    def DebugState(self, value):
        self._debug = value

    @property
    def OutputIntermediateFile(self):
        return self._outputfile

    @OutputIntermediateFile.setter
    def OutputIntermediateFile(self, value):
        self._outputfile = value

    def readinputfile(self):
        file = open(self._InputFile)
        self._text = file.read()
        file.close()

    def run_lexxer(self):
        if self._text == '':
            self.readinputfile()
        lexAnalysis = Lex.Lexxer(self._text)
        lexAnalysis.DebugMode = self._debug
        lexAnalysis.generate_Tokens()
        self._List_Of_Tokens = lexAnalysis.List_Of_Generated_Tokens

    def run_parser(self):
        if self._List_Of_Tokens.__len__() == 0:
            self.run_lexxer()
        pars = parser.Parser()
        pars.DebugFlag = self._debug
        pars.List_Of_Tokens = self._List_Of_Tokens
        pars.ParseIt()
        self._IntermediateCode = pars.IntermediateByteCode

    def generate_intermediate_file(self):
        if self._IntermediateCode.__len__() == 0:
            self.run_parser()

        infile = open(self._outputfile, 'w')
        for line in self._IntermediateCode:
            infile.write(line)
            infile.write('\n')




