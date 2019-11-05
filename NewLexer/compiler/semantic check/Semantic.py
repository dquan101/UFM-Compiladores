from ast import literal_eval
import sys
sys.path.insert(0, '../parser/')
from anytree import Node, RenderTree, PostOrderIter, PreOrderIter
import anytree
import Parser

class SymbolTable:
    def __init__(self):
        self.tree = {}
        self.identifiers = []
        self.tokens = []
        self.starting_values = {'int':0, 'boolean': "false"}
        self.final_tree = Parser.g.final_tree
        with open("token.txt", 'r') as f:
            for line in f:
                line = literal_eval(line)
                self.tokens.append(line)

    def constructSymbolTable(self):
        scope = 0
        for i in range(len(self.tokens)):
            if self.tokens[i][1] == "{" or self.tokens[i][1] == "(":
                #print(self.tokens[i])
                scope += 1
                tree.PushScope(scope)
            elif self.tokens[i][1] == ")":
                scope -= 1
            elif self.tokens[i][1] == "int" or self.tokens[i][1] == "boolean": 
                #self.validateDuplicity(self.tokens[i+1])       
                if self.tokens[i+1][0] == "ID" and self.tokens[i-1][1] == "(":
                    #print("parameter declaration:", self.tokens[i], scope)
                    nodo = DeclarationSymbol(self.tokens[i][1], self.tokens[i+1][1], self.starting_values[self.tokens[i][1]], self.tokens[i][2], "parameter", False)
                    self.validateDuplicity(self.tokens[i+1])   
                    tree.InsertSymbol(nodo, scope)
                    while self.tokens[i+2][0] == "Delimiter" and self.tokens[i+2][1] == ",":
                        i += 3                
                        #print("parameter declaration:", self.tokens[i], scope)
                        nodo = DeclarationSymbol(self.tokens[i][1], self.tokens[i+1][1], self.starting_values[self.tokens[i][1]], self.tokens[i][2], "parameter", False)
                        #nodo = DeclarationSymbol(self.tokens[i][1], self.tokens[i+1][1], starting_values[self.tokens[i][1]], self.tokens[i][2], "parameter")
                        self.validateDuplicity(self.tokens[i+1])   
                        tree.InsertSymbol(nodo, scope)        
                elif self.tokens[i+1][0] == "ID" and self.tokens[i+2][1] == "(":
                    #print("method declaration:", self.tokens[i], scope)
                    nodo = DeclarationSymbol(self.tokens[i][1], self.tokens[i+1][1], self.starting_values[self.tokens[i][1]], self.tokens[i][2], "method", False)
                    self.validateDuplicity(self.tokens[i+1])   
                    tree.InsertSymbol(nodo, scope)
                elif self.tokens[i+1][0] == "ID" and (self.tokens[i+2][1] == "," or self.tokens[i+2][1] == ";" or self.tokens[i+2][1] == "["):
                    #print("var declaration:", self.tokens[i], scope)
                    diferencia = 0 #diferencia de tokens entre una declaracion de un array y de una variable global
                    if self.tokens[i+2][1] == "[":
                        nodo = DeclarationSymbol(self.tokens[i][1], self.tokens[i+1][1], self.starting_values[self.tokens[i][1]], self.tokens[i][2], "declaration", True, self.tokens[i+3][1])   
                        diferencia = 3
                    else:
                        nodo = DeclarationSymbol(self.tokens[i][1], self.tokens[i+1][1], self.starting_values[self.tokens[i][1]], self.tokens[i][2], "declaration", False)
                        diferencia = 0
                    self.validateDuplicity(self.tokens[i+1])   
                    tree.InsertSymbol(nodo, scope)
                    tipo = self.tokens[i][1]
                    i += 1 #Esto setea el contador sobre el token que tiene el ID
                    while self.tokens[i+1+diferencia][0] == "Delimiter" and self.tokens[i+1][1] == ",":                
                        i += (2 + diferencia) #Setea el contador a la altura del ID despues de una coma en una declaracion multiple.
                        #print("var declaration:", self.tokens[i], scope)
                        if self.tokens[i+2][1] == "[":
                            nodo = DeclarationSymbol(tipo, self.tokens[i][1], self.starting_values[tipo], self.tokens[i][2], "declaration", True, self.tokens[i+2][1])   
                            diferencia = 3
                        else:
                            nodo = DeclarationSymbol(tipo, self.tokens[i][1], self.starting_values[tipo], self.tokens[i][2], "declaration", False)
                            diferencia = 0
                        #nodo = DeclarationSymbol(tipo, self.tokens[i][1], self.starting_values[tipo], self.tokens[i][2], "declaration", False)
                        self.validateDuplicity(self.tokens[i])   
                        tree.InsertSymbol(nodo, scope)
                
            elif self.tokens[i][0] == "ID":                
                self.validateVariable(self.tokens[i])

            #print("curtoken: ", self.tokens[i])

            """
            elif self.tokens[i][0] == "Operator":
                pass
                destino = self.tokens[i-1][1]
                print(self.tokens[i], destino)
            """

    def PushScope(self, scope):
        if type(scope) == int:    
            if scope > len(self.tree):
                self.tree.update({scope:[]})
        else:
            raise Exception("Scope must be Integer")

    def PopScope(self, scope):
        if type(scope) == int: 
            self.tree.pop(scope, None)
        else:
            raise Exception("Scope must be Integer")

    def InsertSymbol(self, symbol, scope):
        temp = self.tree[scope]
        temp.append(symbol)
        self.tree.update({scope:temp})
        
        if symbol.op:
        #if symbol.op == "declaration":
            self.identifiers.append([scope, symbol.id])

    def Lookup(self, identifier): #return scope number
        for scope in self.tree:
            for symbol in self.tree[scope]:
                if symbol.id == identifier:                    
                    return [scope, symbol.value]
        return None    

    def LookupType(self, identifier):
        for scope in self.tree:
            for symbol in self.tree[scope]:
                if symbol.id == identifier:                    
                    return symbol.type
        return None    

    def setValue(self, identifier, newvalue):
        for scope in self.tree:
            for symbol in self.tree[scope]:
                if symbol.id == identifier:                    
                    symbol.value = newvalue
        

    def showTree(self):        
        for i in self.tree:
            cadena = ""
            for j in self.tree[i]:
                cadena += str(j.toString()) + "\n"
                #print(cadena)
            print("Scope "+str(i)+":\n"+cadena+"")

    def getExprValue(self, exprNode, expectedType = None):
        operation = ""
        operators = ['+','-','*','%',"(",")"]
        for node in PostOrderIter(exprNode):
            #print(type(node.name) == list)
            if type(node.name) == list:                                
                if node.name[0] == "ID":
                    if self.LookupType(node.name[1]) != expectedType:
                        raise Exception("Invalid type found for", expectedType, "operation")
                    if node.parent.name == "method_call":
                        #Implementar metodo para recuperar el valor de una method call
                        pass
                    else:
                        operation += str(self.Lookup(node.name[1])[1])
                    #operation += super(SemanticRules, self).Lookup(node.name[1])[1]
                else:
                    #print(node.name)
                    if expectedType == "int":
                        if node.name[1].isnumeric() or node.name[1] in operators:
                            operation += node.name[1]
                        else:
                            raise Exception("Invalid type found for <", expectedType, "> operation")
                    elif expectedType == "boolean":
                        if not node.name[1].isnumeric():
                            operation += node.name[1]
                        else:
                            raise Exception("Invalid type found for <", expectedType, "> operation")
                
                            

            #Falta validar los method call
                
        print(operation)

        print("\n End of Expr \n")

        """
        valor = 0
        for child in exprNode.children:
            if type(child.name) != "list":
                return 
            else:
                self.getExprValue(child)
        """            

    #Called during ConstructSymbolTable
    def validateDuplicity(self, token):     
        #print(self.identifiers) 
        """  
        for i in range(len(self.identifiers) - 1):
            for j in range(i+1, len(self.identifiers)):
                if self.identifiers[i] == self.identifiers[j]:
                    raise Exception("Duplicity found in idenfifier:", self.identifiers[j][1])
        """
        if self.Lookup(token[1]) != None:
            raise Exception("Duplicity found in idenfifier:", token[1], "in line", token[2])

    #Called during ConstructSymbolTable
    def validateVariable(self, token):
        if token[0] == "ID" and token[1] != "Program" and token[1] != "main" :
            #Validate undeclared variables
            if self.Lookup(token[1]) == None:
                raise Exception("SymbolError: Undeclared variable", token[1], "in line", token[2])

    def validateTypes(self):
        """
        for scope in self.tree:
            for symbol in self.tree[scope]:
                if symbol.type == "int":
                    if not str(symbol.value).isnumeric():
                        raise Exception ("ValueError: Variable '"+symbol.id+"' in line "+str(symbol.location))
                elif symbol.type == "boolean":
                    if not symbol.value == "true" or not symbol.value == "false":
                        raise Exception ("ValueError: Variable '"+symbol.id+"' in line "+str(symbol.location))
        """
        pass
        
        for pre, fill, node in RenderTree(Parser.g.final_tree):
            if node.name == "statement":    
                for child in node.children:
                    if child.name == "expr":
                        if anytree.util.leftsibling(child).name[0] == "Operator":
                            op = anytree.util.leftsibling(child)
                            destino = anytree.util.leftsibling(op).children[0]
                            print(destino)
                            if op.name[1] == "=":
                                print(destino, "Expr value:", self.getExprValue(child, self.LookupType(destino.name[1])))
                                #self.setValue(destino.name[1], self.getExprValue(child, self.LookupType(destino.name[1])))
                            elif op.name[1] == "+=":
                                pass
                            elif op.name[1] == "-=":
                                pass
            elif node.name == "method_dec":
                for hijo in node.children:
                    if hijo.name[1] == "main":
                        if len(node.children) != 5:
                            raise Exception('ParameterError: Main takes no arguments!')
            
            elif node.name[1] == 'continue' or node.name[1] == 'break':
                viejos = []
                for i in node.ancestors:
                    if i.name == 'statement':
                        for j in i.children:
                            viejos.append(j.name[1])
                if 'for' not in viejos:
                    raise SyntaxError('SyntaxError: BREAK or CONTINUE not in FOR statement')
          
        
                    

    """
    def validateVariables(self, identifier, scope):
        #print(self.identifiers)
        for id in self.identifiers:
            if id[1] == identifier and id[0] == scope:
                return True
        return False             
    """
        
