#Savu Ioana Rusalda 335CB
import sys
EPSILON = ""

#***************************TRANSFORMARE ER - NFA******************************
class Expr: #interfata EXPR
	#constructor clase
	def __init__(self):
		pass
	#metoda folosita pentru debug 
	def __str__(self):
		pass

#clasa pentru definirea opeatiei de concatenare
class Concat(Expr):
	def __init__(self, e1, e2):
		self.e1 = e1
		self.e2 = e2
	def __str__(self):
		return self.e1.__str__() +""+ self.e2.__str__()

#clasa pentru definirea opeatiei de reuniune
class Union(Expr):
	def __init__(self, e1, e2):
		self.e1 = e1
		self.e2 = e2
	def __str__(self):
		return self.e1.__str__() +"|"+ self.e2.__str__()

#clasa pentru definirea opeatiei de star
class Star(Expr):
	def __init__(self, e):
		self.e = e
	def __str__(self):
		return "" + self.e.__str__() + "*"
#clasa pentru definirea unui caracter		
class Character(Expr):
	def __init__(self, c):
		self.c = c
	def __str__(self):
		return str(self.c)
#clasa pentru definirea unei paranteze
class Parant(Expr):
	def __init__(self, p):
		self.p = p
	def __str__(self):
		return "("+ self.p.__str__() + ")"

#clasa care detine arborele de parsare
class Parser:
	def __init__(self):
		self.stack = []

	def push(self, el):
		self.stack.append(el)

	def peek(self, pos):
		return self.stack[pos]

	def pop(self):
		e = self.stack [len(self.stack) - 1]
		self.stack = self.stack[:-1]
		return e

	# functiile de reducere care construiesc Nfa din arborele de parsare

	def reduceConcat(self):
		e1 = self.pop() #se coate expresia 1 de pe stiva
		e2 = self.pop() #se coate expresia 2 de pe stiva
		self.push(Concat(e2,e1)) #se pune concatenarea celor 2 expresii pe stiva

	def reduceUnion(self):
		e1 = self.pop()#se coate expresia 1 de pe stiva
		self.pop()#se coate | de pe stiva
		e2 = self.pop()#se coate expresia 2 de pe stiva
		self.push(Union(e2,e1))#se pune reuniunea celor 2 expresii pe stiva

	def reduceStar(self):
		e = self.pop() #se scaote expresia de pe stiva
		self.push(Star(e)) #se pune obiectul de tip Star pe stiva

	def reduceCharacter(self):
		c = self.pop() #se scoate caracterul de pe stiva
		self.push(Character(c)) #se pune obiectul de tip caracter pe stiva

	def reduceParant(self):
		e = self.pop() #se scoate expresia de pe stiva
		self.pop() #se scoate ( de pe stiva
		self.push(Parant(e))#se pune obiectul de tip paranteza pe stiva

#clasa ce contine NFA-ul format		
class NFA:
	def __init__(self):
		self.final_states = [] #retine starile finale din NFA
		self.nrStates = 0 #retine numarul de stari din NFA
		self.NFA = [] #retine tranzitii
		
