#ID: 2015A7PS0078P
#Name: Naveen Venkat

from random import ( randrange, sample )

failure = None

# Global Constants. Can be changed during the program execution.
globalXmin = config.Xmin
globalXmax = config.Xmax
globalYmin = config.Ymin
globalYmax = config.Ymax


class World(object):

	'''
	Defines the properties of the Environment.
	
	# Environment Representation:
	-----------------------------

	The environment is pictured as a 2D matrix, of dimensions
	(xmax - xmin + 1) * (ymax - ymin + 1)

	For convenience, this is converted to a 1D list of size and used later
	(xmax - xmin + 1) * (ymax - ymin + 1)


	# State Representation:
	-----------------------

	The state is a 2-tuple. The first element of the tuple is the environment. 
	The	second element of the list is the tuple representing the position of 
	the agent as (x,y).

	'''


	def __init__(self, xmin, xmax, ymin, ymax, p=0.2):

		# Set dimensions of the world
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax

		# Define the goal
		self.goal = config.goal_world

		# Create and populate the environment
		self.world = None
		self.dirtify(p)


	def get_pos(self, x, y, xmax=None):

		# This function converts the 2D position to the 1D index in the list

		'''
		Consider the following scenario:
		
		xmin=0
		xmax=4
		ymin=0
		ymax=4

		The position (2,3) is as below:

				 x=2
			 0 1 ^ 3 4
		  0 | | | | | |
		  1 | | | | | |
		  2 | | | | | |
		y=3 | | |x| | |
		  4 | | | | | |

		This position corresponds to the index
		
		or, (xmax+1)*y + x
		= 5*3 + 3

		'''
		
		if xmax==None:
			xmax = self.xmax

		return y*(xmax+1) + x


	def is_dirty(self, x, y):
		
		# Returns true if the cell (x,y) contains dirt

		return self.world[self.get_pos(x,y)]


	def dirtify(self, p):

		# Populates random dirt (on a fraction p of the cells in the world environment)

		size = (self.xmax-self.xmin+1) * (self.ymax-self.ymin+1)

		for x in sample(range(size), int(size*p)):
			self.world[x] = True

		return self.world
		

	def clean(self, world, x, y):

		# Removes dirt from the cell (x,y)

		world[World.get_pos(x,y)] = False


	def get_goal_world(self):

		# Returns the goal world
		# Every cell in goal world is clean

		return self.goal


	def get_goal_states(self):

		#Returns the goal states

		goalStates =    [	(self.goal, (xmin,ymax)),
							(self.goal, (xmax,ymin)),
							(self.goal, (xmin,ymax)),
							(self.goal, (xmax,ymin))	]
		return goalStates


	def get_random_state(self, xmin=None, xmax=None, ymin=None, ymax=None):

		# Returns a random position

		if(xmin==None):
			xmin = self.xmin
		if(xmax==None):
			xmax = self.xmax
		if(ymin==None):
			ymin = self.ymin
		if(ymax==None):
			ymax = self.ymax

		possible_x = range(xmax-xmin+1)
		possible_y = range(ymax-ymin+1)

		return (randomWorld, (sample(possible_x,1)[0], sample(possible_y,1)[0]))


	def print_world(self):

		print "---"

		for y in range(self.ymin, self.ymax+1):
			for x in range(self.xmin, self.xmax+1):
				if self.world[self.get_pos(x,y)]:
					print 1,
				else:
					print 0,
			print

		print "---"


	def __str__(self):
		
		global globalXmin
		global globalYmin
		global globalXmax
		global globalYmax

		retStr = ""
		retStr = retStr + "xm: " + globalXmin + ", xM: " + globalXmax + ", ym: ", + globalYmin + ", yM: " + globalYmax
		return retStr


