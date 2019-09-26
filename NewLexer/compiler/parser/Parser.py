from ast import literal_eval
import sys
"""
bracketCheck = 0 
with open("parser/token.txt", 'r') as f:
    opens = ["(", "{", "["]
    for line in f:
        line = literal_eval(line)
        if line[0] == "Delimiter":
            if line[1] in opens:
                bracketCheck += 1
            else:
                bracketCheck -= 1
print(bracketCheck)
if bracketCheck == 0:
    print("Brackets balanceados")
else:
    print("Brackets no balanceados")
"""


class Grammar:
    def __init__(self):
        self.tokens = []
        with open("token.txt", 'r') as f:
            for line in f:
                line = literal_eval(line)
                self.tokens.append(line)
    
    def getType(self, token):
        return token[0]

    def getValue(self, token):
        return token[1]

    def popToken(self):
        self.tokens.pop(0)

    def printExpectedToken(self, expected):
        print("Expected Token: "+expected+", found ", self.tokens[0], "instead.")
        sys.exit()

    def isexpected(self, token, tipo, value):
        return self.getType(token) == tipo and self.getValue(token) == value

    def istype(self, token):
        return self.isexpected(token, "keywords", "int") or self.isexpected(token, "keywords", "boolean")

    def isID(self, token):
        return self.getType(token) == "ID"

    def syntaxProgram(self):         
        if self.isexpected(self.tokens[0], "keywords", "class"):
            self.popToken()
            if self.isexpected(self.tokens[0], "ID", "Program"):
                self.popToken()    
                if self.isexpected(self.tokens[0], "Delimiter", "{"):
                    self.popToken()  
                    if not self.isexpected(self.tokens[0], "Delimiter", "}"):  
                        while self.isexpected(self.tokens[2], "Delimiter", "["):
                            self.syntaxField_dec()
                        while self.isexpected(self.tokens[2], "Delimiter", "("):
                            self.syntaxMethod_dec()
                    if self.isexpected(self.tokens[0], "Delimiter", "}"):
                        self.popToken()
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
            self.popToken()      
            while True:
                if self.getType(self.tokens[0]) == "ID":
                    self.popToken()    
                    if self.isexpected(self.tokens[0], "Delimiter", "["):
                        self.popToken()    
                        if self.getType(self.tokens[0]) == "decimal" or self.getType(self.tokens[0]) == "hexadecimal":
                            self.popToken()    
                            if self.isexpected(self.tokens[0], "Delimiter", "]"):
                                self.popToken()    
                            else:
                                self.printExpectedToken("['Delimiter', ']']")
                        else:
                            self.printExpectedToken("<int_literal>")
                    elif self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.popToken()    
                        continue
                    elif self.isexpected(self.tokens[0], "Delimiter", ";"):
                        self.popToken()    
                        break
                    else:
                        self.printExpectedToken("['Delimiter', ';']")
                else:
                    self.printExpectedToken("['ID', '*']")
        else:
            self.printExpectedToken("<type>")


    def syntaxMethod_dec(self):        
        if self.istype(self.tokens[0]) or self.isexpected(self.tokens[0], "keywords", "void"):
            self.popToken()    
            if self.isID(self.tokens[0]):
                self.popToken()    
                if self.isexpected(self.tokens[0], "Delimiter", "("):
                    self.popToken()    
                    while True:
                        if self.istype(self.tokens[0]):
                            self.popToken()    
                            if self.isID(self.tokens[0]):
                                self.popToken()    
                                if self.isexpected(self.tokens[0], "Delimiter", ","):
                                    self.popToken()    
                                    continue
                                elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                                    self.popToken()    
                                    self.syntaxBlock()
                                else:
                                    self.printExpectedToken("['Delimiter', ')']")
                            else:
                                self.printExpectedToken("<ID>")
                        else:
                            self.printExpectedToken("<type>")
                else:
                    self.printExpectedToken("['Delimiter', '(']")
            else:
                self.printExpectedToken("<ID>")
        else:
            self.printExpectedToken("<method type>")
    
    def syntaxBlock(self):        
        if self.isexpected(self.tokens[0], "Delimiter", "{"):
            self.popToken()            
            self.syntaxVar_decl()
            self.syntaxStatement()
            if self.isexpected(self.tokens[0], "Delimiter", "}"):
                self.popToken()
            else:
                self.printExpectedToken("['Delimiter','}']")
        else:
            self.printExpectedToken("['Delimiter', '{']")

    def syntaxVar_decl(self):        
        while self.istype(self.tokens[0]):
            self.popToken()
            if self.isID(self.tokens[0]):
                self.popToken()
                if self.isexpected(self.tokens[0], "Delimiter", ","):
                    self.popToken()
                    self.syntaxVar_decl()
                elif self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken()
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
            if self.isexpected(self.tokens[1], "Delimiter", "(") or self.isexpected(self.tokens[0], "keywords", "callout"):
                #is method_call
                self.syntaxMethod_call()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isID(self.tokens[0]) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "[")):
                #is location
                self.syntaxLocation()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "if"):
                #is if
                self.popToken()
                if self.isexpected(self.tokens[0], "Delimiter", "("):
                    self.popToken()
                    self.syntaxExpr()
                    if self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken()
                        self.syntaxBlock()
                        if self.isexpected(self.tokens[0], "keywords", "else"):
                            self.popToken()
                            self.syntaxBlock()
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("['Delimiter','(']")
            elif self.isexpected(self.tokens[0], "keywords", "for"):
                #is for
                self.popToken()
                if self.isID(self.tokens[0]):
                    self.popToken()
                    if self.isexpected(self.tokens[0], "Operator", "="):
                        self.popToken()
                        self.syntaxExpr()
                        if self.isexpected(self.tokens[0], "Delimiter", ","):
                            self.popToken()
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
                self.popToken()
                self.syntaxExpr()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "break"):
                #is break
                self.popToken()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "continue"):
                #is continue
                self.popToken()
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "Delimiter", "{"):
                #is block
                self.syntaxBlock()
            else:
                self.printExpectedToken("<statement>")
        
    def syntaxMethod_call(self):        
        if self.isID(self.tokens[0]):
            self.popToken()
            if self.isexpected(self.tokens[0], "Delimiter", "("):
                self.popToken()
                self.syntaxExpr()
                while self.isexpected(self.tokens[0], "Delimiter", ","):
                    self.popToken()
                    self.syntaxExpr()
                if self.isexpected(self.tokens[0], "Delimiter", ")"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',')']")
            else:
                self.printExpectedToken("['Delimiter','(']")
        elif self.isexpected(self.tokens[0], "keywords", "callout"):
            self.popToken()
            if self.isexpected(self.tokens[0], "Delimiter", "("):
                self.popToken()
                if self.isStringLiteral(self.tokens[0]):
                    self.popToken()
                    if self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.syntaxCallout_arg()
                        while self.isexpected(self.tokens[0], "Delimiter", ","):
                            self.popToken()
                            self.syntaxCallout_arg()
                        if self.isexpected(self.tokens[0], "Delimiter", ")"):
                            self.popToken()
                        else:
                            self.printExpectedToken("['Delimiter',')']")
                    else:
                        self.printExpectedToken("['Delimiter',',']")
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
            self.popToken()
            if self.isexpected(self.tokens[0], "Delimiter", "["):
                self.popToken()
                self.syntaxExpr()
                if self.isexpected(self.tokens[0], "Delimiter", "]"):
                    self.popToken()
                else:
                    self.printExpectedToken("['Delimiter',']']")
        else:
            self.printExpectedToken("<ID>")

    def syntaxExpr(self):        
        if (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "(")) or self.isexpected(self.tokens[0], "keywords", "callout"):
            #is method_call            
            self.syntaxMethod_call()
        elif self.isID(self.tokens[0]) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "[")):
            #is location
            self.syntaxLocation()
        elif self.isLiteral(self.tokens[0]):
            self.popToken()
        elif self.isexpected(self.tokens[0], "Operator", "-"):
            #is negative
            self.popToken()
            self.syntaxExpr()
        elif self.isexpected(self.tokens[0], "Operator", "!"):
            #is differemt !
            self.popToken()
            self.syntaxExpr()
        elif self.isexpected(self.tokens[0], "Delimiter", "("):
            #is parenthesis expr
            self.popToken()
            self.syntaxExpr()
            if self.isexpected(self.tokens[0], "Delimiter", ")"):
                self.popToken()
            else:
                self.printExpectedToken("['Delimiter',')']")
        elif self.isBinOp(self.tokens[1]):
            #is expr alone
            self.syntaxExpr()
            if self.isBinOp(self.tokens[0]):
                self.popToken()
                self.syntaxExpr()
            else:
                self.printExpectedToken("<bin_op>")
        else:
            self.printExpectedToken("<expr>")
        

    def syntaxCallout_arg(self):        
        if self.isStringLiteral(self.tokens[0]):
            self.popToken()
        else:
            self.syntaxExpr()

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
        return self.getType(token) == "Decimal"

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
try:
    g.syntaxProgram()
except:
    print("Missing tokens")