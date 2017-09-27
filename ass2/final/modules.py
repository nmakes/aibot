import turtle as t

maxint = 999999999999999999
minint = -999999999999999999
maxplayer = 1
minplayer = -1

def uf_zeroList(n):
	tempList = []
	for i in range(n):
		tempList
	pass

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
	for row in range(4):
		if board_setting[row*4 + i] == 0:
			return True
	return False

def get_ith_column_free_cell_index(board_setting, i):
	for row in range(4):
		if board_setting[4*row + i] == 0:
			return 4*row + i
	print "FATAL ERROR: get_ith_column_free_cell_index | ", i, "col is not empty. The board_setting is: "
	print board_setting
	return None

def actions(state):

	board_setting = state[0]

	possible_actions = []

	for i in range(4):
		if is_ith_column_free(board_setting, i):
			possible_actions.append(i+1)

	return possible_actions

def successor_function(state, action):

	board_setting = state[0]
	player_turn = state[1]

	if action == 1:
		i = get_ith_column_free_cell_index(board_setting, 0)
		board_setting[i] = player_turn
		new_board_setting = board_setting

	elif action == 2:
		i = get_ith_column_free_cell_index(board_setting, 1)
		board_setting[i] = player_turn
		new_board_setting = board_setting

	elif action == 3:
		i = get_ith_column_free_cell_index(board_setting, 2)
		board_setting[i] = player_turn
		new_board_setting = board_setting

	elif action == 4:
		i = get_ith_column_free_cell_index(board_setting, 3)
		board_setting[i] = player_turn
		new_board_setting = board_setting

	return [new_board_setting, -player_turn]


def terminal_test(state):
	
	board_setting = state[0]
	player_turn = state[1]

	for i in range(16):
		pass

def is_uniform(board_setting, triplet):
	
	if board_setting[triplet[0]] == board_setting[triplet[1]] == board_setting[triplet[2]]:
		return True
	
	return False

def utility_value(state):

	board_setting = state[0]
	player_turn = state[1]

	triplets = [ [0,1,2], [1,2,3], [4,5,6], [5,6,7], [8,9,10], [9,10,11], [0,5,10], [1,6,11], [3,6,9], [2,5,8], [0,4,8], [1,5,9], [2,6,10], [3,7,11], [12,13,14], [13,14,15], [4,8,12], [5,9,13], [6,10,14], [7,11,15], [4,9,14], [5,10,15], [6,9,12], [7,10,13] ]

	for triplet in triplets:
		if is_uniform(board_setting, triplet):
			return board_setting[triplet[0]]

	print "FATAL ERROR: utility_value | board_setting is not uniform for any triplet"
	print board_setting
	return None

def min_value(state):
	if terminal_test(state):
		return utility_value(state)
	else:
		v = maxint
		for a in actions(state):
			v = min(v, max_value(successor_function(state,a)))
		return v

def max_value(state):
	if terminal_test(state):
		return utility_value(state)
	else:
		v = minint
		for a in actions(state):
			v = max(v, min_value(successor_function(state,a)))
		return v

def minimax_algorithm(state):

	board_setting = state[0]
	player_turn = state[1]

	if player_turn == maxplayer:
		v = minint
		for a in actions(state):
			v = max(v, min_value(successor_function(state,a)))
		return v

	elif player_turn == minplayer:
		v = maxint
		for a in actions(state):
			v = min(v, max_value(successor_function(state,a)))
		return v

def alphabeta_pruning(state):
	# to be implemented
	pass

# t.fd(200)
# raw_input()

minimax_algorithm( [uf_zeroList(16), maxplayer] )