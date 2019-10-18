from ast import literal_eval
import sys
from anytree import Node, RenderTree

class Grammar:
    def __init__(self):
        self.tokens = []
        self.tree = []
        with open("token.txt", 'r') as f:
            for line in f:
                line = literal_eval(line)
                self.tokens.append(line)
    
    def getType(self, token):
        return token[0]

    def getValue(self, token):
        return token[1]

    def popToken(self, nodo):
        popped = self.tokens.pop(0)
        popped.append(nodo)
        self.tree.append(popped)
        print("Popped:", popped)

    def printExpectedToken(self, expected):
        print("Expected Token: "+expected+", found ", self.tokens[0], "instead. Near line:", (self.tokens[0][2]))
        sys.exit()

    def isexpected(self, token, tipo, value):
        return self.getType(token) == tipo and self.getValue(token) == value

    def istype(self, token):
        return self.isexpected(token, "keywords", "int") or self.isexpected(token, "keywords", "boolean")

    def isID(self, token):
        return self.getType(token) == "ID"

    def syntaxProgram(self):         
        if self.isexpected(self.tokens[0], "keywords", "class"):
            self.popToken('program')
            if self.isexpected(self.tokens[0], "ID", "Program"):
                self.popToken('program')    
                if self.isexpected(self.tokens[0], "Delimiter", "{"):
                    self.popToken('program')  
                    if not self.isexpected(self.tokens[0], "Delimiter", "}"):  
                        try:
                            while self.isexpected(self.tokens[2], "Delimiter", "["):
                                self.syntaxField_dec()
                            while self.isexpected(self.tokens[2], "Delimiter", "("):
                                self.syntaxMethod_dec()
                        except IndexError:
                            pass
                    if self.isexpected(self.tokens[0], "Delimiter", "}"):
                        self.popToken('program')
                        print("Program OK")
                    else:
                        self.printExpectedToken("['Delimiter', '}']")
                else:
                    self.printExpectedToken("['Delimiter', '{']")
            else:
                self.printExpectedToken("['ID', 'Program']")
        else:
            self.printExpectedToken("['keywords', 'class']")

    def syntaxField_dec(self):
        if self.istype(self.tokens[0]):
            self.popToken('field_dec')      
            while True:
                if self.getType(self.tokens[0]) == "ID":
                    self.popToken('field_dec')    
                    if self.isexpected(self.tokens[0], "Delimiter", "["):
                        self.popToken('field_dec')    
                        if self.getType(self.tokens[0]) == "decimal" or self.getType(self.tokens[0]) == "hexadecimal":
                            self.popToken('field_dec')    
                            if self.isexpected(self.tokens[0], "Delimiter", "]"):
                                self.popToken('field_dec')    
                            else:
                                self.printExpectedToken("['Delimiter', ']']")
                        else:
                            self.printExpectedToken("<int_literal>")
                    elif self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.popToken('field_dec')    
                        continue
                    elif self.isexpected(self.tokens[0], "Delimiter", ";"):
                        self.popToken('field_dec')    
                        break
                    else:
                        self.printExpectedToken("['Delimiter', ';']")
                else:
                    self.printExpectedToken("['ID', '*']")
        else:
            self.printExpectedToken("<type>")


    def syntaxMethod_dec(self): #Could fail due to while statement        
        if self.istype(self.tokens[0]) or self.isexpected(self.tokens[0], "keywords", "void"):
            self.popToken('method_dec')    
            if self.isID(self.tokens[0]):
                self.popToken('method_dec')    
                if self.isexpected(self.tokens[0], "Delimiter", "("):
                    self.popToken('method_dec')    
                    if self.istype(self.tokens[0]):
                        while self.istype(self.tokens[0]):
                            if self.istype(self.tokens[0]):
                                self.popToken('method_dec')    
                                if self.isID(self.tokens[0]):
                                    self.popToken('method_dec')    
                                    if self.isexpected(self.tokens[0], "Delimiter", ","):
                                        self.popToken('method_dec')    
                                        continue
                                    elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                                        self.popToken('method_dec')    
                                        self.syntaxBlock()
                                    else:
                                        self.printExpectedToken("['Delimiter', ')']")
                                else:
                                    self.printExpectedToken("<ID>")
                            else:
                                self.printExpectedToken("<type>")
                    elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken('method_dec')
                        self.syntaxBlock()
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("['Delimiter', '(']")
            else:
                self.printExpectedToken("<ID>")
        else:
            self.printExpectedToken("<method type>")
    
    def syntaxBlock(self):        
        if self.isexpected(self.tokens[0], "Delimiter", "{"):
            self.popToken('block')            
            self.syntaxVar_decl()
            self.syntaxStatement()
            if self.isexpected(self.tokens[0], "Delimiter", "}"):
                self.popToken('block')
            else:
                self.printExpectedToken("['Delimiter','}']")
        else:
            self.printExpectedToken("['Delimiter', '{']")

    def syntaxVar_decl(self):        
        while self.istype(self.tokens[0]):
            self.popToken('var_decl')
            if self.isID(self.tokens[0]):
                self.popToken('var_decl')
                while self.isexpected(self.tokens[0], "Delimiter", ","):
                    self.popToken('var_decl')
                    if self.isID(self.tokens[0]):
                        self.popToken('var_decl')
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('var_decl')
                else:
                    self.printExpectedToken("['Delimiter',';']")
            else:
                self.printExpectedToken("<ID>")            

    """
    def syntaxType(self):
        pass
    """
    def syntaxStatement(self):
        while not self.isexpected(self.tokens[0], "Delimiter", "}"):
            if (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "(")) or self.isexpected(self.tokens[0], "keywords", "callout"):
                #is method_call
                self.syntaxMethod_call()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement')
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isID(self.tokens[0]) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "[")):
                #is location
                self.syntaxLocation()
                if self.isAssignOp(self.tokens[0]):
                    self.popToken('statement')
                    self.syntaxExpr()
                    if self.isexpected(self.tokens[0], "Delimiter", ";"):
                        self.popToken('statement')
                    else:
                        self.printExpectedToken("['Delimiter',';']")
                else:
                    self.printExpectedToken("<assig_op>")
            elif self.isexpected(self.tokens[0], "keywords", "if"):
                #is if
                self.popToken('statement')
                if self.isexpected(self.tokens[0], "Delimiter", "("):
                    self.popToken('statement')
                    self.syntaxExpr()
                    if self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken('statement')
                        self.syntaxBlock()
                        if self.isexpected(self.tokens[0], "keywords", "else"):
                            self.popToken('statement')
                            self.syntaxBlock()
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("['Delimiter','(']")
            elif self.isexpected(self.tokens[0], "keywords", "for"):
                #is for
                self.popToken('statement')
                if self.isID(self.tokens[0]):
                    self.popToken('statement')
                    if self.isexpected(self.tokens[0], "Operator", "="):
                        self.popToken('statement')
                        self.syntaxExpr()
                        if self.isexpected(self.tokens[0], "Delimiter", ","):
                            self.popToken('statement')
                            self.syntaxExpr()
                            self.syntaxBlock()
                        else:
                            self.printExpectedToken("['Delimiter',',']")
                    else:
                        self.printExpectedToken("['Operator','=']")
                else:
                    self.printExpectedToken("<ID>")
            elif self.isexpected(self.tokens[0], "keywords", "return"):
                #is return
                self.popToken('statement')
                self.syntaxExpr()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement')
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "break"):
                #is break
                self.popToken('statement')
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement')
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "continue"):
                #is continue
                self.popToken('statement')
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement')
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "Delimiter", "{"):
                #is block
                self.syntaxBlock()
            else:
                self.printExpectedToken("<statement>")
        
    def syntaxMethod_call(self):        
        if self.isID(self.tokens[0]):
            self.popToken('method_call')
            if self.isexpected(self.tokens[0], "Delimiter", "("):
                self.popToken('method_call')
                if not self.isexpected(self.tokens[0], "Delimiter", ")"):
                    self.syntaxExpr()
                    while self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.popToken('method_call')
                        self.syntaxExpr()
                if self.isexpected(self.tokens[0], "Delimiter", ")"):
                    self.popToken('method_call')
                else:
                    self.printExpectedToken("['Delimiter',')']")
            else:
                self.printExpectedToken("['Delimiter','(']")
        elif self.isexpected(self.tokens[0], "keywords", "callout"):
            self.popToken('method_call')
            if self.isexpected(self.tokens[0], "Delimiter", "("):
                self.popToken('method_call')
                if self.isStringLiteral(self.tokens[0]):
                    self.popToken('method_call')
                    if self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.syntaxCallout_arg()
                        while self.isexpected(self.tokens[0], "Delimiter", ","):
                            self.popToken('method_call')
                            self.syntaxCallout_arg()
                        if self.isexpected(self.tokens[0], "Delimiter", ")"):
                            self.popToken('method_call')
                        else:
                            self.printExpectedToken("['Delimiter',')']")
                    elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken('method_call')
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("<string_literal>")
            else:
                self.printExpectedToken("['Delimiter','(']")
        else:
            self.printExpectedToken("<method_name> or <callout>")

    """
    def syntaxMethod_name(self):
        pass
    """

    def syntaxLocation(self):
        if self.isID(self.tokens[0]):
            self.popToken('location')
            if self.isexpected(self.tokens[0], "Delimiter", "["):
                self.popToken('location')
                self.syntaxExpr()
                if self.isexpected(self.tokens[0], "Delimiter", "]"):
                    self.popToken('location')
                else:
                    self.printExpectedToken("['Delimiter',']']")
        else:
            self.printExpectedToken("<ID>")

    def syntaxExpr(self):                
        if (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "(")) or self.isexpected(self.tokens[0], "keywords", "callout"):
            #is method_call                       
            self.syntaxMethod_call()
        elif (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", ")")) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "[")):
            #is location
            print("is location")
            self.syntaxLocation()
        elif self.isLiteral(self.tokens[0]):
            self.popToken('expr')
        elif self.isexpected(self.tokens[0], "Operator", "-"):
            #is negative
            self.popToken('expr')
            self.syntaxExpr()
        elif self.isexpected(self.tokens[0], "Operator", "!"):
            #is differemt !
            self.popToken('expr')
            self.syntaxExpr()
        elif self.isexpected(self.tokens[0], "Delimiter", "("):
            #is parenthesis expr
            self.popToken('expr')
            self.syntaxExpr()
            if self.isexpected(self.tokens[0], "Delimiter", ")"):
                self.popToken('expr')
            else:
                self.printExpectedToken("['Delimiter',')']")
        elif self.isBinOp(self.tokens[1]):
            #is expr alone
            self.popToken('expr')
            
            if self.isBinOp(self.tokens[0]):
                self.popToken('expr')
                self.syntaxExpr()
            else:
                self.printExpectedToken("<bin_op>")
        else:
            self.printExpectedToken("<expr>")            

    def syntaxCallout_arg(self):        
        if self.isStringLiteral(self.tokens[0]):
            self.popToken('callout_arg')
        else:
            self.syntaxExpr()

    def syntaxBinOp(self):
        if self.isBinOp(self.tokens[0]):
            self.popToken('bin_op')
        else:
            self.printExpectedToken("<bin_op>")

    def isAssignOp(self, token):
        return self.isexpected(token, "Operator", "=") or self.isexpected(token, "Operator", "+=") or self.isexpected(token, "Operator", "-=")

    def isBinOp(self, token):
        return self.isArithOp(token) or self.isRelOp(token) or self.isEqOp(token) or self.isCondOp(token)

    def isArithOp(self, token):
        return self.isexpected(token, "Operator", "+") or self.isexpected(token, "Operator", "-") or self.isexpected(token, "Operator", "*") or self.isexpected(token, "Operator", "/") or self.isexpected(token, "Operator", "%")

    def isRelOp(self, token):
        return self.isexpected(token, "Operator", "<") or self.isexpected(token, "Operator", ">") or self.isexpected(token, "Operator", "<=") or self.isexpected(token, "Operator", ">=")

    def isEqOp(self, token):
        return self.isexpected(token, "Operator", "==") or self.isexpected(token, "Operator", "!=")

    def isCondOp(self, token):
        return self.isexpected(token, "Operator", "&&") or self.isexpected(token, "Operator", "||")

    def isLiteral(self, token):
        return self.isIntLiteral(token) or self.isCharLiteral(token) or self.isBoolLiteral(token)
    
    """
    def syntaxId(self):
        pass
    """

    """
    def syntaxAlpha_num(self):
        pass
    """

    """
    def syntaxAlpha(self):
        pass
    """

    """
    def syntaxDigit(self):
        pass
    """

    """
    def syntaxHex_digit(self):
        pass
    """

    def isIntLiteral(self, token):
        return self.isDecimalLiteral(token) or self.isHexLiteral(token)

    def isDecimalLiteral(self, token):
        return self.getType(token) == "decimal"

    def isHexLiteral(self, token):
        return self.getType(token) == "hexadecimal"

    def isBoolLiteral(self, token):
        return (self.getType(token) == "keywords" and self.getValue(token) == "true") or (self.getType(token) == "keywords" and self.getValue(token) == "false")

    def isCharLiteral(self, token):
        return self.getType(token) == "char"

    def isStringLiteral(self, token):
        return self.getType(token) == "string"

    
g = Grammar()
#print(g.tokens)

g.syntaxProgram()
with open('../semantic check/token.txt', 'w') as nodos:
    for i in g.tree:
        nodos.write(str(i))
        nodos.write('\n')

