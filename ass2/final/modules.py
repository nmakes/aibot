import turtle as t
from random import randrange
from time import time

maxint = 999999999999999999
minint = -999999999999999999
maxplayer = 1
minplayer = -1

verbose = False

def uf_zeroList(n):
	if verbose:
		print "uf_zeroList: ", n
	tempList = []
	for i in range(n):
		tempList.append(0)
	pass
	return tempList

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

	@staticmethod
	def opponent_node_type(nodeType):
		if nodeType==TreeNode.maxnode:
			return TreeNode.minnode
		else:
			return TreeNode.maxnode


	#constructor
	def __init__(self, state=None, nodeType=None, parent=None):
		
		if state==None:
			state = TreeNode.initial_state(16)
		if nodeType==None:
			nodeType = maxnode

		self.state = state
		self.nodeType = nodeType
		self.parent = parent

	#childnode
	def child_node(self, action):
		nextState = successor_function(self.state, action)
		childNode = TreeNode(nextState, TreeNode.opponent_node_type(self.nodeType))

# Serious WORK+++

# assume
	# state = [ [board_setting], player_turn ]
	# player = minplayer / maxplayer

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
				print "YES:: ^_^ :: ", triplet
			return board_setting[triplet[0]]
	if verbose:
		print "FATAL ERROR: utility_value | board_setting is not uniform for any triplet"
		print board_setting

	return 0

def min_value(state):

	if terminal_test(state):
		return utility_value(state)
	else:
		v = maxint
		Actions = actions(state)
		#print Actions
		for a in Actions:
			succ = successor_function(state,a)
			if succ!=None:
				v = min(v, max_value(succ))
		return v

def max_value(state):

	if terminal_test(state):
		return utility_value(state)
	else:
		v = minint
		Actions = actions(state)
		#print Actions
		for a in Actions:
			succ = successor_function(state,a)
			if succ!=None:
				v = max(v, min_value(succ))
		return v

def minimax_algorithm(state):

	if verbose:
		print state

	board_setting = state[0]
	player_turn = state[1]

	action = None

	if player_turn == maxplayer:
		v = minint
		for a in actions(state):
			#print "checking action ", a
			m = min_value(successor_function(state,a))
			if m > v:
				v = m
				action = a

	elif player_turn == minplayer:
		v = maxint
		for a in actions(state):
			#print "checking action ", a
			M = max_value(successor_function(state,a))
			if M < v:
				v = M
				action = a

	return successor_function(state, action)

# ALPHABETA

def alphabeta_min_value(state, alpha, beta):

	if terminal_test(state):
		return utility_value(state)
	else:
		v = maxint
		Actions = actions(state)
		#print Actions
		for a in Actions:
			succ = successor_function(state,a)
			if succ!=None:
				v = min(v, alphabeta_max_value(succ, alpha, beta))
				if v <= alpha:
					return v
				beta = min(beta,v)
		return v

def alphabeta_max_value(state, alpha, beta):

	if terminal_test(state):
		return utility_value(state)
	else:
		v = minint
		Actions = actions(state)
		#print Actions
		for a in Actions:
			succ = successor_function(state,a)
			if succ!=None:
				v = max(v, alphabeta_min_value(succ, alpha, beta))
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

	if player_turn == maxplayer:
		v = minint
		for a in actions(state):
			#print "checking action ", a
			m = alphabeta_max_value(successor_function(state,a), alpha, beta)
			if m > v:
				v = m
				action = a

	return successor_function(state, action)



def printBoard(state):
	print
	for row in range(4):
		for col in range(4):
			if state[0][row*4+col] == 1:
				print 'm',
			elif state[0][row*4+col] == -1:
				print 'H',
			else:
				print '.',
		print

	print "player: ", state[1]

def menu():
	print
	print

	print "1. Display empty board"
# t.fd(200)
# raw_input()

"""
WORKING CONSOLE GAME
"""

t1 = time()


print "making first move..."

initstate = [uf_zeroList(16),maxplayer]

# first move calculated
# ns = minimax_algorithm(initstate)
ns = alphabeta_algorithm(initstate)

print time() - t1, "seconds"
# first random computer move
# initstate[0][2] = 1
# initstate[1] = minplayer
# ns = initstate

while(True):
	if(terminal_test(ns)):
		print "GAME OVER"
		break
	printBoard(ns)
	inp = int(raw_input("move: "))
	ns = successor_function(ns, inp)
	printBoard(ns)
	print "thinking..."
	t1 = time()
	
	# ns = minimax_algorithm( ns )
	ns = alphabeta_algorithm( ns )
	print time()-t1, "seconds"
	if(terminal_test(ns)):
		print "GAME OVER"
		break

print "\n\n\n", ns
print "\n\n"
printBoard(ns)