class ConvertToNFA:
	def __init__(self):
		pass
	#creeaza NFA pentru un caracter
	def convertCharacter(self,expr):
		character_nfa = NFA() 
		character_nfa.final_states = 1
		character_nfa.nrStates = 2
		#tranzitia corespunzatoare NFA-ului pentru un caracter
		transition = (0,expr.c,1) 
		character_nfa.NFA.append(transition)
		return character_nfa

	#creeaza NFA pentru un Concatenarea a doua expresii
	def convertConcat(self,expr):
		#apel recursiv pentru transformarea expresiilor din concatenare
		nfa1 = self.convertType(expr.e1) 
		nfa2 = self.convertType(expr.e2)

		(s1,c,s2) = nfa1.NFA[len(nfa1.NFA) - 1]
		#determinare numar stari din NFA 1
		nr = nfa1.nrStates  - 1

		#modificare tranzitii din NFA 2
		for (st1,ch,st2) in nfa2.NFA:
			transition = (st1 + nr,ch,st2 + nr)
			nfa1.NFA.append(transition)

		#determinare stare finala + numar de stari
		(st1,ch,st2) = nfa1.NFA[len(nfa1.NFA) - 1]
		nfa1.nrStates = st2 + 1
		nfa1.final_states = [st2]
		return nfa1

	#creeaza NFA pentru un Reuniunea a doua expresii
	def convertReunion(self,expr):
		#apel recursiv pentru transformarea expresiilor din reuniune
		nfa1 = self.convertType(expr.e1)
		nfa2 = self.convertType(expr.e2)
		
		#modificare stari NFA1
		#numarul pentru fiecare stare creste cu 1 pentru ca starea initiala
			#adaugata sa fie 0
		l = []
		for (st1,ch,st2) in nfa1.NFA:
			l.append((st1+1,ch,st2 +1))
		nfa1.NFA = l

		#memorare stare finala NFA 1 pentru a putea modifica starile in NFA 2
		(s1,c,s2) = nfa1.NFA[len(nfa1.NFA) - 1]
		nfa1.final_states = [s2]
		l = []

		#modificare stari in NFA2
		nr = nfa1.nrStates + 1
		for (st1,ch,st2) in nfa2.NFA:
			transition = (st1 +nr,ch,st2 + nr)
			l.append(transition)
		nfa2.NFA = l

		#memorare stare finala din NFA2, folosita in adaugarea tranzitiilor eps
		(s1,c,s2) = nfa2.NFA[len(nfa2.NFA) - 1]
		nfa2_final_state  = s2
		(s1,c,s2) = nfa1.NFA[len(nfa1.NFA) - 1]

		#adaugare tranzitii Epsilon
		nfa1.NFA.insert(0,(0,'eps',1))
		nfa1.NFA.insert(1,(0,'eps',s2 + 1))
		nfa1.NFA.append((s2,'eps',nfa2_final_state + 1))

		#reuniune NFA1 cu NFA2
		for t in nfa2.NFA:
			nfa1.NFA.append(t)
		nfa1.NFA.append((nfa2_final_state,'eps',nfa2_final_state + 1))

		#calculare stare finala si numar de stari din NFA-ul reuniune
		nfa1.final_states = [nfa2_final_state + 1]
		nfa1.nrStates = nfa1.nrStates + nfa2.nrStates + 2
		return nfa1

	#creeaza NFA pentru un obiect de tip Star 
	def convertStar(self,expr):
		#apel recursiv pentru transformarea expresiei pe care se aplica star
		nfa1 = self.convertType(expr.e)

		#numarul pentru fiecare stare creste cu 1 pentru ca starea initiala
			#adaugata sa fie 0
		l = []
		for (st1,ch,st2) in nfa1.NFA:
			l.append((st1+1,ch,st2 +1))
		nfa1.NFA = l

		#memorare stare finala folosita pentru adaugarea tranzitiilor eps
		(s1,c,s2) = nfa1.NFA[len(nfa1.NFA) - 1]
		nfa1_final_state  = s2

		#adaugare tranzitii Epsilon
		nfa1.NFA.insert(0,(0,"eps",1))
		nfa1.NFA.insert(1,(0, 'eps', nfa1_final_state + 1))
		nfa1.NFA.append((nfa1_final_state , 'eps', 1))
		nfa1.NFA.append((nfa1_final_state , 'eps', nfa1_final_state + 1))

		#calcul num ar de stari NFA
		nfa1.nrStates = nfa1.nrStates + 2
		return nfa1

	#elimina Paranteza si apeleaza recursiv crearea NFA-ului in functie de tipul
		#expresiei care se afla in paranteza 
	def convertParant(self,expr):
		return self.convertType(expr.p)


	#functie care apeleaza recursiv functiile de convertire in functie de 
		#tipul obiectului curent
	def convertType(self,expr):
		if (isinstance(expr,Character)):
			NFA = self.convertCharacter(expr)
		if (isinstance(expr,Concat)):
			NFA = self.convertConcat(expr)
		if (isinstance(expr,Union)):
			NFA = self.convertReunion(expr)
		if (isinstance(expr,Star)):
			NFA = self.convertStar(expr)
		if (isinstance(expr,Parant)):
			NFA = self.convertParant(expr)
		return NFA

