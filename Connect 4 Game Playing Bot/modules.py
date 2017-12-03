"""
NAME: Naveen Venkat
ID: 2015A7PS0078P
"""

import turtle as t
from random import randrange
from time import time
from sys import getsizeof
import config

# utility function
def uf_zeroList(n): #Creates a list of zeroes of size n
	if config.verbose:
		print "uf_zeroList: ", n
	tempList = []
	for i in range(n):
		tempList.append(0)
	pass
	return tempList

def uf_neatScreen():	
	for i in range(50):
		print

# =========
# TREE NODE
# =========

class TreeNode(object):

	#static methods
	@staticmethod
	def initial_state(dim):
		tempList = []
		for i in range(dim):
			tempList.append(0)
		return [tempList, config.initial]

	#constructor
	def __init__(self, state=None, action=None, utilityValue=None):
		
		if state==None:
			state = TreeNode.initial_state(16)

		self.state = state
		self.action = action
		self.utilityValue = utilityValue

# STATE REPRESENTATION
#	state = [ [board_setting], player_turn ]
#	where player can be either config.minplayer or config.maxplayer
#	and board_setting is a vector of size 16

def is_ith_column_free(board_setting, i):
	if config.verbose:
		print "is_ith_column_free: ", i
	for row in range(4):
		if board_setting[row*4 + i] == 0:
			return True
	return False

def get_ith_column_free_cell_index(board_setting, i):
	if config.verbose:
		print "get_ith_column_free_cell_index: ", i
	for row in range(4):
		if board_setting[4*row + i] == 0:
			return 4*row + i
	if not(config.suppressGuiClicks):
		print "FATAL ERROR: get_ith_column_free_cell_index | ", i, "col is not empty. The board_setting is: "
	return None

def actions(state):
	if config.verbose:
		print "actions: ", state
	board_setting = state[0]

	possible_actions = []

	for i in range(4):
		if is_ith_column_free(board_setting, i):
			possible_actions.append(i+1)
	if config.verbose:
		print "possible_actions: ", possible_actions
	return possible_actions

def successor_function(state, action):

	if config.verbose:
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

	else:
		print "FATAL ERROR: Successor_Function got an invalid action =", action
		return None

	return [new_board_setting, -player_turn]

def terminal_test(state):
	if config.verbose:
		print "terminal_test: ", state
	board_setting = state[0]
	player_turn = state[1]

	for triplet in config.triplets:
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

# =============
# UTILITY VALUE
# =============

def utility_value(state):
	if config.verbose:
		print "utility_value: ", state
	board_setting = state[0]
	player_turn = state[1]

	for triplet in config.triplets:
		if is_uniform(board_setting, triplet):
			if config.verbose:
				print "Winning situation ", triplet
			return board_setting[triplet[0]]
			
	if config.verbose:
		print "FATAL ERROR: utility_value | board_setting is not uniform for any triplet"
		print board_setting

	return 0

# =================
# MINIMAX ALGORITHM
# =================

def min_value(state):

	if terminal_test(state):
		return utility_value(state)
	else:
		succ = None
		v = config.maxint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R1 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = max_value(childnode.state)
				v = min(v, childnode.utilityValue)
				config.tempStackSize -= 1
		return v

def max_value(state):

	if terminal_test(state):
		return utility_value(state)
	else:
		succ = None
		v = config.minint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R1 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = min_value(childnode.state)
				v = max(v, childnode.utilityValue)
				config.tempStackSize -= 1
		return v

