#ID: 2015A7PS0078P
#Name: Naveen Venkat

from random import ( randrange, sample )

# Global Variables
failure = None

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
	The	second element of the list is the tuple representing the position 
	(coordinates) of the agent as (x,y).

	'''


	def __init__(self, xmin, xmax, ymin, ymax, dirt=config.defaultDirt):

		# Set dimensions of the world
		if(xmin==None):
			xmin = config.Xmin
		if xmax==None:
			xmax = config.Xmax
		if ymin==None:
			ymin = config.Ymin
		if ymax==None:
			ymax = config.Ymax

		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax

		# Define the goal
		self.goal = config.goal_world

		# Create and populate the environment
		self.world = None
		self.dirtify(dirt)


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


	def get_random_state(self, xmin=None, xmax=None, ymin=None, ymax=None):

		# Returns a state with random position in the range (xmax-xmin+1, ymax-ymin+1)

		if(xmin==None):
			xmin = self.xmin
		if(xmax==None):
			xmax = self.xmax
		if(ymin==None):
			ymin = self.ymin
		if(ymax==None):
			ymax = self.ymax

		possible_x = range(xmin, xmax+1)
		possible_y = range(ymin, ymax+1)

		return (randomWorld, (sample(possible_x,1)[0], sample(possible_y,1)[0]))


	def print_world(self):

		# Prints the world on the console

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
		
		retStr = ""
		retStr = retStr + "xm: " + self.xmin + ", xM: " + self.xmax + ", ym: ", + self.ymin + ", yM: " + self.ymax
		return retStr


class Problem(object):

	'''
	Defines the problem.
	
	# Components of a problem:
	--------------------------
	
	A problem is set in a unique 'world'. Thus it has its own unique 'goals'.
	The states are represented as given in the class World.

	'''

	# constructor
	def __init__(self, initialState, xmin=None, xmax=None, ymin=None, ymax=None, dirt=config.defaultDirt):

		# Initial and Goal Worlds
		self.world = World(xmin, xmax, ymin, ymax, dirt)
		self.goalWorld = config.goalWorld

		# Initial and Goal States
		self.initialState = initialState
		self.goalStates = self.get_goal_states()


	def get_goal_states(self):

		#Returns the goal states

		goalStates =    [	(self.goal, (xmin,ymin)),
							(self.goal, (xmin,ymax)),
							(self.goal, (xmax,ymin)),
							(self.goal, (xmax,ymax))	]
		return goalStates
		
	
	def possible_actions(self, state):

		'''
		
		This function returns the possible actions (that can be taken) in a state.

		We initialize the possibleActions list with the five actions:
		1. left
		2. right
		3. up
		4. down
		5. suck (clean the cell by sucking the dirt)

		Then, the coordinates of the agent are checked to see which moves can be performed.

		'''

		actions = []

		world = state[0] #	( From the state
		(x,y) = state[1] #    representation )
		
		if x>xmin:
			# If at least one cell is on the left
			# we can move left
			actions.append('l')

		if x<xmax:
			# If at least one cell is on the right
			# we can move right
			actions.append('r')

		if y>ymin:
			# If at least one cell is above
			# we can move up
			actions.append('u')

		if y<ymax:
			# If at least one cell is below
			# we can move down
			actions.append('d')

		if World.has_dirt(world,x,y):
			# If there is dirt in the cell
			# we can clean the dirt
			actions.append('s')

		return actions


	def successor_function(self, state, action):

		# This function returns the next state based on the action on a state

		world = state[0]
		(x,y) = state[1]

		# Change x/y/world based on the action
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

		# Return the successor state
		return [world, (x,y)]


	def goal_test(self, state):

		# Tests if the given state is the goal state

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
