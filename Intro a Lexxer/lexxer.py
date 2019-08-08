def valida1(cadena, num):
    f = open("config1.txt", "r")    
    if len(cadena) != len(f.read()):
        print("Los largos no concuerdan")
        return False
    else:
        return True

def valida2(cadena, num):
    pass
    f = open("config2.txt", "r")  
    if cadena == f.readline():
        return True
    else:
        return False

def valida3(cadena, num):
    pass
    validateGeneral(cadena, num)

def valida4(cadena, num):
    pass
    validateGeneral(cadena, num)
    
def valida5(cadena, num):
    pass
    validateGeneral(cadena, num)

def validateGeneral(cadena, num):
    pass
    archivo = "config"+str(num)+".txt"
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

switcher = {
    1: "valida1",
    2: "valida2",
    3: "validateGeneral",
    4: "validateGeneral",
    5: "validateGeneral"
}

op = int(input("Ingrese el numero del metodo a validar: "))
cadena = input("Ingrese una cadena al lexxer (frases separadas por espacios en blanco): ")
# Get the function from switcher dictionary

func = switcher.get(op)
if func == None:
    print("Opcion invalida")
else:
    print("Respuesta Final: ", globals()[func](cadena, op))
