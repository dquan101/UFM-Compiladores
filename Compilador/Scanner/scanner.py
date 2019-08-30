def validateGeneral(cadena):
    pass
    archivo = "Compilador\Scanner\onlyint.txt"
    f = open(archivo, "r")  
    #Rs = f.readline().split("*")
    #print(Rs)
    separadores = ['*','(',')']
    Rs = []
    R = ""
    RegExp = f.readline()
    #print(RegExp)
    
    #----- Separate keywords of regular expression -------
    for i in range(len(RegExp)):       
        char =  RegExp[i]
        #print(char)
        if char in separadores:
            if char == '*':    
                if R != "":            
                    Rs.append([R, '*'])
                    R = ""
            elif char == '(':
                
                R += char
                if len(R) > 1:
                    Rs.append([R, '+']) # '+' means 1 or more 
                    R = ""
                else:
                    pass
            elif char == ')':
                R += char
                
                if i == len(RegExp)-1:
                    Rs.append([R, '+'])
                    R = "" 

                elif RegExp[i+1] == '*':
                    Rs.append([R, '*'])
                    R = ""                    
                else:
                    Rs.append([R, '+']) # '+' means 1 or more 
                    R = ""
        else:
            R += char
            if i == len(RegExp)-1:
                Rs.append([R, '+']) # '+' means 1 or more 
    #---------------------------------------------------------------

    #------ Check for dual options --------------    
    for i in range(len(Rs)):
        multi = []
        R = ""
        if Rs[i][0][0] == "(":
            """
            j = 1
            while Rs[i][0][j] != ")":
                print(Rs[i][0][j])
                if Rs[i][0][j] != "|":
                    R += Rs[i][0][j]
                else:
                    multi.append([R, Rs[i][1]])
                    R = ""
                j += 1
                print(multi)
            
            Rs[i] = multi
            """
            for j in range(1,len(Rs[i][0])):                
                if Rs[i][0][j] != "|" and Rs[i][0][j] != ")":
                    #print(Rs[i][0][j])
                    R += Rs[i][0][j]
                elif Rs[i][0][j] == ')':
                    #print("Entro")
                    new = [R, Rs[i][1]]
                    multi.append(new)
                    R = ""
                else:
                    multi.append([R, Rs[i][1]])
                    R = ""
            Rs[i] = multi
    #---------------------------------------------------------------
    print(Rs)
    pos = 0
    match = True
    """
    for phrase in Rs:
        #print(type(phrase[0]) == list)
        if type(phrase[0]) != list:
            test = cadena[pos:len(phrase[0])]
            print(test)
            if phrase[1] == "*":
                timesfound = 0
                while test == phrase[0]:
                    timesfound += 1
                    pos += len(phrase[0])
                    test = cadena[pos:len(phrase[0])]
                    print(timesfound)
                if timesfound >= 0:
                    print("Match sera true")
                    match = True
            elif phrase[1] == "+":
                pass
    """       
    #tokens = cadena.split(" ")         
    for i in range(len(Rs)):
        phrase = Rs[i]
        #print(phrase)
        print("Frase: ", phrase)
        if type(phrase[0]) != list:
            test = cadena[pos:pos+len(Rs[i][0])]
            existe = False
            print("test:", test)
            if phrase[1] == "*":
                timesfound = 0
                while test == phrase[0]:
                    existe = True
                    #print("pos: ", pos)
                    #print("test: ", test)
                    timesfound += 1
                    pos += len(phrase[0])
                    test = cadena[pos:pos+len(phrase[0])]
                print("times: ", timesfound)
                
                if len(test) == 0:
                    match = True
                elif existe == True:
                    #print("Match sera true")
                    match = True
                else:
                    match = False

            elif phrase[1] == "+":
                timesfound = 0
                while test == phrase[0]:
                    timesfound += 1
                    pos += len(phrase[0])
                    test = cadena[pos:pos+len(phrase[0])]
                print("times: ", timesfound)
                if timesfound == 0:
                    print("Salvacion: ", cadena[pos-len(phrase[0]):pos])
                    if cadena[pos-len(phrase[0]):pos] == phrase[0]:
                        match = True
                    else:
                        match = False
                elif timesfound == 1:
                    #print("Match sera true")
                    match = True
               
                    
                    
            print("match: ",match)
        else:
            pass
            options = []
            method = phrase[0][1]
            for element in phrase:
                options.append(element[0])
            print("options:", options)

            test = cadena[pos:pos+len(options[0])]
            existe = False
            print("test:", test)
            if method == "*":
                timesfound = 0
                while test in options:
                    existe = True
                    #print("pos: ", pos)
                    #print("test: ", test)
                    timesfound += 1
                    pos += len(phrase[0])
                    test = cadena[pos:pos+len(options[0])]
                print("times: ", timesfound)
                
                if len(test) == 0:
                    match = True
                elif existe == True:
                    #print("Match sera true")
                    match = True
                else:
                    match = False

            elif method == "+":
                timesfound = 0
                while test in options:
                    timesfound += 1
                    pos += len(phrase[0])
                    test = cadena[pos:pos+len(options[0])]
                print("times: ", timesfound)
                if timesfound == 0:
                    print("Salvacion: ", cadena[pos-len(phrase[0]):pos])
                    if cadena[pos-len(options[0]):pos] in options:
                        match = True
                    else:
                        match = False
                elif timesfound == 1:
                    #print("Match sera true")
                    match = True
               
                    
            print("match: ",match)            
        print("last pos: ", pos)

    return match

