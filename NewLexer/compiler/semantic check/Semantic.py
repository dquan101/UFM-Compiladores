from ast import literal_eval

outF = open("parser/token.txt", "r")
outL = open("scanner/location.txt", "r")
locations = outL.readlines()
contents = outF.readlines()
location = []
new_contents = []
for i in locations:
    line = literal_eval(i)
    location.append(line)
for i in contents:
    line = literal_eval(i)
    new_contents.append(line)

scope = 0
for i in new_contents:
    if i[1] == '{':
        scope += 1
    if i[0] == 'ID' and i[1] != 'Program' and i[1] != 'main':
        i.append(scope)

for x in new_contents:
    for i in location:
        if x[0] == 'ID':    
            if x[1] in i[0]:
                x.append(i[1])
                print(x)