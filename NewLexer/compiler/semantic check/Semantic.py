from ast import literal_eval

outF = open("parser/token.txt", "r")
contents = outF.readlines()
new_contents = []
for i in contents:
    line = literal_eval(i)
    new_contents.append(line)

scope = 0
for i in new_contents:
    if i[1] == '{':
        scope += 1
    if i[0] == 'ID' and i[1] != 'Program' and i[1] != 'main':
        i.append(scope)
        print(i)