def separate(RegExp):
    separadores = ['(',')','[',']'] #Separadores de tokens
    signos = ['*','+','?']  #Signos que dicen la cantidad
    Rs = [] #Arreglo que contiene las expresiones separadas
    R = "" #String que tiene el texto de cada expresion

    for i in range(len(RegExp)):
        char = RegExp[i]
        #print("char: ",char) 
        if char in separadores:                       
            if char == '(':
                while char != ')':
                    char = RegExp[i]
                    i += 1
                    R += char                    
                print("Content of ():", R) 
                
                char = RegExp[i]
                #print("Char sign: ", char)
                if char in signos:
                    Rs.append([R,char])
            
                
            if char == '[':
                while char != ']':
                    char = RegExp[i]
                    i += 1
                    R += char                    
                print("Content of []:", R)   
                
                char = RegExp[i]
                #print("Char sign: ", char)
                if char in signos:
                    Rs.append([R,char])
            R = ""

    #print("Rs contains: ",Rs)
    return Rs

def generate(Rs):
    dfa = {}
    operaciones = ['|',':'] #Separadores de expresiones
    R = ""
    conte = 0 #Revisa si ya existe un elemento para partir
    ops = []
    
    print("RS: ", Rs)
    for i in range(len(Rs)):        
        Rs[i][0] = Rs[i][0][1:len(Rs[i][0])-1] #Eliminando los caracteres sepadores del inicio y el final
        #print(Rs[i])

        if not any(op in Rs[i][0] for op in operaciones):
            print(i, Rs[i][0])
        else:
            for op in operaciones:
                #print("OP:", op)
                if op in Rs[i][0]:
                    ops = Rs[i][0].split(op)
            if ops:
                print(i, ops)
                d = {}
                for op in ops:                    
                    try:        
                        int(op)                
                        if 48 <= ord(op) <= 57: #Es int
                            for j in range(ord(ops[0]), ord(ops[1])+1):
                                d[j-48] = i
                            continue
                    except ValueError:
                        d[op] = i+1
            
                #d = { x:x+1 for x in d}
                
                print(i, "D:",d)
                dfa[i] = d
        if i == len(Rs)-1:
            d = dict.fromkeys(d, d[1]+1)
            dfa[i] = d
    return dfa
                

                

import os
 
dirpath = os.getcwd()
print("current directory is : " + dirpath)

f = open("onlyint.txt", "r") 
RegExp = f.readline()

print(RegExp)
print(generate(separate(RegExp)))
