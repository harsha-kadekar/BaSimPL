# Name: BaSimPL_Compiler
# Description: This file holds the classes and functions which help in compiling the 'Basic Simple Programming Language'
#              (BaSimPL). It uses the lexxer and parser to generate an intermediate byte code.
# References: http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
#             https://ruslanspivak.com/lsbasi-part1/

import BaSimPL_Lexxer as Lex
import BaSimPL_Parser as parser


class Compiler(object):
    def __init__(self, text_of_program):
        self._text = text_of_program
        self._List_Of_Tokens = []

    @property
    def Text_of_Program(self):
        return self._text

    @Text_of_Program.setter
    def Text_of_Program(self, value):
        self._text = value

    def run_lexxer(self):
        lexAnalysis = Lex.Lexxer(self._text)
        lexAnalysis.generate_Tokens()
        self._List_Of_Tokens = lexAnalysis.List_Of_Generated_Tokens
        self._position_of_token = 0


