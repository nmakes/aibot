import turtle as t
from random import randrange
from time import time
from sys import getsizeof
import config

maxint = 999999999999999999
minint = -999999999999999999
maxplayer = 1
minplayer = -1

verbose = False

# utility function
def uf_zeroList(n): #Creates a list of zeroes of size n
	if verbose:
		print "uf_zeroList: ", n
	tempList = []
	for i in range(n):
		tempList.append(0)
	pass
	return tempList

# Tree Node
class TreeNode(object):

	'''
	| state
	| nodeType - maxnode / minnode
	'''

	# static variables
	maxnode = 1
	minnode = -1

	#static methods
	@staticmethod
	def initial_state(dim):
		tempList = []
		for i in range(dim):
			tempList.append(0)
		return tempList

	#constructor
	def __init__(self, state=None, action=None, utilityValue=None):
		
		if state==None:
			state = TreeNode.initial_state(16)

		self.state = state
		self.action = action
		self.utilityValue = utilityValue

# State representation
	# state = [ [board_setting], player_turn ]
	# where player can be either minplayer or maxplayer
	# and board_setting is a vector of size 16

def is_ith_column_free(board_setting, i):
	if verbose:
		print "is_ith_column_free: ", i
	for row in range(4):
		if board_setting[row*4 + i] == 0:
			return True
	return False

def get_ith_column_free_cell_index(board_setting, i):
	if verbose:
		print "get_ith_column_free_cell_index: ", i
	for row in range(4):
		if board_setting[4*row + i] == 0:
			return 4*row + i
	print "FATAL ERROR: get_ith_column_free_cell_index | ", i, "col is not empty. The board_setting is: "
	return None

def actions(state):
	if verbose:
		print "actions: ", state
	board_setting = state[0]

	possible_actions = []

	for i in range(4):
		if is_ith_column_free(board_setting, i):
			possible_actions.append(i+1)
	if verbose:
		print "possible_actions: ", possible_actions
	return possible_actions

def successor_function(state, action):

	if verbose:
		print "successor_function: ", state, ": ", action

	if action==None:
		return None

	board_setting = state[0]
	player_turn = state[1]

	if action == 1:
		i = get_ith_column_free_cell_index(board_setting, 0)
		if(i==None):
			return None
		new_board_setting = list(board_setting)
		new_board_setting[i] = player_turn

	elif action == 2:
		i = get_ith_column_free_cell_index(board_setting, 1)
		if(i==None):
			return None
		new_board_setting = list(board_setting)
		new_board_setting[i] = player_turn

	elif action == 3:
		i = get_ith_column_free_cell_index(board_setting, 2)
		if(i==None):
			return None
		new_board_setting = list(board_setting)
		new_board_setting[i] = player_turn

	elif action == 4:
		i = get_ith_column_free_cell_index(board_setting, 3)
		if(i==None):
			return None
		new_board_setting = list(board_setting)
		new_board_setting[i] = player_turn

	return [new_board_setting, -player_turn]

def terminal_test(state):
	if verbose:
		print "terminal_test: ", state
	board_setting = state[0]
	player_turn = state[1]

	triplets = [ [0,1,2], [1,2,3], [4,5,6], [5,6,7], [8,9,10], [9,10,11], [0,5,10], [1,6,11], [3,6,9], [2,5,8], [0,4,8], [1,5,9], [2,6,10], [3,7,11], [12,13,14], [13,14,15], [4,8,12], [5,9,13], [6,10,14], [7,11,15], [4,9,14], [5,10,15], [6,9,12], [7,10,13] ]

	for triplet in triplets:
		if is_uniform(board_setting, triplet):
			return True

	for i in range(16):
		if board_setting[i]==0:
			return False

	return True

def is_uniform(board_setting, triplet):
	
	if (board_setting[triplet[0]] == board_setting[triplet[1]] == board_setting[triplet[2]]) & (board_setting[triplet[0]]!=0):
		return True
	
	return False