#functie ce converteste inputul primit in arbore de parsare
def Pars_Expr(inStr):

	while (len(inStr) != 0): 
		#retinere caracter curent si urmatorul aracter
		char = inStr[0];
		inStr = inStr[1:]
		nextChar = ''
		if(len(inStr) != 0):
			nextChar = inStr[0]  

		#verificare gasire litera in input
		if (ord(char) > 96 and ord(char) < 123): #caractere intre a si z
			p.push(Character(char)) #punere obiect de tip Caracter pe stiva

			#reducere concatenare daca este posibil
			if (nextChar != '*' ): #verificare ca inputul sa nu contina *
				#se va face mai intai reducerea Star si mai apoi concatenarea
				if (len(p.stack) >= 2 and 
									isinstance(p.stack[len(p.stack) - 2],Expr)):
					p.reduceConcat()  

			#reducere reuniuni daca este posibil
			if (nextChar == ')' ): #verificare paranteza inchisa
				#in while ne asiguram ca pe stiva va ramane un singur obiect 
					#intre paranteze, care nu mai poate fi redus
				while(p.stack[len(p.stack) - 2] != '(' ):
					if(p.stack[len(p.stack) - 2] == '|'):
						p.reduceUnion()
					if(len(p.stack) <= 2):
							break
		#verificare paranteza deschisa si adaugarea ei pe stiva
		if(char == '('):
			p.push(char)
		#verificare simbol reuniune si adaugarea lui pe stiva
		if(char == '|'):
			p.push(char)
		#verificare paranteza inchisa si efectuarea tuturor reducerilor posibile
		if(char == ')'):
			p.reduceParant() #reducere paranteza

			if ((nextChar != '*')): #reducere concatenare, daca acest lucru mai 
										#mai este posibil
				if (len(p.stack) >= 2 and 
									isinstance(p.stack[len(p.stack) - 2],Expr)):
					p.reduceConcat() 
				#reducere reuniune daca acest lucru mai este posibil
				if (nextChar == ')' ):
					#in while ne asiguram ca pe stiva va ramane un singur obiect 
						#intre paranteze, care nu mai poate fi redus
					while(p.stack[len(p.stack) - 2] != '(' ): 
						if(p.stack[len(p.stack) - 2] == '|'):
							p.reduceUnion()
						if(len(p.stack) <= 2):
							break
		#verificare simbol star si reducerea expresiei
		if(char == '*'):
			p.reduceStar() #reducerea star
			#reducerea concatenarii daca este posibila dupa aplicarea lui Star
			if(len(p.stack) >= 2 and isinstance(p.stack[len(p.stack) - 2],Expr)):
				p.reduceConcat()
			# reducerea reuniunii din paranteze dupa aplicarea lui star
			if (nextChar == ')' ):
				while(p.stack[len(p.stack) - 2] != '(' ): 
					if(p.stack[len(p.stack) - 2] == '|'):
						p.reduceUnion()
					if(len(p.stack) <= 2):
						break 
	#realizarea de reduceri pana cand pe stiva se afla un singur obiect de tip 
			#EXPR
	while(len(p.stack) > 1):
		if(p.stack[len(p.stack) - 2] == '|'):
			p.reduceUnion()

#***************************TRANSFORMARE NFA - DFA******************************

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
			if ((n,'') in delta) and 
								(delta[(n,'')].issubset(set_of_states) == False):
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
	output_file1 = sys.argv[2]
	output_file2 = sys.argv[3]


	#deschidere fisier output
	out1 = open(output_file1,"w")
	out2 = open(output_file2, "w")
	inFile = open(input_file, 'rb+')
	inStr = ""

	#eliminare * consecutive
	while 1: 
		char = inFile.read(1)
		char = str(char,'utf-8')
		if ((char == '*' and inStr[len(inStr) - 1] != '*') or (char != '*')):
			inStr += char
		if not char:
			break
			#pozitionare la inceput de fisier
	inFile.seek(0,0)

	#creare arbore de parsare
	# ab -> Concat(Character(a), Character(b))
	p = Parser()
	Pars_Expr(inStr)
	expr = p.peek(len(p.stack)-1)

	#generare NFA
	convert = ConvertToNFA()
	NFA = convert.convertType(expr)


	#scriere output NFA in fisier
	out1.write(str(NFA.nrStates) +"\n")
	(s1,c,s2) = NFA.NFA[len(NFA.NFA) - 1]
	out1.write(str(s2 ) +"\n")
	lastState = ''
	lastChar =	''
	ok = 0
	for (s1,c,s2) in NFA.NFA:
		if (lastState == s1):
			if (lastChar == c):
				out1.write(" "+ str(s2))
			else:
				out1.write("\n")
				out1.write(str(s1) + " "+ c +" " +str(s2))
				lastChar = c

		else:
			if(ok != 0):
				out1.write("\n")
			out1.write(str(s1) + " "+ c +" " +str(s2))
			lastChar = c
			lastState = s1
		ok = 1;

	out1.close();
	

	#citire NFA din fisier
	delta = {}
	alphabet = []
	#citire din fisier si generare alfabet si reprezentare NFA
	with open(output_file1) as file:
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
	DFA = subset_construction(out2,epsClosures)
	#scriere DFA in fisier de out
	for (state,ch) in DFA:
		out2.write(str(state) + " " + ch + " " + str(DFA[(state,ch)]))
		out2.write("\n")

	inFile.close() 
	out1.close();
	out2.close();