class Problem(object):

	# constructor
	def __init__(self, _initialState, _xmin=None, _xmax=None, _ymin=None, _ymax=None):

		global globalXmin
		global globalYmin
		global globalXmax
		global globalYmax

		if(_xmin==None):
			_xmin = globalXmin
			_xmax = globalXmax
			_ymin = globalYmin
			_ymax = globalYmax
		
		goalWorld = World.get_goal_world(_xmin, _xmax, _ymin, _ymax)

		self.initialState = _initialState
		self.goalStates = World.get_goal_states(goalWorld, _xmin, _xmax, _ymin, _ymax)
		self.xmin = _xmin
		self.xmax = _xmax
		self.ymin = _ymin
		self.ymin = _ymax

	# possible actions: gives the possible actions in a state (does not return the impossible actions)
	def possible_actions(self, state, _xmin=None, _xmax=None, _ymin=None, _ymax=None):

		global globalXmin
		global globalYmin
		global globalXmax
		global globalYmax

		if(_xmin==None):
			_xmin = globalXmin
			_xmax = globalXmax
			_ymin = globalYmin
			_ymax = globalYmax

		possibleActions = ['l','r','u','d','s']
		actions = []

		world = state[0]
		(x,y) = state[1]
		
		for a in possibleActions:
			if a=='l':
				if x>_xmin:
					actions.append(a)
			elif a=='r':
				if x<_xmax:
					actions.append(a)
			elif a=='u':
				if y>_ymin:
					actions.append(a)
			elif a=='d':
				if y<_ymax:
					actions.append(a)
			elif a=='s':
				if World.has_dirt(world,x,y):
					actions.append(a)

		return actions

	# successor function: gives the next state based on the action on a state
	def successor_function(self, state, action):
		world = state[0]
		(x,y) = state[1]

		if (action=='l'):
			x -= 1
		elif (action=='r'):
			x += 1
		elif (action=='u'):
			y -= 1
		elif (action=='d'):
			y += 1
		elif (action=='s'):
			World.clean(world, x,y)

		return [world, (x,y)]

	def goal_test(self, state):
		if state in self.goalStates:
			return True
		else:
			return False

	def compute_heuristic1(self, state):
		"""
		TODO

		Heuristic: number of dirt cells around the cell in the partially observable 3x3 space
		Optimization: move towards the direction with a lower value of this heuristic. 
		"""
		pass

	def compute_heuristic2(self, state):
		"""
		TODO
		
		Heuristic: number of clean cells in the surrounding cells
		Optimization: move towards the direction with a higher value of this heuristic
		"""
		pass

	def __str__(self):
		retStr = str(self.initialState) + " " + str(self.goalStates)

class TreeNode:

	def __init__(self, _state, _parent=None, _action=None):
		
		self.state = _state
		self.parent = _parent
		self.action = _action
		self.depth = 0

		if self.parent!=None:
			self.depth = self.parent.depth + 1

	def __str__(self):
		return "\nSTATE: " + str(self.state) + "\nACTION: " + str(self.action)

	def __repr__(self):
		return "\nSTATE: " + str(self.state) + "\nACTION: " + str(self.action)

	# child node: gives the child node pertaining to the given action on the state contained in the problem
	def child_node(self, problem, action):
		nextState = problem.successor_function(self.state, action)
		childNode = TreeNode(nextState, self, action)
		return childNode

	# solution resulting the path to the goal states
	def solution(self):
		mov = self
		soln = []

		while mov!=None:
			soln.append(mov.action)
			mov = mov.parent
		
		return soln[::-1]

	# T1: BFS
	def breadth_first_search(self, problem):

		node = TreeNode(problem.initialState)
		
		if problem.goal_test(node.state)==True:
			return node.solution()

		frontier = [node]
		
		exploredStates = []

		while True:

			if(len(frontier)==0):
				#print "fail"
				return failure

			node = frontier.pop(0)

			exploredStates.append(node.state)
			
			print "depth = ", node.depth
			
			for action in problem.possible_actions(node.state):
				
				child = node.child_node(problem, action)
				
				if (child.state not in exploredStates) or (child not in frontier):                    
					if problem.goal_test(child.state): 
						return child.solution()

					frontier.append(child)
