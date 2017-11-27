# Name: Naveen Venkat
# ID: 2015A7PS0078P

import FileHelper as fh

def mergeList(list1, list2):
	retList = []

	for i in list1:
		retList.append(i)

	for i in list2:
		retList.append(i)

	return retList


class VariableNode:

	def __init__(self, var, causeList, PP, condProbList, numCauses):
		self.varName = var
		self.parentsInOrder = causeList # Useful to make the table
		self.parents = set(causeList)
		self.childrenInOrder = [] # list to be processed
		self.children = set() # set to be processed
		self.PP = PP
		self.condProbList = condProbList
		self.numCauses = numCauses


	def __str__(self):
		retstr = ""
		retstr += str(list(self.parentsInOrder)) + "   ->   |#| " + self.varName + " |#|   ->   " + str(self.childrenInOrder)
		return retstr


class BayesianNetwork(dict): # Inherits from dict datatype

	# This data structure will be a similar to the dictionary datatype. Operations will be similar to a dictionary.
	# Reason for using this is to allow O(1) search time.

	def __init__(self, vertexDict = None):
		# vertexDict is a dictionary of VariableNodes indexed (key) by the name
		self = vertexDict


	def createBayesianNetwork(self, cause_effect_file): #Populates the network

		# Create a helper object and preprocess (as described in class FileHelper)
		helper = fh.FileHelper()
		helper.preProcess(cause_effect_file)

		# Obtain lists of each attribute of the variable node
		hVars = helper.getAttributes('var')
		hCauseList = helper.getAttributes('causeList')
		hPP = helper.getAttributes('PP')
		hCondProbList = helper.getAttributes('condProbList')
		hNumCauses = helper.getAttributes('numCauses')		

		# create nodes
		for i in range(len(hVars)):
			self[hVars[i]] = VariableNode(hVars[i], hCauseList[i], hPP[i], hCondProbList[i], hNumCauses[i])

		# compute children
		for var in self.keys(): # For each variable node,
			for par in self[var].parents: # for each parent of that variable node,
				(self[par].childrenInOrder).append(var) # append the variable node to the list of children
				(self[par].children).add(var) # add the variable node to the set of children


	def computeMarkovBlanket(self, node):

		markovBlanket = set() # We want a set so as to avoid repeating elements
		varNode = self[node]

		# add parents to the blanket
		for parent in varNode.parentsInOrder:
			markovBlanket.add(parent)

		# add children to the blanket
		for child in varNode.childrenInOrder:
			markovBlanket.add(child)

		# add children's parents
		for childOfVarNode in varNode.childrenInOrder:
			for parentOfChildOfVarNode in self[childOfVarNode].parentsInOrder:
				markovBlanket.add(parentOfChildOfVarNode)

		# convert the final set into list and return
		return list(markovBlanket)


	def createExpression(self, Q, C):

		# Q = list of query variables
		# C = list of condition variables

		if len(Q) == 0:
			print
			print "INVALID QUERY"
			print

		# Declaring expression as a dictionary
		expression = {}

		# It will contain the list of query variables and condition variables
		expression['query'] = Q
		expression['cond'] = C

		# Additionally it will also contain a string denoting the expression
		# eg. 'P(A,B,C|G,~H)'
		expression['string'] = ""

		# Generating the string
		exprStr = "P("
		lq = len(Q)
		lc = len(C)

		for i in range(lq):
			if i<lq-1:
				exprStr += Q[i] + ","
			else:
				exprStr += Q[i]

		if lc==0: # If only query variables are there, then it is just a joint probability
			# Nothing more to be done
			pass
		else: 
			# Append causes as well
			exprStr += "|"

			for i in range(lc):
				if i<lc-1:
					exprStr += C[i] + ","
				else:
					exprStr += C[i]

		exprStr += ")"
		expression['string'] = exprStr

		return expression