def utility_value(state):
	if verbose:
		print "utility_value: ", state
	board_setting = state[0]
	player_turn = state[1]

	triplets = [ [0,1,2], [1,2,3], [4,5,6], [5,6,7], [8,9,10], [9,10,11], [0,5,10], [1,6,11], [3,6,9], [2,5,8], [0,4,8], [1,5,9], [2,6,10], [3,7,11], [12,13,14], [13,14,15], [4,8,12], [5,9,13], [6,10,14], [7,11,15], [4,9,14], [5,10,15], [6,9,12], [7,10,13] ]

	for triplet in triplets:
		if is_uniform(board_setting, triplet):
			if verbose:
				print "Winning situation ", triplet
			return board_setting[triplet[0]]
	if verbose:
		print "FATAL ERROR: utility_value | board_setting is not uniform for any triplet"
		print board_setting

	return 0

# MINIMAX ALGORITHM

def min_value(state):

	if terminal_test(state):
		return utility_value(state)
	else:
		succ = None
		v = maxint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = max_value(childnode.state)
				config.R1 += 1
				v = min(v, childnode.utilityValue)
		return v

def max_value(state):

	if terminal_test(state):
		return utility_value(state)
	else:
		succ = None
		v = minint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = min_value(childnode.state)
				config.R1 += 1
				v = max(v, childnode.utilityValue)
		return v