class DeclarationSymbol:
    def __init__(self, tipo, id, value, location, op, isarray, arraysize = None):
        self.id = id        
        self.type = tipo
        self.value = value
        self.location = location
        self.op = op
        self.isarray = isarray
        self.arraysize = arraysize
        if arraysize != None and isarray == False:
            raise Exception("There can only be array size when declaring an array.")
            


    def toString(self):
        #if self.op == "declaration":
        #    return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location
        #elif self.op == "method":
        #    return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location
        return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location, "| isArray:", self.isarray, "| ArraySize:", self.arraysize

"""
class Symbol:
    def __init__(self, tipo, id, value, location, op):
        self.id = id        
        self.type = tipo
        self.value = value
        self.location = location
        self.op = op


    def toString(self):
        if self.op == "declaration":
            return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location
        else:
            return "ID:", self.id, "| Identifier:", self.identifier1, "| Value:", self.identifier2, "| Operation:", self.op, "| Location:", self.location
"""
class SemanticRules(SymbolTable):
    def __init__(self):    
        #SymbolTable.__init__(self)
        pass

    def typeCheck(self):
        pass        

    

    
        
        
    


tree = SymbolTable()
rules = SemanticRules()

"""
def validateVariable(token):
    if token[0] == "ID" and token[1] != "Program" and token[1] != "main" :
        #Validate undeclared variables
        if tree.Lookup(token[1]) == None:
            raise Exception("SymbolError: Undeclared variable '" + token[1] + "' in line " + str(token[2]))
"""

#print(RenderTree(Parser.g.final_tree))
print(RenderTree(tree.final_tree))

try:
    tree.constructSymbolTable()
    tree.showTree()
    #tree.validateDuplicity()    
    #tree.validateTypes()
except Exception as e:
    print(e)
    sys.exit(0)




#for pre, fill, node in RenderTree(Parser.g.final_tree):
    #print("%s%s" % (pre, node.name))
#    print(node.name)