def minimax_algorithm(state):

	if config.verbose:
		print state

	board_setting = state[0]
	player_turn = state[1]

	action = None
	succ = None

	t1 = time()

	if player_turn == config.maxplayer:
		v = config.minint
		for a in actions(state):
			succ = successor_function(state, a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R1 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = min_value(childnode.state)
				if childnode.utilityValue > v:
					v = childnode.utilityValue
					action = childnode.action
					config.guiAction = childnode.action
				config.tempStackSize -= 1

	elif player_turn == config.minplayer:
		v = config.maxint
		for a in actions(state):
			succ = successor_function(state, a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R1 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = max_value(childnode.state)
				if childnode.utilityValue < v:
					v = childnode.utilityValue
					action = a
					config.guiAction = childnode.action
				config.tempStackSize -= 1

	config.minimaxAgentTime += time() - t1

	return successor_function(state,action)

# ===================
# ALPHABETA ALGORITHM
# ===================

def alphabeta_min_value(state, alpha, beta):

	if terminal_test(state):
		#print utility_value(state)
		return utility_value(state)
	else:
		succ = None
		v = config.maxint
		for a in actions(state):
			succ = successor_function(state, a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R6 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = alphabeta_max_value(childnode.state, alpha, beta)
				v = min(v, childnode.utilityValue)
				if v <= alpha:
					return v
				beta = min(beta,v)
				config.tempStackSize -= 1
		return v

def alphabeta_max_value(state, alpha, beta):

	if terminal_test(state):
		#print utility_value(state)
		return utility_value(state)
	else:
		succ = None
		v = config.minint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R6 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = alphabeta_min_value(childnode.state, alpha, beta)
				v = max(v, childnode.utilityValue)
				if v >= beta:
					return v
				alpha = max(alpha, v)
				config.tempStackSize -= 1
		return v

def alphabeta_algorithm(state):

	if config.verbose:
		print state

	board_setting = state[0]
	player_turn = state[1]

	action = None

	alpha = config.minint
	beta = config.maxint

	t1 = time()

	if player_turn == config.maxplayer:
		v = config.minint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R6 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = alphabeta_min_value(childnode.state, alpha, beta)
				if childnode.utilityValue > v:
					v = childnode.utilityValue
					action = a
					config.guiAction = a
				config.tempStackSize -= 1

	if player_turn == config.minplayer:
		v = config.maxint
		for a in actions(state):
			succ = successor_function(state,a)
			if succ!=None:
				childnode = TreeNode(succ, a)
				config.R6 += 1
				config.tempStackSize += 1
				if config.tempStackSize > config.maxStackSize:
					config.maxStackSize = config.tempStackSize
				childnode.utilityValue = alphabeta_max_value(childnode.state, alpha, beta)
				if childnode.utilityValue < v:
					v = childnode.utilityValue
					action = a
					config.guiAction = a
				config.tempStackSize -= 1

	config.alphaBetaAgentTime += time() - t1

	return successor_function(state,action)

# =======================
# CONSOLE FUNCTIONALITIES
# =======================

def print_board(state):
	if config.neat:
		uf_neatScreen()
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

	if state[1] == config.maxplayer:
		print "Human moved"
	elif state[1] == config.minplayer:
		print "Machine moved"
	elif state[1] == config.initial:
		print "Initial state"
	print

	if config.neat:
		raw_input("press enter to continue...")

def menu():

	if config.neat:
		uf_neatScreen()

	print
	print "Menu"
	print "----"
	#print "========================================="
	print "1. Display empty board"
	print "2. Play the game using Minimax algorithm"
	print "3. Play the game using Alpha Beta pruning"
	print "4. Show all results (R1 - R12)"
	print "5. Exit"
	#print "========================================="
	print

def publish_minimax_stats():
	print
	print "Minimax based analysis"
	print "R1 (number of nodes generated) = ", config.R1
	print "R2 (memory allocated to one node) = ", config.R2
	print "R3 (maximum growth of the implicit stack) = ", config.R3
	print "R4 (total time to play the game) = ", config.R4
	print "R5 (number of nodes created in one micro second) = ", config.R5
	#print "minimaxAgentTime = ", config.minimaxAgentTime

def publish_alphabeta_stats():
	print
	print "Alpha Beta pruning based analysis"
	print "R6 (number of nodes generated) = ", config.R6
	print "R7 (saving using pruning) = ", config.R7
	print "R8 (total time to play a game) = ", config.R8
	#print "alphaBetaAgentTime = ", config.alphaBetaAgentTime

def publish_comparative_stats():

	if config.R6==0:
		print "Please play minimax game first, then alpha beta game, and then run the analysis"
	else:
		config.R9 = config.R1 / config.R6
		print
		print "Comparative Analysis"
		print "R9 (minimax/alphabeta) = ", config.R9
		print "R10 (average time to play the game) = ", config.R10
		print "R11 (number of times player M wins) = ", config.R11
		print "R12 (average number of times player M wins) = ", config.R12
		print

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

# ==================
# CONSOLE BASED GAME
# ==================

def play_console_minimax_game():

	config.R1 = 0 # number of nodes generated till the problem is solved
	config.R2 = 0 # amount of memory allocated to one node
	config.R3 = 0 # the maximum growth of the implicit stack
	config.R4 = 0 # the total time to play the game
	config.R5 = 0 # the number of nodes created in one micro second

	t1 = time()
	config.R2 = getsizeof(TreeNode)

	initstate = [uf_zeroList(16),config.maxplayer]

	"""first move hard coded"""
	if config.verbose:
		print "first move hard coded"
	ns = initstate
	ns[0][0] = config.maxplayer
	ns[1] = config.minplayer
	print_board(ns)

	"""first move calculated"""
	# if config.verbose:
	# 	print "first move calculated"
	# print "Computer is calculating the first move. This may take upto 90 seconds (on i7 7700HQ under moderate load). Please wait..."
	# ns = minimax_algorithm(initstate)
	# print_board(ns)
	
	while(True):

		inp = int(raw_input("move: "))
		#if inp not in range(1,5):
		ns = successor_function(ns, inp)
		print_board(ns)

		if(terminal_test(ns)):
			print "YOU WIN"
			break

		if config.neat:
			uf_neatScreen()
		
		print "thinking..."
		ns = minimax_algorithm( ns )
		print_board(ns)

		if(terminal_test(ns)):
			config.R11 += 1
			print "YOU LOSE"
			break

	t2 = time()
	config.R4 = t2-t1
	config.R3 = config.maxStackSize
	config.maxStackSize = 0
	config.tempStackSize = 0
	config.R5 = (float(config.R1) / float(config.minimaxAgentTime)) / 100000
	config.minimaxAgentTime = 0

	if config.neat:
		raw_input("press enter to continue ...")

def play_console_alphabeta_game():

	config.R6 = 0 # the number of nodes generated till the problem is solved
	config.R7 = 0 # (R1 - R6)/R1 : saving using pruning
	config.R8 = 0 # the total time to play a game

	config.R8 = 0

	t1 = time()
	config.R2 = getsizeof(TreeNode)

	initstate = [uf_zeroList(16),config.maxplayer]

	"""first move hard coded"""
	# if config.verbose:
	# 	print "first move hard coded"
	# ns = initstate
	# ns[0][0] = config.maxplayer
	# ns[1] = config.minplayer
	# print_board(ns)

	"""first move calculated"""
	if config.verbose:
		print "first move calculated"
	ns = alphabeta_algorithm(initstate)
	print_board(ns)

	while(True):

		inp = int(raw_input("move: "))
		ns = successor_function(ns, inp)
		print_board(ns)

		if(terminal_test(ns)):
			print "YOU WIN"
			break

		if config.neat:
			uf_neatScreen()

		print "thinking..."
		ns = alphabeta_algorithm( ns )
		print_board(ns)

		if(terminal_test(ns)):
			config.R11 += 1
			print "YOU LOSE"
			break

	t2 = time()
	config.R8 = t2-t1

	config.R7 = float(float((config.R1 - config.R6))/float(config.R1))
	config.alphaBetaAgentTime = 0

	if config.neat:
		raw_input("press enter to continue...")