class ProbabilityFinder:

	def getMarkovExpansions(self, expr, bn):
		
		query = expr['query']
		cond = expr['cond']
		string = expr['string']

		probabilityList = []

		for var in query:
			markovBlanket = bn.computeMarkovBlanket(var)
			probabilityList.append(markovBlanket)

		return probabilityList


	def getRankFromModel(self, vars): # Returns the index into the CPT by observing the state of vars

		'''
		Note: A negated variable, eg. '~A' is considered as a 0. A true variable eg. 'B' is considered as a 1.

		This will be used to get the CPT from the conditional probability table as follows:
		- The value of P('A'|'B','~C','D') would be taken from the CPT.
		- The index of the entry is given by 
				
				getRankFromModel(['B','~C','D'])
		'''

		rank = 0

		for var in vars:
			if var[0]=='~':
				rank += 0
			else:
				rank += 1

			rank *= 2

		return rank


	def getModelFromRank(self, vars, rank):

		# Assumes that all vars are in their true form.
		# i.e No variable is of the form '~A'.

		if rank > 2**len(vars):
			if config.flag_show_errors:
				print
				print "### FATAL ERROR 1 [ProbabilityFinder.getModelFromRank()]: rank is more than 2**len(vars)"
				print
			return None
		else:

			newVarExpr = [] # the new expression

			# get binary representation
			binary = format(rank, 'b')

			# extend the number of bits
			while len(binary) < len(vars):
				binary = '0' + binary

			# get the expression from binary string
			for i in range(len(binary)):
				var = vars[i]
				binaryBit = binary[i]

				if binaryBit=='1':
					newVar = var
				else:
					newVar = '~'+var
				
				newVarExpr.append(newVar)

			return newVarExpr

	
	def getAllModels(self, vars):
		
		# Assumes an ordered list of vars
		
		models = []

		# For every number from 0 to 2**N, generate the expression
		for i in range(2**len(vars)):
			models.append(self.getModelFromRank(vars, i))

		return models


	def getJPExprFromCPExpr(self, expr, bn): # Converts conditional probability expression into ratio of joint probability expressions

		''' eg.

			P(A,B,C|D,E) will be converted to

				P(A,B,C,D,E) / P(D,E)

			The division is taken care in the P() function that calculates the probabilities. This function returns a dictionary
			that contains the numerator and denominator as two values.
		'''

		# Dictionary corresponding to the joint probability ratio
		JP = {}

		# Check whether the given expression is a conditional probability expression
		if '|' not in expr:
			if config.flag_show_errors:
				print
				print "### WARNING [ProbabilityFinder.getJPfromCP()]: given expr does not correspond to conditional probability. expr =", expr
				print
			return {'numerator':expr, 'denominator':None}
		else:
			# Get the variables from the probability string
			agenda = expr.split('(')[1]
			agenda = expr.split(')')[0]

			# Form numerator
			numerator = ','.join(agenda.split('|'))
			numerator = numerator.split(',')
			JP['numerator'] = (bn.createExpression(numerator))['string']

			# Form denominator
			denominator = agenda.split('|')[1]
			denominator = denominator.split(',')
			JP['denominator'] = (bn.createExpression(denominator))['string']

			return JP

	def P(self, expr, bn):
		'''
			Parameters:
			- expr: The string expression of probability
					eg. 'P(A,B,C)' for joint probability, 'P(A|B,C)' for conditional probability

			Result:
			- Value of the given probability expression
		'''

		# Keep track of whether the given expression corresponds to joint or conditional probability
		type_of_expr = None

		# Get the variables from the probability string
		agenda = expr.split('(')[1]
		agenda = expr.split(')')[0]

		# Find out whether it is a conditional probability or joint probability
		if '|' in agenda:
			type_of_expr = 'conditional'
		else:
			type_of_expr = 'joint'

		'''
			The expression will be evaluated as follows:
			
			1. if it is a conditional probability, and it is not of the form of P(A|parents), convert it to joint probability in numerator
			   and denominator and call P on each.
			2. if it is a conditional probabilty, and of the form P(A|parents) find the probabilty from the CPT and return.
			3. if it is a joint probabiltiy, expand each variable along all the models of its
			   parents and evaluate the joint probability thus obtained.
		'''


		if type_of_expr == 'conditional':

			'''
				The given string will be of the form

					P(query|causes)

				Extract this into two variables and inspect further.
			'''
			splitAgenda = agenda.split('|')
			
			query = splitAgenda[0]

			causes = splitAgenda[1]
			causes.split(',')

			'''
				Inspect the query. 
				If number of variables is more than one, then convert it into
				joint probability and call this function recursively on both. Otherwise, check further
				if all the variables given in the causes part are exactly equal to the parents. If yes,
				then return the value from the CPT. Otherwise, convert it into joint probability and
				call recursively.
			'''
			query = query.strip()
			query = query.split(',')

			if len(query)!=1:
				
				'''
				@TODO: JPfromCP
				'''


		elif type_of_expr == 'joint':

			jointVars = agenda.split(',')

			'''
				Explanation of the algorithm followed for joint probability:

				We go one by one on each variable in the given list of variables.
				If the parent of the given variable already exists, we ignore it.
				Otherwise, we calculate two joint probabilities corresponding to each parent,
				and sum it. This function is called recursively until all the variables' parents
				are exhausted.

				For eg.

					If the bayesian network is as follows:
					
					par    children
					A  --> B, C
					B  --> D, C
					E  --> B
				
				Consider the expression

					P(C,D)

				The following will be the execution:
				
				Expand C's parents.
				
					= P(C,D,A,B) + P(C,D,A,~B) + P(C,D,~A,B) + P(C,D,~A,~B)
				
				Now, all C's parents have been expanded. P will be called on
				each of the four expressions.

					(a) Consider P(C,D,A,B).

						C's parents already exist in the joint probability list (agenda).
						So skip to the next variable, ie. D. D's parents also exist.
						So, skip to A. A doesn't have parents, so skip to B.

							= P(C,D,A,B,E) + P(C,D,A,B,~E)

						Now, apply the same again on each of these two.

							(i) Consider P(C,D,A,B,E).
							
								All parents exist in the expression, so we are ready to evaluate it.

								To evaluate it, do the following:

									= P(C|parents) * P(D|parents) * P(A|parents) * P(B|parents) * P(E|parents)
								
								We know C's parents A and B occur in the form 'A' and 'B'. 
								Similarly, for B. 
								A doesn't have parents, so this reduces to P(A).
								B has a parent E, which occurs in the form 'E'.
								E doesn't have parents, so this is just P(E)

								Thus the above reduces to:

									= P(C|A,B) * P(D|B) * P(A) * P(B|E) * P(E)
								
								This can be obtained from the corresponding CPTs for each variable.

							(ii) Consider P(C,D,A,B,E).
							
								Following the discussion in part (i) this above reduces to:

									= P(C|A,B) * P(D|B) * P(A) * P(B|~E) * P(~E)
								
								which can be obtained from the corresponding CPTs.

						From (i) and (ii) we find P(C,D,A,B) by adding them.

					(b) P(C,D,A,~B).
					(c) P(C,D,~A,B).
					(d) P(C,D,~A,~B).

				(b), (c), (d) can be found in similar way as explained in (a).

				Adding these four, we get the result of P(C,D).
			'''

			# After we find
			for var in jointVars:

				# We consider only the parents for expansion for this problem.
				# This can be extended to the complete markov blanket, but it will give the same result
				# (as mentioned in the AIMA book)

				parents = bn[var].parentsInOrder

				parentsNotInList = []
				
				# Enumerate the parents that are already not considered in the joint probability expression
				for p in parents:
					if p in jointVars: 	# if p has been considered, ignore it
						continue
					else:				# otherwise add p to the list
						parentsNotInList.append(p)

				# Now expand according to the parentsNotInList
				if len(parentsNotInList)==0: # If all parents have been considered in the list, move to the next variable
					continue
				else: # otherwise find sum of the joint probabilities considering all the models of the parentsNotInList

					# Sum of the joint probabilities as explained above
					sum = 0

					# Enumerate all the models
					models = getAllModels(parentsNotInList)

					# For each model, we get a joint probability
					for model in models:
						sum += P( (bn.createExpression(mergeList(jointVars, parentsNotInList))['string'], []))

					# return the sum
					return sum

			'''
				By now, all the 

				@TODO: after all the variables have been expanded, now find probability
			'''



n = BayesianNetwork()
n.createBayesianNetwork('input1.txt')

for key in n:
	print key + " :: " + str(n[key])

print "----"
print n.computeMarkovBlanket('B')
expr = n.createExpression(['A','D','C'], ['G','H'])
print expr

print n.createExpression(['A','D','C'], [])

print ProbabilityFinder().getMarkovExpansions(expr, n)
print ProbabilityFinder().getRankFromModel(['~A','~B','F','~D','~E','~H'])
print ProbabilityFinder().getModelFromRank(['A','B','F','D','E','H'], 45)
print ProbabilityFinder().getAllModels(['A','B','F','D'])