def minimax_algorithm(state):

	if verbose:
		print state

	board_setting = state[0]
	player_turn = state[1]

	action = None
	succ = None

	t1 = time()

	if player_turn == maxplayer:
		v = minint
		for a in actions(state):
			succ = successor_function(state, a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = min_value(childnode.state)
				config.R1 += 1
				if childnode.utilityValue > v:
					v = childnode.utilityValue
					action = childnode.action

	elif player_turn == minplayer:
		v = maxint
		for a in actions(state):
			succ = successor_function(state, a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = max_value(childnode.state)
				config.R1 += 1
				if childnode.utilityValue < v:
					v = childnode.utilityValue
					action = a

	config.minimaxAgentTime += time() - t1

	return successor_function(state,action)

# ALPHABETA ALGORITHM

def alphabeta_min_value(state, alpha, beta):

	if terminal_test(state):
		#print utility_value(state)
		return utility_value(state)
	else:
		succ = None
		v = maxint
		for a in actions(state):
			succ = successor_function(state, a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = alphabeta_max_value(childnode.state, alpha, beta)
				config.R6 += 1
				v = min(v, childnode.utilityValue)
				if v <= alpha:
					return v
				beta = min(beta,v)
		return v

def alphabeta_max_value(state, alpha, beta):

	if terminal_test(state):
		#print utility_value(state)
		return utility_value(state)
	else:
		succ = None
		v = minint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = alphabeta_min_value(childnode.state, alpha, beta)
				config.R6 += 1
				v = max(v, childnode.utilityValue)
				if v >= beta:
					return v
				alpha = max(alpha, v)
		return v

def alphabeta_algorithm(state):

	if verbose:
		print state

	board_setting = state[0]
	player_turn = state[1]

	action = None

	alpha = minint
	beta = maxint

	t1 = time()

	if player_turn == maxplayer:
		v = minint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = alphabeta_min_value(childnode.state, alpha, beta)
				config.R6 += 1
				if childnode.utilityValue > v:
					v = childnode.utilityValue
					action = a

	if player_turn == minplayer:
		v = maxint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				childnode.utilityValue = alphabeta_max_value(childnode.state, alpha, beta)
				config.R6 += 1
				if childnode.utilityValue < v:
					v = childnode.utilityValue
					action = a

	config.alphaBetaAgentTime += time() - t1

	return successor_function(state,action)

def print_board(state):
	print
	for row in range(4):
		for col in range(4):
			if state[0][row*4+col] == 1:
				print 'o',
			elif state[0][row*4+col] == -1:
				print 'x',
			else:
				print '.',
		print

	if state[1] == maxplayer:
		print "Human moved"
	if state[1] == minplayer:
		print "Machine moved"

	print

def menu():
	print
	print

	print "1. Display empty board"
	print "2. Play the game using Minimax algorithm"
	print "3. Play the game using Alpha Beta pruning"
	print "4. Show all results (R1 - R12)"

def publish_minimax_stats():
	print "R1 = ", config.R1
	print "R2 = ", config.R2
	print "R3 = ", config.R3
	print "R4 = ", config.R4
	print "R5 = ", config.R5
	print "minimaxAgentTime = ", config.minimaxAgentTime

def publish_alphabeta_stats():
	print "R6 = ", config.R6
	print "R7 = ", config.R7
	print "R8 = ", config.R8
	print "alphaBetaAgentTime = ", config.alphaBetaAgentTime

def publish_comparative_stats():
	print "R9 = ", config.R9
	print "R10 = ", config.R10
	print "R11 = ", config.R11
	print "R12 = ", config.R12

def reset_all_stats():
	# Minimax based analysis
	config.R1 = 0 # number of nodes generated till the problem is solved
	config.R2 = 0 # amount of memory allocated to one node
	config.R3 = 0 # the maximum growth of the implicit stack
	config.R4 = 0 # the total time to play the game
	config.R5 = 0 # the number of nodes created in one micro second

	# Alpha Beta pruning based analysis
	config.R6 = 0 # the number of nodes generated till the problem is solved
	config.R7 = 0 # (R1 - R6)/R1 : saving using pruning
	config.R8 = 0 # the total time to play a game

	# Comparative analysis
	config.R9 = 0 # the memory used in both the techniques (Minimax and Alpha Beta pruning)
	config.R10 = 0 # average time to play the game ( 10 times )
	config.R11 = 0 # the number of times player M wins
	config.R12 = 0 # average number of times player M wins ( repeating the step in R10 for 20 times)

"""
WORKING CONSOLE GAME
"""

def play_console_minimax_game():

	t1 = time()
	config.R2 = getsizeof(TreeNode)

	initstate = [uf_zeroList(16),maxplayer]

	"""first move hard coded"""
	if verbose:
		print "first move hard coded"
	ns = initstate
	ns[0][0] = maxplayer
	ns[1] = minplayer

	"""first move calculated"""
	# if verbose:
	# 	print "first move calculated"
	# print "Computer is calculating the first move. This may take upto 90 seconds (on i7 7700HQ under moderate load). Please wait..."
	# ns = minimax_algorithm(initstate)

	while(True):

		if(terminal_test(ns)):
			print_board(ns)
			print "GAME OVER"
			break
		
		print_board(ns)
		
		inp = int(raw_input("move: "))
		ns = successor_function(ns, inp)
		print_board(ns)
		
		print "thinking..."
		ns = minimax_algorithm( ns )

		if(terminal_test(ns)):
			print_board(ns)
			print "GAME OVER"
			break

	t2 = time()
	config.R4 = t2-t1

	publish_minimax_stats()

def play_console_alphabeta_game():

	t1 = time()
	config.R2 = getsizeof(TreeNode)

	initstate = [uf_zeroList(16),maxplayer]

	"""first move hard coded"""
	# if verbose:
	# 	print "first move hard coded"
	# ns = initstate
	# ns[0][0] = maxplayer
	# ns[1] = minplayer

	"""first move calculated"""
	if verbose:
		print "first move calculated"

	ns = alphabeta_algorithm(initstate)

	while(True):

		if(terminal_test(ns)):
			print_board(ns)
			print "GAME OVER"
			break

		print_board(ns)

		inp = int(raw_input("move: "))
		ns = successor_function(ns, inp)
		print_board(ns)

		print "thinking..."
		ns = alphabeta_algorithm( ns )

		if(terminal_test(ns)):
			print_board(ns)
			print "GAME OVER"
			break

	t2 = time()
	config.R8 = t2-t1

	config.R7 = float(float((config.R1 - config.R6))/float(config.R1))

	publish_alphabeta_stats()

play_console_minimax_game()
play_console_alphabeta_game()