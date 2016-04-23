# Name: BaSimPL_Parser
# Description: This file holds the classes and functions which help in parsing the 'Basic Simple Programming Language'
#              (BaSimPL) using the tokens generated by the Lexxer of BaSimPL.
# References: http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
#             https://ruslanspivak.com/lsbasi-part1/
#             http://compilers.iecc.com/crenshaw/tutorfinal.pdf


import BaSimPL_Lexxer as Lex
import SymbolTable as syTable
import Entry as entItem

#####################################################################################################################
#               GRAMMAR OF BaSimPL                                                                                  #
#####################################################################################################################

# program -> topLevelDeclarations*
# topLevelDeclaration -> functionDecl | GlobalDataDecl | globalAssignment
# GlobalDecl -> TYPE_DECL declList SEMICOLON
# DataDecl -> TYPE_DECL declList SEMI_COLON
# functionDecl -> FUNCT_DEF funcReturnType ID OPEN_BRACE PARAMETER_LIST CLOSE_BRACE funBlock
# funReturnType -> VOID | INT_TYPE
# declList -> ID { COMA ID }
# funBlock -> SEG_OPEN declRegion SEQSTATMENTS SEG_CLOSE
# declRegion -> DataDecl*
# globalAssignment -> ID ASSIGN_OPERATOR INT SEMI_COLON
# PARAMETER_LIST -> TYPE_DECL ID { COMA TYPE_DECL ID }
# TYPE_DECL -> INT_TYPE

# SEQSTATEMENTS -> STATEMENT {STATEMENT}
# STATEMENT -> simpleSTATEMENT | compoundSTATEMENT
# simpleSTATEMENT -> assignmentSTATEMENT | procedureSTATEMENT | returnStatement
# compoundSTATEMENT -> ifSTATEMENT | whileSTATEMENT
# assignmentSTATEMENT -> ID ASSIGNT_OPERATOR expression SEMI_COLON
# ifSTATEMENT -> IF OPEN_BRACE expression CLOSE_BRACE SEG_OPEN SEQSTATEMENTS SEG_CLOSE {ELSE SEG_OPEN SEQSTATEMENTS SEG_CLOSE}
# whileSTATEMENT -> WHILE OPEN_BRACE expression CLOSE_BRACE SEG_OPEN SEQSTATEMENTS SEG_CLOSE
# Expression -> bterm [ OR_OPR bterm]*
# bterm -> notfactor [AND_OPR notfactor]*
# notfactor -> [NOT] bfactor
# bfactor -> INT | ID | relation
# procedureSTATEMENT -> procedureCall SEMI_COLON
# procedureCall -> ID OPEN_BRACE ARGU_LIST* CLOSE_BRACE
# returnStatement -> FUN_RETURN returnValues SEMI_COLON
# returnValues -> ID | INT | NULL
# ARGU_LIST -> ID {COMMA ID }
# relation -> simpleExpression { relationalOperator simpleExpression}
# simpleExpression -> term { ADDSUB_OPERATOR term}
# term -> factor { MULDIV_OPERATOR factor}
# factor -> OPEN_BRACE simpleExpression CLOSE_BRACE | ID | INT | procedureCall
# ADDSUB_OPEATOR -> ADD_OPERATOR | SUB_OPERATOR
# MULDIV_OPERATOR -> MUL_OPERATOR | DIV_OPERATOR
# relationalOperator ->  EQUALS | GREATER | LESSER | GREATEREQUAL | LESSEREQUAL | NOTEQUAL
# INT -> [0-9]{[0-9]}
# ID -> [a-zA-Z]{[a-zA-Z0-9_]}
# OPEN_BRACE -> "("
# CLOSE_BRACE -> ")"
# SEG_OPEN -> "{"
# SEG_CLOSE -> "}"
# IF -> "if"
# ELSE -> "else"
# WHILE -> "while"
# ADD_OPERATOR -> "+"
# SUB_OPERATOR -> "-"
# MUL_OPERATOR -> "*"
# DIV_OPERATOR -> "/"
# ASSIGNT_OPERATOR -> "=="
# EQUALS -> "="
# SEMI_COLON -> ";"
# FUNCT_DEF -> "funct"
# VOID -> "void"
# INT_TYPE -> "int"
# COMMA -> ","
# FUN_RETURN -> "return"

#####################################################################################################################
#####################################################################################################################


