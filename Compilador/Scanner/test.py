D = {'0': 1, '1': 1}
d = {0: 1, 1: 1}


d = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}

import string
alphabet = list(string.printable)
d = {}
for c in alphabet:
    d[c] = 2
string_dfa = {
	0:{'"':1, "'":1},
	1:d,
	2:{'"':2, "'":2}
}
for key in string_dfa:
	print(string_dfa[key])



alphabet = list(string.printable)
print(alphabet)

d = {}
for c in alphabet:
    d[c] = 1
e = {}
for c in alphabet:
    e[c] = 2

print(d)