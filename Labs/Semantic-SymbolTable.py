class SymbolTable:
    def __init__(self):
        self.tree = {}
        self.identifiers = []

    def PushScope(self, scope):
        if type(scope) == int:    
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
        if symbol.op == "declaration":
            self.identifiers.append([scope, symbol.identifier])

    def Lookup(self, identifier): #return scope number
        for scope in self.tree:
            for symbol in self.tree[scope]:
                if symbol.identifier == identifier:
                    return scope
        return None    

    def showTree(self):        
        for i in self.tree:
            cadena = ""
            for j in self.tree[i]:
                cadena += str(j.toString()) + "\n"
                #print(cadena)
            print("Scope "+str(i)+":\n"+cadena+"")

    def validateDuplicity(self):     
        #print(self.identifiers)   
        for i in range(len(self.identifiers) - 1):
            for j in range(i+1, len(self.identifiers)):
                if self.identifiers[i] == self.identifiers[j]:
                    print("Duplicity found in idenfifier:", self.identifiers[j][1])

    def validateVariables(self, identifier, scope):
        #print(self.identifiers)
        for id in self.identifiers:
            if id[1] == identifier and id[0] == scope:
                return True
        return False                
        
            


class Symbol:
    def __init__(self, id, identifier, tipo, location, op):
        self.id = id        
        self.location = location
        self.op = op
        if op == "declaration":
            self.identifier = identifier
            self.tipo = tipo        
        else:
            self.identifier1 = identifier
            self.identifier2 = tipo

    def toString(self):
        if self.op == "declaration":
            return "ID:", self.id, "| Identifier:", self.identifier, "| Tipo:", self.tipo, "| Operation:", self.op, "| Location:", self.location
        else:
            return "ID:", self.id, "| Identifier:", self.identifier1, "| Value:", self.identifier2, "| Operation:", self.op, "| Location:", self.location
"""
nodo = Symbol(1, "a", "int", 1)
print(nodo.identifier)

tabla = {
    1: [nodo]
}

print(tabla[1][0].toString())

tabla.update({1:[15,20]})


for scope in tabla:
    for symbol in tabla[scope]:
        print(symbol)
"""
tree = SymbolTable()
cont = 1
line = 1
parse = open('parse.txt', 'r')

archivo = parse.readlines()
file = []
for item in archivo:
    file.append(item.strip())
scope = 0
undeclareds = ""
for x in file:
    if x == '{':
        scope += 1
        tree.PushScope(scope)
    elif x == '}':
        scope -= 1
    elif scope == 0:
        break
    else:        
        if len(x) > 0:
            s = x.replace(";", "")     
            #print("X:",x)   
            if "=" not in s:
                #print("No hay igual")
                array = s.split(" ")
                cont += 1
                nodo = Symbol(cont, array[1], array[0], line, "declaration")
                tree.InsertSymbol(nodo, scope)
            else:
                array = s.split("=")
                cont += 1            
                nodo = Symbol(cont, array[0], array[1], line, "assignation")
                if tree.validateVariables(array[1], scope):
                    tree.InsertSymbol(nodo, scope)
                else:
                    if not array[1].isdigit():
                        undeclareds += "Undeclared variable: "+ array[1]+ ", line:"+ str(line) +"\n"
    line += 1 
tree.showTree()

if scope != 0:
    print("Falta cerrar un scope\n")

tree.validateDuplicity()
print(undeclareds)