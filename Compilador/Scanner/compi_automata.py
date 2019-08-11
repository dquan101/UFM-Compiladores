dfa = {0:{'+':0, '-':1},
       1:{'0':2, '1':2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9':2,},
       2:{'0':2, '1':2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9':2,}}

def acepta(transicion, inicial, acepta, s):
	estado = inicial
	if s[0] != '+' or s[0] != '-':
		estado += 1
	for c in s:
		estado = transicion[estado][c]
	return estado in acepta

try:
	print(acepta(dfa, 0, {2}, '10101'))
except KeyError:
	print(False)
