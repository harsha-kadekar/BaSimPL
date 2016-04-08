# Name: BaSimPL_Lexxer
# Description: This file holds the classes and functions which helps in identifying Tokens of the programming
#              language 'Basic Simple Programming Language' (BaSimPL)
# References: http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
#             https://ruslanspivak.com/lsbasi-part1/

import re as regex


# Name: Token
# Description: This class represents a token identified by the Lexxer. Each token has value which will store the
#              actual matched string and type which tells the class of token that represents.
class Token(object):
    def __init__(self, type_of_token, value):
        self._type = type_of_token
        self._value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self._type, value=repr(self._value))

    def __repr__(self):
        return self.__str__()


# Name: Defined_Token_Types
# Description: This class holds the different class or types of Tokens BaSimPL can have
class Defined_Token_Types(object):
    INT = 'INT'
    IDENTIFIER = 'ID'
    ADD_OPERATOR = 'ADD'
    SUB_OPERATOR = 'SUB'
    MUL_OPERATOR = 'MUL'
    DIV_OPERATOR = 'DIV'
    EQUALS_OPERATOR = 'EQUALS'
    ASSIGNMENT_OPERATOR = 'ASSIGN'
    GREATERTHAN_OPERATOR = 'GREATER'
    LESSERTHAN_OPERATOR = 'LESSER'
    GREATEREQUAL_OPERATOR = 'GREATEREQUAL'
    LESSEREQUAL_OPERATOR = 'LESSEREQUAL'
    NOTEQUAL_OPERATOR = 'NOTEQUAL'
    OPEN_BRACE = 'OPEN_BRACE'
    CLOSE_BRACE = 'CLOSE_BRACE'
    LOG_AND_OPERATOR = 'AND'
    LOG_OR_OPERATOR = 'OR'
    LOG_NOT_OPERATOR = 'NOT'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    SEG_OPEN = 'SEG_OPEN'
    SEG_CLOSE = 'SEG_CLOSE'
    SEMICOLON = 'SEMI_COLON'
    COMMA = 'COMMA'
    IN_MODE = 'IN_MODE'
    OUT_MODE = 'OUT_MODE'
    EOF = 'EOF'


# Name: Lexxer
# Description:
class Lexxer(object):
    def __init__(self, text):
        self._text = text
        self.Tokens_Expression = [
            (r'[ \n\t]+', None),
            (r'\\[^\n]*', None),
            (r'\=', Defined_Token_Types.ASSIGNMENT_OPERATOR),
            (r'\(', Defined_Token_Types.OPEN_BRACE),
            (r'\)', Defined_Token_Types.CLOSE_BRACE),
            (r'\{', Defined_Token_Types.SEG_OPEN),
            (r'\}', Defined_Token_Types.SEG_CLOSE),
            (r'\;', Defined_Token_Types.SEMICOLON),
            (r'\+', Defined_Token_Types.ADD_OPERATOR),
            (r'-', Defined_Token_Types.SUB_OPERATOR),
            (r'\*', Defined_Token_Types.MUL_OPERATOR),
            (r'/', Defined_Token_Types.DIV_OPERATOR),
            (r'>', Defined_Token_Types.GREATERTHAN_OPERATOR),
            (r'<', Defined_Token_Types.LESSERTHAN_OPERATOR),
            (r'>=', Defined_Token_Types.GREATEREQUAL_OPERATOR),
            (r'<=', Defined_Token_Types.LESSEREQUAL_OPERATOR),
            (r'!=', Defined_Token_Types.NOTEQUAL_OPERATOR),
            (r'==', Defined_Token_Types.EQUALS_OPERATOR),
            (r'and', Defined_Token_Types.LOG_AND_OPERATOR),
            (r'or', Defined_Token_Types.LOG_OR_OPERATOR),
            (r'not', Defined_Token_Types.LOG_NOT_OPERATOR),
            (r'if', Defined_Token_Types.IF),
            (r'else', Defined_Token_Types.ELSE),
            (r'while', Defined_Token_Types.WHILE),
            (r'in', Defined_Token_Types.IN_MODE),
            (r'out', Defined_Token_Types.OUT_MODE),
            (r'[0-9]+', Defined_Token_Types.INT),
            (r'[A-Za-z][A-Za-z0-9_]*', Defined_Token_Types.IDENTIFIER)
        ]
        self._List_Of_Generated_Tokens = []

    @property
    def List_Of_Generated_Tokens(self):
        return self._List_Of_Generated_Tokens

    @property
    def Text_Of_Language(self):
        return self._text

    @Text_Of_Language.setter
    def Text_Of_Language(self, text):
        self._text = text

    # Name: generate_Tokens
    # Description: This is the main engine of this class. This will generate the tokens by going through the
    #              text and using regular expressions will generate the tokens.
    def generate_Tokens(self):
        characters = self._text
        self._List_Of_Generated_Tokens = []
        pos = 0
        while pos < len(characters):
            match = None
            for token_expr in self.Tokens_Expression:
                pattern, tag = token_expr
                regexp = regex.compile(pattern)
                match = regexp.match(characters, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = Token(tag, text)
                        self._List_Of_Generated_Tokens.append(token)
                    break
            if not match:
                raise Exception("Illegal characters, Not able to generate tokens")
            else:
                pos = match.end(0)

