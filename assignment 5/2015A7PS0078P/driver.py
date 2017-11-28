# Name: Naveen Venkat
# ID: 2015A7PS0078P

import bayesianNetwork as BN
import config

# utility function to clear the console
def uf_neatScreen():	
	for i in range(50):
		print

# Global variables to be used in the program
Q = []
C = []
markov_blanket = []

def getInputFile(): # Input the file name

	fileName = raw_input("Enter input file name (eg. 'input1.txt'): ")
	return fileName


def console_menu():

	global Q
	global C
	global markov_blanket

	if config.neat:
		uf_neatScreen()

	print
	print "------------"
	print "Console Menu"
	print "================================================"
	print "1. Choose query variables"
	print "2. Choose condition variables"
	print "3. Generate Markov Blanket of selected variables"
	print "4. Generate Query and Calculate Probability"
	print "5. Clear Selection"
	print "6. Exit"
	print "================================================"
	print
	print "selected Query:", Q
	print "selected Condition:", C
	print "generated markov blanket:", markov_blanket
	print
	print "------------"


def selected_vars(): # Gives the list of already selected variables

	global Q
	global C

	selectedVarList = []

	for v in Q:
		if v[0]=='~':
			selectedVarList.append(v[1:])
		else:
			selectedVarList.append(v)

	for v in C:
		if v[0]=='~':
			selectedVarList.append(v[1:])
		else:
			selectedVarList.append(v)

	return selectedVarList


def console_opt1(bn):
	
	global Q
	global C

	# Enumerate the variables that can be selected
	possible_true_variables = set(bn.keys()).difference(set(selected_vars()))
	
	# Keep the negated form as well
	possible_variables = list(possible_true_variables)
	for v in possible_true_variables:
		possible_variables.append('~'+v)

	# Show the possible variables
	print "Possible query variables:"

	for var in possible_true_variables:
		print var, '~'+var

	# Take the variable input
	v = raw_input("Enter a single capitalized query variable (eg. A, ~B): ")

	# Check if the variable is valid
	if v not in possible_variables:
			print "ERROR: Please enter a valid query variable"
			raw_input("Press enter to continue...")
			return
	
	# Append it to the list of query variables
	Q.append(v)


def console_opt2(bn):
	
	global Q
	global C

	# Enumerate the variables that can be selected
	possible_true_variables = set(bn.keys()).difference(set(selected_vars()))
	
	# Keep the negated form as well
	possible_variables = list(possible_true_variables)
	for v in possible_true_variables:
		possible_variables.append('~'+v)

	# Show the possible variables
	print "Possible condition variables:"

	for var in possible_true_variables:
		print var, '~'+var

	# Take the variable input
	v = raw_input("Enter a single capitalized condition variable (eg. A, ~B): ")

	# Check if the variable is valid
	if v not in possible_variables:
			print "ERROR: Please enter a valid condition variable"
			raw_input("Press enter to continue...")
			return
	
	# Append it to the list of condition variables
	C.append(v)


def console_opt3(bn):

	global Q
	global C
	global markov_blanket

	varList = BN.mergeList(Q,C)
	blanket = []

	for var in varList:
		blanket = BN.mergeList(blanket, bn.computeMarkovBlanket(var))

	markov_blanket = list(set(blanket))


def console_opt4(bn, solver):

	global Q
	global C

	generated_query = bn.createExpression(Q, C)

	probability = solver.P(generated_query['string'], bn)

	print "Given Query: ", generated_query['string']
	print "Calculated Probability: ", probability

	print 
	raw_input("press enter to continue ...")


def console_run():

	global Q
	global C
	global markov_blanket

	# Clearing the screen
	if config.neat:
		uf_neatScreen()

	# Getting input file
	inputFileName = getInputFile()
	
	# Creating bayesian network by reading the file
	bn = BN.BayesianNetwork()
	bn.createBayesianNetwork(cause_effect_file=inputFileName)

	# Creating a Probability Finder object
	solver = BN.ProbabilityFinder()

	# Showing menu and further execution
	u_input = None

	while(u_input!='6'):

		console_menu()
		u_input = raw_input("\nEnter option: ")

		if u_input == '1': # choose query variables
			console_opt1(bn)

		elif u_input == '2': # choose condition variables
			console_opt2(bn)

		elif u_input == '3': # generate markov blanket
			console_opt3(bn)

		elif u_input == '4': # generate query and solve

			# If no query variable is selected, it is an error.
			# However, we can have only query variables, without condition variables. It will be treated as the joint probability of query variables.
			if Q==[]:
				print "ERROR: No query variables are selected."
				raw_input("Press enter to continue...")
			else:
				console_opt4(bn, solver)

		elif u_input == '5': # clear selection
			Q = []
			C = []
			markov_blanket = []

		elif u_input == '6': # exit
			break

		else:
			print "Please try again!"


# ==================
# DRIVER STARTS HERE
# ==================

console_run()