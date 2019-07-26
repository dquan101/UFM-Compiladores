def valida1(cadena):
    f = open("config1.txt", "r")    
    if len(cadena) != len(f.read()):
        print("Los largos no concuerdan")
        return False
    else:
        return True

def valida2(cadena):
    pass
    R = "c"
    
    

def valida3(cadena):
    pass
    
def valida4(cadena):
    pass
    
def valida5(cadena):
    pass
    
switcher = {
    1: "valida1",
    2: "valida2",
    3: "valida3",
    4: "valida4",
    5: "valida5"
}

op = int(input("Ingrese el numero del metodo a validar: "))
cadena = input("Ingrese una cadena al lexxer")
# Get the function from switcher dictionary

func = switcher.get(op)
if func == None:
    print("Opcion invalida")
else:
    print(globals()[func](cadena))