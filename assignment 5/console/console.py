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


def getInputFile():

	fileName = raw_input("Enter input file name (eg. 'input1.txt'): ")
	return fileName


def console_menu():

	global Q
	global C

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
	print "5. Exit"
	print "================================================"
	print
	print "selected Q:", Q
	print "selected C:", C
	print
	print "------------"


def console_op1():
	pass

def console_run():

	# Clearing the screen
	if config.neat:
		uf_neatScreen()

	# Getting input file
	inputFileName = getInputFile()
	
	# Creating bayesian network by reading the file
	bn = BN.BayesianNetwork()
	bn.createBayesianNetwork(cause_effect_file=inputFileName)

	# Showing menu and further execution
	u_input = None

	while(u_input!=5):

		console_menu()
		u_input = raw_input("\nEnter option:")

		if u_input == 1:
			console_opt1()

		elif u_input == 2:
			console_opt2()

		elif u_input == 3:
			console_opt3

		elif u_input == 4:
			console_opt4()

		elif u_input == 5:
			break

		else:
			print "Please try again!"