HFA = {0:{'-':5, '0':1, '1':3, '2':3, '3':3, '4':3, '5':3, '6':3, '7':3, '8':3, '9':3},
		1:{'x':2},
		2:{'a':2, 'b':2, 'c':2, 'd':2, 'e':2, 'f':2, 'A':2, 'B':2, 'C':2, 'D':2, 'E':2, 'F':2, '0':2, '1':2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9':2},
		3:{'.':4, '0':3, '1':3, '2':3, '3':3, '4':3, '5':3, '6':3, '7':3, '8':3, '9':3},
		4:{'0':4, '1':4, '2':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4},
		5:{'0':6, '1':8, '2':8, '3':8, '4':8, '5':8, '6':8, '7':8, '8':8, '9':8},
		6:{'x':7},
		7:{'a':7, 'b':7, 'c':7, 'd':7, 'e':7, 'f':7, 'A':7, 'B':7, 'C':7, 'D':7, 'E':7, 'F':7, '0':7, '1':7, '2':7, '3':7, '4':7, '5':7, '6':7, '7':7, '8':7, '9':7},
		8:{'.':9, '0':8, '1':8, '2':8, '3':8, '4':8, '5':8, '6':8, '7':8, '8':8, '9':8},
		9:{'0':9, '1':9, '2':9, '3':9, '4':9, '5':9, '6':9, '7':9, '8':9, '9':9}}

def type(listt, types):
	matrix = []
	for x in listt:
		lists = [None, None]
		if x in types['reservadas']:
			lists[0] = 'reservadas'
			lists[1] = x
			matrix.append(lists)
		else:
			try:
				if accepts(HFA, 0, {2, 3, 4, 7, 8, 9}, x) in (2, 7):
					lists[0] = 'hexadecimal'
					lists[1] = x
					matrix.append(lists)
				if accepts(HFA, 0, {2, 3, 4, 7, 8, 9}, x) in (3, 4, 8, 9):
					lists[0] = 'decimal'
					lists[1] = x
					matrix.append(lists)
			except:
				pass
	return matrix 
	

def tokenize(file):
	with open(file, 'r') as f:
		newlist = []
		for line in f:
			str = line.split()
			newlist.extend(str)
	return newlist

def accepts(transitions,initial,accepting,s):
    state = initial
    for c in s:
        state = transitions[state][c]
    return state


keys = {'reservadas':['boolean', 'for', 'integer', 'in']}
newlist = tokenize('lexerr.txt')
print(newlist)
print(type(newlist, keys))