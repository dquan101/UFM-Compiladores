class Nodes:
    def __init__(self, id, identifier, type, location):
        self.id = id
        self.identifier = identifier
        self.type = type
        self.location = location

tree = {}

parse = open('parse.txt', 'r')

archivo = parse.readlines()
file = []
for item in archivo:
    file.append(item.strip())
scope = 0
for x in file:
    if x == '{':
        scope += 1
    elif x == '}':
        scope -= 1
    elif scope == 0:
        break
    else:
        #tree[scope] = x
        x = x.replace(";", "")
        if len(x.split(" ")) > 1:
            print(x.split(" "))
            

#print(tree)


