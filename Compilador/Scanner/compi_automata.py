dfa = {0:{'+':1, '-':1},
       1:{'0':2, '1':2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9':2,},
       2:{'0':2, '1':2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9':2,}}
hex_dfa = {0:{'+':1, '-':1, '0':2},
		   1:{'0':2},
		   2:{'x':3},
		   3:{'A':4, 'a':4, 'b':4, 'B':4, 'C':4, 'c':4, 'D':4, 'e':4, 'E':4, 'F':4, 'f':4, '0':4, '1':4, '4':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4,},
		   4:{'A':4, 'a':4, 'b':4, 'B':4, 'C':4, 'c':4, 'D':4, 'e':4, 'E':4, 'F':4, 'f':4, '0':4, '1':4, '4':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4,}}

def acepta(transicion, inicial, acepta, s):
	estado = inicial
	if s[0] != '+' or s[0] != '-':
		estado += 1
	for c in s:
		estado = transicion[estado][c]
	return estado in acepta

try:
	test = '066AFA'
	if test[1] == 'x':
		print(acepta(hex_dfa, 0, {4}, test))
	else:
		print(acepta(dfa, 0, {2}, test))
except KeyError:
	print(False)

