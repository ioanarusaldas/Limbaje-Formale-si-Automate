#Savu Ioana Rusalda 335CB
import sys

#reprezentare epsilon
EPSILON = ""

#functie de calculare a inchiderii epsilon pentru o stare data
def epsilonClosure(state):
	#state este starea pentru care se calculeaza inchiderea epsilon
	set_of_states = {state}
	#nextStates - set care retine starile rezultate dupa tranzitia epsilon
	nextStates = {state}
	all_states_visited = 1

	while (all_states_visited == 1):
		#parcurgere stari 
		for s in set_of_states:
			#parcurgere NFA
			for (st, w) in delta:
				#verific daca am gasit tranzitie epsilon pe starea curenta
				if (s == st and w == ''):
					nextStates = nextStates.union(delta[(st,w)])
		#marcare vizitare fiecare stare pentru gasirea tranzitiilor epsilon
		all_states_visited = 0;

		#verific daca s-a gasit stare noua
		for n in nextStates:
			if ((n,'') in delta) and (delta[(n,'')].issubset(set_of_states) == False):
				#nu s-au vizitat toate starile
				all_states_visited = 1;
		#actualizare set de stari
		set_of_states.update(nextStates)
	return set_of_states

#fuctie ce intoarce un set cu starile accesibile din starea curenta
#(determinarea starii din DFA)
def reachable_states(state,ch,epsClosures):
	states = set()
	new_set = set()
	#verificare existenta tranzitie pe characterul dat in NFA
	if (state,ch) in delta:
		#salvare stari in care se ajunge in urma tranzitiei 
		next_states = delta[(state,ch)]
		#parcurgere stari pentru a atasa starii din DFA inchiderile epsilon
		for s in next_states:
			new_set = new_set.union(epsClosures[s])
		states = states.union(new_set)

	return states

#functie care intoarce cheia din dictionar corespunzatoare unei valori date
def get_key(val,my_dict): 
	for key, value in my_dict.items(): 
		 if val == value: 
			 return key
#functie care determina starile finale din DFA
def final_states(states):
	aux = set()
	#parcurgere stari finale NFA
	for s in finalStates:
		aux = set()
		aux.update([s])
		#verificare stare DFA contine stare finala din NFA
		if(aux.issubset(states)):
			return True
	return False

#functie de constructie DFA
def subset_construction(out,epsClosures):
	initial_state = epsClosures[0]
	nr_states = 1;
	#lista de valori boolean care indica starile care au fost deja parcurse
	visited = []
	visited.append(False)
	finished = False
	#declarare dictionar in care se va realiza reprezentarea DFA
	DFA = {}
	#declarare dictionar care face maparea dintre starile din DFA si valori
									#de la 1 la nr_states
	DFA_states = {}
	DFA_states[0] = initial_state
	#contor ce retine starea curenta
	current_state = 0
	new_states = set()
	#set cu starile finale din DFA
	final = set()

	#verificare daca starea initiala este si finala
	if(final_states(initial_state) == True):
		final.update([0])

	while (finished == False):
		#extragere stari ce alcatuiesc starea curenta din DFA
		states = DFA_states[current_state]
		#parcurgere alfabet
		for ch in alphabet:
			#resetare new_set
			new_states = set()
			#parcurgere stari ce alcatuiesc starea din DFA
			for st in states:
				#calculare stari accesibile din starea curenta
				new_states = new_states.union(reachable_states(st,ch,epsClosures))
			#verificare daca exista deja starea calculata in DFA
			if (new_states in DFA_states.values()):
				key = get_key(new_states,DFA_states)
				#adaugare tranzitie catre starea deja existenta in DFA
				DFA[(current_state,ch)] = key
				#verificare stare daca este finala
				if(final_states(new_states) == True):
					final.update([key])
			else:
				#adaugare stare noua in DFA
				nr_states = nr_states + 1
				DFA_states[nr_states - 1] = new_states
				#marcare stare creata ca nevizitata
				visited.append(False)
				DFA[(current_state,ch)] = nr_states - 1
				#verificare stare daca este finala
				if(final_states(new_states) == True):
					final.update([nr_states - 1])
		#marcare stare curenta ca fiind vizitata
		visited[current_state] = True
		#actualizare stare curenta
		current_state = current_state + 1
		#verificare vizitare toate starile
		finished = all(f == True for (f) in visited)

	#scriere numar de stari in fisier
	out.write(str(len(DFA_states)))
	out.write("\n")

	#scriere tranzitii DFA in fisier
	for i in final:
		out.write(str(i) + " ")
	out.write("\n")
	
	return DFA

if __name__ == '__main__':
	#extragere nume fisiere
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	#deschidere fisier output
	out = open(output_file,"w")

	delta = {}
	alphabet = []
	#citire din fisier si generare alfabet si reprezentare NFA
	with open(input_file) as file:
		#citire numar de stari
		numberOfStates = int(file.readline().rstrip())
		#citire stari finale
		finalStates = set(map(int, file.readline().rstrip().split(" ")))
		#citire tranzitii
		while True:
			transition = file.readline().rstrip().split(" ")
			if transition == ['']:
				break
			if transition[1] == "eps":
				transition[1] = EPSILON
			elif (transition[1] not in alphabet):
				alphabet.append(transition[1])

			delta[(int(transition[0]), transition[1])] = set(map(int, transition[2:]))


	epsClosures = {}
	#calculare inchideri epsilon pentru fiecare stare din NFA
	for i in range (0,numberOfStates):
		epsClosures[i] = epsilonClosure(i)

	#reprezentare DFA
	DFA = subset_construction(out,epsClosures)
	#scriere in fisier de out
	for (state,ch) in DFA:
		out.write(str(state) + " " + ch + " " + str(DFA[(state,ch)]))
		out.write("\n")