# Name: Parser
# Description: This class is responsible for the semantic & syntactic analysis of the 'Basic Simple Programming Language'
#              This is a recursive descent parsing
class Parser(object):
    def __init__(self):
        self._position_of_token = -1
        self._List_Of_Tokens = []
        self._current_token = None
        self._Label_Counter = 0
        self._Line_Counter = -1
        self._globalTable = syTable.SymTable(None)
        self._curSymTable = None

    @property
    def List_Of_Tokens(self):
        return self._List_Of_Tokens

    @List_Of_Tokens.setter
    def List_Of_Tokens(self, value):
        self._List_Of_Tokens = value
        self._position_of_token = 0

    def get_next_token(self):
        token = Lex.Token(Lex.Defined_Token_Types.EOF, None)
        if self._position_of_token < self._List_Of_Tokens.__len__():
            token = self._List_Of_Tokens[self._position_of_token]
            self._position_of_token += 1
        # self._current_token = token
        return token

    def peek_next_token(self):
        token = Lex.Token(Lex.Defined_Token_Types.EOF, None)
        if self._position_of_token < self._List_Of_Tokens.__len__():
            token = self._List_Of_Tokens[self._position_of_token]
        return token

    def Error(self, errormsg):
        raise Exception('ERROR while parsing '+errormsg)

    def generate_labels(self, type, startOrend):
        label = type + '_'
        if startOrend == 1:
            label += 'BEGIN_'
        else:
            label += 'END_'
        label += self._Label_Counter.__str__()
        self._Label_Counter += 1

        return label

    def Program(self):
        # while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.EOF:
        #    if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
        # symTable = syTable.SymTable(None)
        while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.EOF:
            self.TopLevelDeclaration()
        return

    def TopLevelDeclaration(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.FUNCTION_DEFINITION:
            self._current_token = self.get_next_token()
            self.FunctionDeclaration()
        elif self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
            self.GlobalDataDeclaration()
        elif self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
            self.GlobalAssignment()
        else:
            errorMsg = 'Invalid token - Should have been a global declaration, global assignment or function'
            self.Error(errorMsg)
        return

    def GlobalDataDeclaration(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
            # Need to make an entry in the symbol table
            # Also allocate in symbol table
            self._current_token = self.get_next_token()
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
                # Allocate it in symbol table
                if self._globalTable.searchTable(self._current_token.Value_Of_Token):
                    errorMsg = 'Aldready a variable called ' + self._current_token.Value_Of_Token + ' is defined'
                    self.Error(errorMsg)
                    return

                print 'ALOC VAR.' + self._current_token.Value_Of_Token
                self._Line_Counter += 1
                NewEntry = entItem.Entry(self._current_token.Value_Of_Token, self._Line_Counter, 'INT_VAR', None, None)
                self._globalTable.initEntry(self._current_token.Value_Of_Token, NewEntry)

                self._current_token = self.get_next_token()
                while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.COMMA:
                    self._current_token = self.get_next_token()
                    if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
                        if self._globalTable.searchTable(self._current_token.Value_Of_Token):
                            errorMsg = 'Aldready a variable called ' + self._current_token.Value_Of_Token + ' is defined'
                            self.Error(errorMsg)
                            return

                        print 'ALOC VAR.' + self._current_token.Value_Of_Token
                        self._Line_Counter += 1
                        NewEntry = entItem.Entry(self._current_token.Value_Of_Token, self._Line_Counter, 'INT_VAR', None, None)
                        self._globalTable.initEntry(self._current_token.Value_Of_Token, NewEntry)
                    else:
                        errorMsg = 'expected an identifier'
                        self.Error(errorMsg)
                    self._current_token = self.get_next_token()

                if self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEMICOLON:
                    errorMsg = 'Expected a ;'
                    self.Error(errorMsg)
                    return
                self._current_token = self.get_next_token()
            else:
                errorMsg = 'Expected an identifier'
                self.Error(errorMsg)
        else:
            errorMsg = 'Invalid type'
            self.Error(errorMsg)

        return

    def DataDeclaration(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
            # Need to make an entry in the symbol table
            # Also allocate in symbol table
            self._current_token = self.get_next_token()
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
                # Allocate it in symbol table
                if self._curSymTable.searchCurrentTable(self._current_token.Value_Of_Token):
                    errorMsg = 'A variable ' + self._current_token.Value_Of_Token + ' is already declared'
                    self.Error(errorMsg)
                    return
                print 'ALOC VAR.' + self._current_token.Value_Of_Token
                self._Line_Counter += 1
                NewEntry = entItem.Entry(self._current_token.Value_Of_Token, self._Line_Counter, 'INT_VAR', None, None)
                self._curSymTable.initEntry(self._current_token.Value_Of_Token, NewEntry)

                self._current_token = self.get_next_token()
                while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.COMMA:
                    self._current_token = self.get_next_token()
                    if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
                        #Allocate it in symbol table
                        if self._curSymTable.searchCurrentTable(self._current_token.Value_Of_Token):
                            errorMsg = 'A variable ' + self._current_token.Value_Of_Token + ' is already declared'
                            self.Error(errorMsg)
                            return
                        print 'ALOC VAR.' + self._current_token.Value_Of_Token
                        self._Line_Counter += 1
                        NewEntry = entItem.Entry(self._current_token.Value_Of_Token, self._Line_Counter, 'INT_VAR', None, None)
                        self._curSymTable.initEntry(self._current_token.Value_Of_Token, NewEntry)
                    else:
                        errorMsg = 'expected an identifier'
                        self.Error(errorMsg)
                    self._current_token = self.get_next_token()

                if self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEMICOLON:
                    errorMsg = 'Expected a ;'
                    self.Error(errorMsg)
                    return
                self._current_token = self.get_next_token()
            else:
                errorMsg = 'Expected an identifier'
                self.Error(errorMsg)
        else:
            errorMsg = 'Invalid type'
            self.Error(errorMsg)
        return

    def FunctionDeclaration(self):
        returnType = 0  # default trying to treat as void
        functionName = ''
        paramList = []
        self._curSymTable = syTable.SymTable(self._globalTable)

        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.VOID:
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.VOID:
                # No return type So then dont allocate anyting.
                returnType = 0
            elif self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
                # Function is going to return an integer value
                returnType = 1
            else:
                errorMsg = 'Invalid return type'
                self.Error(errorMsg)
                return

            self._current_token = self.get_next_token()
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
                labelOfFunction = self.generate_labels('FUNCT', 1)
                functionName = self._current_token.Value_Of_Token
                labelOfFunction = labelOfFunction + '_' + functionName
                if self._globalTable.searchTable(self._current_token.Value_Of_Token):
                    errorMsg = 'Already a function/variable with name ' + functionName + ' exists'
                    self.Error(errorMsg)
                    return
                self._current_token = self.get_next_token()
                if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.OPEN_BRACE:
                    self._current_token = self.get_next_token()
                    while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.CLOSE_BRACE:
                        #Handle Parameters
                        paramType = 0
                        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
                            paramType = 1
                        else:
                            errorMsg = 'Invalid Parameter Type'
                            self.Error(errorMsg)
                            return
                        self._current_token = self.get_next_token()

                        if self._current_token.Type_Of_Token != Lex.Defined_Token_Types.IDENTIFIER:
                            errorMsg = 'Expected an identifier'
                            self.Error(errorMsg)
                            return

                        param = (paramType, self._current_token.Value_Of_Token)
                        paramList.append(param)
                        self._current_token = self.get_next_token()

                        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.COMMA:
                            self._current_token = self.get_next_token()

                    print labelOfFunction + ':'
                    self._Line_Counter += 1
                    NewEntry = entItem.Entry(functionName, self._Line_Counter, 'FUNCT', None, returnType)
                    NewEntry.symParamList = paramList
                    self._globalTable.initEntry(functionName, NewEntry)
                    for param in paramList:
                        if self._curSymTable.searchCurrentTable(param[1]):
                            errorMsg = 'Already parameter ' + param[1] + ' is defined'
                            self.Error(errorMsg)
                            return
                        print 'ALOC VAR.' + param[1]
                        self._Line_Counter += 1
                        NewEntry = entItem.Entry(param[1], self._Line_Counter, 'VAR', None, None)
                        self._curSymTable.initEntry(param[1], NewEntry)
                        print 'POP D0'
                        self._Line_Counter += 1
                        print 'LEA A0, '+self._Line_Counter.__str__()+'(PC)'
                        self._Line_Counter += 1
                        print 'MOV (A0), D0'
                        self._Line_Counter += 1

                    self._current_token = self.get_next_token()
                    self.FunctionBody()
                else:
                    errorMsg = 'Expected ('
                    self.Error(errorMsg)

            else:
                errorMsg = 'Expected an identifier'
                self.Error(errorMsg)
        else:
            errorMsg = 'Expected a return type'
            self.Error(errorMsg)
        return

    def FunctionBody(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SEG_OPEN:
            self._current_token = self.get_next_token()
            #while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEG_CLOSE:
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
                self.DeclRegion()
            self.SeqStatements()
        else:
            errorMsg = 'Expected {'
            self.Error(errorMsg)
        return

    def DeclRegion(self):
        while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT_TYPE:
            self.DataDeclaration()
            # self._current_token = self.get_next_token()
        return

    def GlobalAssignment(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
            variable = self._current_token.Value_Of_Token
            if not self._globalTable.searchTable(variable):
                errorMsg = 'Variable ' + variable + ' is not yet declared'
                self.Error(errorMsg)
                return
            entry = self._globalTable.getEntry(variable)
            if entry is None:
                errorMsg = 'Entry is None'
                self.Error(errorMsg)
                return

            location = entry.symLocation
            self._current_token = self.get_next_token()
            if self._current_token is not None and self._current_token.Type_Of_Token == Lex.Defined_Token_Types.ASSIGNMENT_OPERATOR:
                self._current_token = self.get_next_token()
                self.Expression()
                if self._current_token is not None and self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SEMICOLON:
                    print 'LEA A0, ' + location.__str__() + '(PC)'
                    print 'POP D0'
                    print 'MOV (A0), D0'
                    self._Line_Counter += 3
                    self._current_token = self.get_next_token()
                else:
                    errormsg = 'Expected a Semicolon ; but got some other token'
                    self.Error(errormsg)
            else:
                errormsg = 'Expected an assignment operator'
                self.Error(errormsg)
        else:
            errorMsg = 'Expected an identifier'
            self.Error(errorMsg)

        return

    def SimpleExpression(self):
        self.Term()
        # print 'MOV D0, D1'
        # Push it to a stack or move it to a register
        while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.ADD_OPERATOR or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SUB_OPERATOR:
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.ADD_OPERATOR:
                self._current_token = self.get_next_token()
                self.Term()
                print 'POP D1'
                print 'POP D0'
                print 'ADD D0, D1'
            else:
                self._current_token = self.get_next_token()
                self.Term()
                print 'POP D1'
                print 'POP D0'
                print 'SUB D0, D1'
            print 'PUSH D0'
            self._Line_Counter += 4
        return

    def SeqStatements(self):

        while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEG_CLOSE:
            self.Statements()

        self._current_token = self.get_next_token()

        return

    def Statements(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IF or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.WHILE:
            self.CompoundStatement()
        else:
            self.SimpleStatement()

        return

    def SimpleStatement(self):
        next_token = self.peek_next_token()
        if next_token.Type_Of_Token == Lex.Defined_Token_Types.OPEN_BRACE:
            function_call = self._current_token.Value_Of_Token
            self._current_token = self.get_next_token()
            if not self._globalTable.searchTable(function_call):
                errorMsg = 'Function declaration not found'
                self.Error(errorMsg)
                return
            location = self._globalTable.getEntry(function_call).symLocation
            self._current_token = self.get_next_token()
            nParamCount = 0
            while self._current_token != Lex.Defined_Token_Types.CLOSE_BRACE:
                self.Expression()
                nParamCount += 1
                if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.COMMA:
                    self._current_token = self.get_next_token()

            self._current_token = self.get_next_token()
            print 'CALL ' + function_call + ' ' + location.__str__()
            self._Line_Counter += 1
        elif self._current_token.Type_Of_Token == Lex.Defined_Token_Types.RETURN:
            self.HandleReturnStatement()
        else:
            self.AssignmentStatement()
        return

    def HandleReturnStatement(self):
        self._current_token = self.get_next_token()
        if self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEMICOLON:
            self.Expression()
            if self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEMICOLON:
                errorMsg = 'Expected a ;'
                self.Error(errorMsg)
                return
        print 'ret'
        self._Line_Counter += 1
        self._current_token = self.get_next_token()


    def CompoundStatement(self):
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IF:
            self.IfStatement()
        else:
            self.WhileStatement()
        return

    def AssignmentStatement(self):
        # ID = expression ;

        if self._current_token is not None and self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
            variable = self._current_token.Value_Of_Token

            if not self._curSymTable.searchTable(variable):
                errorMsg = 'Variable ' + variable + ' is not declared'
                self.Error(errorMsg)
                return
            entry = self._curSymTable.getEntry(variable)

            self._current_token = self.get_next_token()
            if self._current_token is not None and self._current_token.Type_Of_Token == Lex.Defined_Token_Types.ASSIGNMENT_OPERATOR:
                self._current_token = self.get_next_token()
                self.Expression()
                if self._current_token is not None and self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SEMICOLON:
                    print 'LEA A0, ' + entry.symLocation.__str__() + '(PC)'
                    print 'POP D0'
                    print 'MOV (A0), D0'
                    self._Line_Counter += 3
                    self._current_token = self.get_next_token()
                else:
                    errormsg = 'Expected a Semicolon ; but got some other token'
                    self.Error(errormsg)
            else:
                errormsg = 'Expected an assignment operator'
                self.Error(errormsg)
        else:
            errormsg = 'Expected an identifier'
            self.Error(errormsg)

        return

    def IfStatement(self):
        self._current_token = self.get_next_token()
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.OPEN_BRACE:
            endIflabel = self.generate_labels('IF', 0)
            endElselable = endIflabel
            self._current_token = self.get_next_token()
            self.Expression()
            print 'POP D0'
            print 'BEQ '+endIflabel
            self._Line_Counter += 2
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.CLOSE_BRACE:
                self._current_token = self.get_next_token()
                if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SEG_OPEN:
                    self._current_token = self.get_next_token()
                    while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEG_CLOSE:
                        self.Statements()
                    self._current_token = self.get_next_token()

                    if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.ELSE:
                        self._current_token = self.get_next_token()
                        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SEG_OPEN:
                            endElselable = self.generate_labels('ELSE', 0)
                            print 'JMP ' + endIflabel
                            self._Line_Counter += 1
                            print endIflabel + ':'
                            self._Line_Counter += 1
                            self._current_token = self.get_next_token()
                            while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEG_CLOSE:
                                self.Statements()
                            self._current_token = self.get_next_token()
                        else:
                            errorMsg = 'Expected }'
                            self.Error(errorMsg)

                    print endElselable + ':'
                    self._Line_Counter += 1
                else:
                    errorMsg = 'Expected {'
                    self.Error(errorMsg)
            else:
                errorMsg = 'Expected )'
                self.Error(errorMsg)
        else:
            errorMsg = 'Expected ('
            self.Error(errorMsg)

        return

    def WhileStatement(self):
        self._current_token = self.get_next_token()
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.OPEN_BRACE:
            endWhileLabel = self.generate_labels('WHILE', 0)
            startWhileLabel = self.generate_labels('WHILE', 1)
            self._current_token = self.get_next_token()
            print startWhileLabel + ':'
            self._Line_Counter += 1
            self.Expression()
            print 'POP D0'
            print 'BEQ ' + endWhileLabel
            self._Line_Counter += 2
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.CLOSE_BRACE:
                self._current_token = self.get_next_token()
                if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.SEG_OPEN:
                    self._current_token = self.get_next_token()
                    while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.SEG_CLOSE:
                        self.Statements()
                    self._current_token = self.get_next_token()
                    print 'JMP ' + startWhileLabel
                    self._Line_Counter += 1
                    print endWhileLabel + ':'
                    self._Line_Counter += 1
                else:
                    errorMsg = 'Expected {'
                    self.Error(errorMsg)
            else:
                errorMsg = 'Expected )'
                self.Error(errorMsg)
        else:
            errorMsg = 'Expected ('
            self.Error(errorMsg)
        return

    def Expression(self):
        self.BTerm()
        while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.LOG_OR_OPERATOR:
            self._current_token = self.get_next_token()
            self.BTerm()
            print 'POP D1'
            print 'POP D0'
            print 'OR D0, D1'
            print 'PUSH D0'
            self._Line_Counter += 4

        return

    def Relation(self):
        self.SimpleExpression()
        while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.GREATEREQUAL_OPERATOR or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.GREATERTHAN_OPERATOR or \
            self._current_token.Type_Of_Token == Lex.Defined_Token_Types.LESSERTHAN_OPERATOR or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.LESSEREQUAL_OPERATOR or \
            self._current_token.Type_Of_Token == Lex.Defined_Token_Types.EQUALS_OPERATOR or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.NOTEQUAL_OPERATOR:
            relop = self._current_token.Type_Of_Token
            self._current_token = self.get_next_token()
            self.Expression()
            print 'POP D1'
            print 'POP D0'
            if relop == Lex.Defined_Token_Types.NOTEQUAL_OPERATOR:
                print 'CNE D0, D1'
            elif relop == Lex.Defined_Token_Types.EQUALS_OPERATOR:
                print 'CEQ D0,D1'
            elif relop == Lex.Defined_Token_Types.GREATERTHAN_OPERATOR:
                print 'CGT D0,D1'
            elif relop == Lex.Defined_Token_Types.GREATEREQUAL_OPERATOR:
                print 'CGE D0,D1'
            elif relop == Lex.Defined_Token_Types.LESSEREQUAL_OPERATOR:
                print 'CLE D0,D1'
            else:
                print 'CLT D0,D1'
            print 'PUSH D0'
            self._Line_Counter += 4
        return

    def BTerm(self):
        self.NotFactor()
        while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.LOG_AND_OPERATOR:
            self._current_token = self.get_next_token()
            self.NotFactor()
            print 'POP D1'
            print 'POP D0'
            print 'AND D0, D1'
            print 'PUSH D0'
            self._Line_Counter += 4
        return

    def NotFactor(self):
        # As of now it is directly calling next step. Future It will do the logical not operation.
        self.BFactor()
        return

    def BFactor(self):
        self.Relation()
        return

    def Term(self):
        self.Factor()
        #print 'MOV D0, D1'
        while self._current_token.Type_Of_Token == Lex.Defined_Token_Types.MUL_OPERATOR or self._current_token.Type_Of_Token == Lex.Defined_Token_Types.DIV_OPERATOR:
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.MUL_OPERATOR:
                self._current_token = self.get_next_token()
                self.Factor()
                print 'POP D1'
                print 'POP D0'
                print 'MUL D0, D1'

            else:
                self._current_token = self.get_next_token()
                self.Factor()
                print 'POP D1'
                print 'POP D0'
                print 'DIV D0, D1'
            print 'PUSH D0'
            self._Line_Counter += 4

        return

    def Factor(self):
        # Token should be either an integer or an identifier
        if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.INT:
            # This is a constant
            #movi A, value
            print 'MOVI D0, ' + self._current_token.Value_Of_Token
            print 'PUSH D0'
            self._Line_Counter += 2
            self._current_token = self.get_next_token()
        elif self._current_token.Type_Of_Token == Lex.Defined_Token_Types.IDENTIFIER:
            next_token = self.peek_next_token()
            if next_token.Type_Of_Token == Lex.Defined_Token_Types.OPEN_BRACE:
                # print 'PUSH $RA'

                function_call = self._current_token.Value_Of_Token
                self._current_token = self.get_next_token()
                if not self._globalTable.searchTable(function_call):
                    errorMsg = 'Function '+ function_call + ' is not declared'
                    self.Error(errorMsg)
                    return
                nCount = 0
                entry = self._curSymTable.getEntry(function_call)
                self._current_token = self.get_next_token()
                while self._current_token.Type_Of_Token != Lex.Defined_Token_Types.CLOSE_BRACE:
                    self.Expression()
                    nCount += 1
                    if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.COMMA:
                        self._current_token = self.get_next_token()

                if nCount != entry.symParamList.__len__():
                    errorMsg = 'Arguments number mismatch'
                    self.Error(errorMsg)
                    return
                print 'CALL ' + function_call + ' ' + entry.symLocation.__str__()
                print 'POP D0'
                print 'PUSH D0'                                                                 #Return Value
                self._Line_Counter += 3
                self._current_token = self.get_next_token()
            else:
                if not self._curSymTable.searchTable(self._current_token.Value_Of_Token):
                    errorMsg = 'variable ' + self._current_token.Value_Of_Token + ' is not declared'
                    self.Error(errorMsg)
                    return
                entry = self._curSymTable.getEntry(self._current_token.Value_Of_Token)

                print 'LEA A0, ' + entry._symLocation.__str__() + '(PC)'
                print 'MOV D0, (A0)'
                print 'PUSH D0'
                self._Line_Counter += 3
                self._current_token = self.get_next_token()
        elif self._current_token.Type_Of_Token == Lex.Defined_Token_Types.OPEN_BRACE:
            self._current_token = self.get_next_token()
            self.Expression()
            if self._current_token.Type_Of_Token == Lex.Defined_Token_Types.CLOSE_BRACE:
                self._current_token = self.get_next_token()
            else:
                errormsg = 'Expected a closing bracket'
                self.Error(errormsg)
        else:
            errormsg = 'Exepected a value or an identifier'
            self.Error(errormsg)
        return

    def ParseIt(self):
        # self.SeqStatements()
        self._current_token = self.get_next_token()
        self.Program()
        # self.SeqStatements()
        # self.AssignmentStatement()
        # self.SimpleExpression()
        return





