from ast import literal_eval
import sys
sys.path.insert(0, '../parser/')
from anytree import Node, RenderTree
import Parser

class SymbolTable:
    def __init__(self):
        self.tree = {}
        self.identifiers = []

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
                    return scope
        return None    

    def showTree(self):        
        for i in self.tree:
            cadena = ""
            for j in self.tree[i]:
                cadena += str(j.toString()) + "\n"
                #print(cadena)
            print("Scope "+str(i)+":\n"+cadena+"")

    def recurse(self, node):
        for child in node.children:
            print(child)
            self.recurse(child)

    def validateDuplicity(self):     
        #print(self.identifiers)   
        for i in range(len(self.identifiers) - 1):
            for j in range(i+1, len(self.identifiers)):
                if self.identifiers[i] == self.identifiers[j]:
                    raise Exception("Duplicity found in idenfifier:", self.identifiers[j][1])
        
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

        for pre, fill, node in RenderTree(Parser.g.final_tree):
            if node.name == "method_dec":
                for child in node.children:
                    print(child)
                    if child.name == "location":
                        for pre1, fill1, node1 in RenderTree(child):
                            print("%s%s" % (pre1, node1.name))
                    

    """
    def validateVariables(self, identifier, scope):
        #print(self.identifiers)
        for id in self.identifiers:
            if id[1] == identifier and id[0] == scope:
                return True
        return False             
    """
        
class DeclarationSymbol:
    def __init__(self, tipo, id, value, location, op):
        self.id = id        
        self.type = tipo
        self.value = value
        self.location = location
        self.op = op


    def toString(self):
        #if self.op == "declaration":
        #    return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location
        #elif self.op == "method":
        #    return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location
        return "ID:", self.id, "| Valor:", self.value, "| Tipo:", self.type, "| Operation:", self.op, "| Location:", self.location

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
        pass

    def typeCheck(self):
        pass        
        
    def validateVariable(self, token):
        if token[0] == "ID" and token[1] != "Program" and token[1] != "main" :
            #Validate undeclared variables
            if self.Lookup(token[1]) == None:
                raise Exception("SymbolError: Undeclared variable", token[1], "in line", token[2])


tree = SymbolTable()
rules = SemanticRules()

def validateVariable(token):
    if token[0] == "ID" and token[1] != "Program" and token[1] != "main" :
        #Validate undeclared variables
        if tree.Lookup(token[1]) == None:
            raise Exception("SymbolError: Undeclared variable '" + token[1] + "' in line " + str(token[2]))

def constructSymbolTable():
    scope = 0
    tokens = []
    starting_values = {'int':0, 'boolean': "false"}
    with open("token.txt", 'r') as f:
        for line in f:
            line = literal_eval(line)
            tokens.append(line)

    for i in range(len(tokens)):
        if tokens[i][1] == "{" or tokens[i][1] == "(":
            #print(tokens[i])
            scope += 1
            tree.PushScope(scope)
        elif tokens[i][1] == ")":
            scope -= 1
        elif tokens[i][1] == "int" or tokens[i][1] == "boolean":        
            if tokens[i+1][0] == "ID" and tokens[i-1][1] == "(":
                #print("parameter declaration:", tokens[i], scope)
                nodo = DeclarationSymbol(tokens[i][1], tokens[i+1][1], starting_values[tokens[i][1]], tokens[i][2], "parameter")
                tree.InsertSymbol(nodo, scope)
                while tokens[i+2][0] == "Delimiter" and tokens[i+2][1] == ",":
                    i += 3                
                    #print("parameter declaration:", tokens[i], scope)
                    nodo = DeclarationSymbol(tokens[i][1], tokens[i+1][1], starting_values[tokens[i][1]], tokens[i][2], "parameter")
                    #nodo = DeclarationSymbol(tokens[i][1], tokens[i+1][1], starting_values[tokens[i][1]], tokens[i][2], "parameter")
                    tree.InsertSymbol(nodo, scope)        
            elif tokens[i+1][0] == "ID" and tokens[i+2][1] == "(":
                #print("method declaration:", tokens[i], scope)
                nodo = DeclarationSymbol(tokens[i][1], tokens[i+1][1], starting_values[tokens[i][1]], tokens[i][2], "method")
                tree.InsertSymbol(nodo, scope)
            elif tokens[i+1][0] == "ID" and (tokens[i+2][1] == "," or tokens[i+2][1] == ";"):
                #print("var declaration:", tokens[i], scope)
                nodo = DeclarationSymbol(tokens[i][1], tokens[i+1][1], starting_values[tokens[i][1]], tokens[i][2], "declaration")
                tree.InsertSymbol(nodo, scope)
                tipo = tokens[i][1]
                i += 1
                while tokens[i+1][0] == "Delimiter" and tokens[i+1][1] == ",":                
                    i += 2
                    #print("var declaration:", tokens[i], scope)
                    nodo = DeclarationSymbol(tipo, tokens[i][1], starting_values[tipo], tokens[i][2], "declaration")
                    tree.InsertSymbol(nodo, scope)
        elif tokens[i][0] == "ID":
            validateVariable(tokens[i])
        #print("curtoken: ", tokens[i])
        elif tokens[i][0] == "Operator":
            pass
            destino = tokens[i-1][1]
            print(tokens[i], destino)


try:
    constructSymbolTable()
    tree.showTree()
    tree.validateDuplicity()    
    tree.validateTypes()
except Exception as e:
    print(e)
    sys.exit(0)

#print(RenderTree(Parser.g.final_tree))


#for pre, fill, node in RenderTree(Parser.g.final_tree):
    #print("%s%s" % (pre, node.name))
#    print(node.name)