from ast import literal_eval
import sys

tokens = []
with open("semantic check/token.txt", 'r') as f:
    for line in f:
        line = literal_eval(line)
        tokens.append(line)

changes = 0
tree = {}
father = "program"
for token in tokens:
    cur_father = token[3]
    if cur_father == father:
        tree[cur_father+str(changes)] = token[1]
    else:
        changes += 1


def makeTree(newfather):
    pass
    if father == newfather:
        

print(tree) 
father = cur_father
input("Press Enter to continue...")


c = {"a":"funciono perro"}
arbol = {"a": "aaa", "b":"bbb", "c":c}

print(arbol)