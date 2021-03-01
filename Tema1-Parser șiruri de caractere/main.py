#Savu Ioana Rusalda 335CB
import sys
import string

#genereaza matricea delta cu 0
def generate_delta(patterns):
	delta = []
	#generare lista de litere din alfabet (A-Z)
	alphabet = list(string.ascii_uppercase)
	alphabet.insert(0,'')

	#generare linie specifica cuvantului vid
	empty_word = ['e']
	for i in range(len(alphabet) - 1):
		empty_word.append(0)

	#adaugare primele 2 linii in matrice
	delta.append(alphabet)
	delta.append(empty_word)	

	substring = ""
	#parcurgere caractere din string
	for ch in string1:
		#alcatuire substring
		substring = substring + ch
		#adaugare substring in lista de patterns si in lista provizorie
		state = [substring]
		patterns.append(substring)

		for i in range(0 ,(len(alphabet) - 1)):
			state.append(0)#adaugare 0
		#adaugare line noua in matricea delta
		delta.append(state)
	return delta

#functie ajutatoare de afisare a matricii delta
def print_delta(delta,out_file):
	for line in delta:
		out_file.write(str(line) + "\n")

#functia care intoarce indexul coloanei din matrice corespunzator literei
def letter_index(letter):
	return ord(letter) - 64

#functie de maxim
def max(a, b):
	if (a > b):
		return a
	return b

#functie cautare sufix maxim 
def find_sufix(possible_pattern,delta,patterns,i,j):
	#cautare pana la ultima litera din pattern
	while (len(possible_pattern) > 0):
		#verificare daca o stare apartine matricei
		if (possible_pattern in patterns):
			delta[i][j] = max(delta[i][j] ,len(possible_pattern))
			break;
		#eliminare prima litera din pattern
		possible_pattern = possible_pattern[1:]

def complete_delta(patterns,delta):
	#extragere prima litera din pattern(starea1)
	first_state = delta[2][0]

	#completare stare corespunzatoare cuvantului vid
	index = letter_index(first_state)
	delta[1][index] = 1;

	#parcurgere matrice delta
	for i in range(2,len(delta)):
		#extragere stare de referinta
		state_pattern  =  delta[i][0];
		#parcurgere litere din alfabet
		for j in range(1,len(delta[0])):
			#generare pattern posibil
			possible_pattern = state_pattern + delta[0][j]
			#cautare cel mai lung prefix care se potriveste
			find_sufix(possible_pattern,delta,patterns,i,j)
	return delta


if __name__ == "__main__":
	#deschidere fisiere
	in_file = open(sys.argv[1],"r")
	out_file = open(sys.argv[2],"w")

	#citire din fisier
	line1 = in_file.readline()
	line2 = in_file.readline()
	#eliminare /n
	string1 = line1[:(len(line1) - 1)]
	string2 = line2[:(len(line2) - 1)]

	#creare lista patterns + generare delta
	patterns = []
	delta = generate_delta(patterns)

	#completare matrice delta
	delta = complete_delta(patterns,delta)

	#extragere stare finala
	final_state = len(string1)

	#initializare indici stari
	current_state = 0 
	i = -1

	#parcurgere text
	for ch in string2:
		i = i + 1
		index = letter_index(ch)
		#extragere stare curenta
		current_state = delta[current_state + 1][index]
		#verificare daca starea curenta este finala
		if (current_state == final_state):
			#calculare index + scriere in fisier
			j = i - (len(string1) - 1)
			out_file.write(str(j) + " ")

	out_file.write("\n")
	#inchidere fisiere
	in_file.close()
	out_file.close()