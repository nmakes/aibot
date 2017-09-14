maxDepth = 50

# world

globalXMin = 0
globalXMax = 3
globalYMin = 0
globalYMax = 3

globalWorld = [False, False, True, False, True, False, False, False, True, True, False, False, False, False, False, True]
globalGoal = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
initState = [ globalWorld, (0,0) ]
goalState = [ globalGoal, (0,0) ]

def get_world_pos(x,y):
	return y*globalXMax + x

def has_dirt(world, x, y):
	if(world[get_world_pos(x,y)]==True):
		return True
	else:
		return False

def clean_world(world, x, y):
	world[get_world_pos(x,y)] = False

def dirty_world(world, x, y):
	world[get_world_pos(x,y)] = True

def step_cost(action):
	if action=='suck':
		return 0
	else:
		return 1

def goalTest(state,goalState):
	if state==goalState:
		return True
	else:
		return False

#________________________________________________________________________________

# Tree Structure

class TreeNode(object):

	def __init__(self, _state=None, _parent=None, _action=None, _pathCost=0):
		self.state = _state
		self.parent = _parent
		self.action = _action
		self.pathCost = _pathCost
		self.l = None
		self.r = None
		self.u = None
		self.d = None
		self.s = None

#-- Utilities
	
	def possible_actions(self, _state, _xmin=globalXMin, _xmax=globalXMax, _ymin=globalYMin, _ymax=globalYMax):
		possibleActions = ['l','r','u','d','s']
		(x,y) = _state[1]
		world = _state[0]
		actions = []
		
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
				if has_dirt(world,x,y):
					actions.append(a)
		print actions
		return actions

	def successor_function(self, _state, _action, _xmin=globalXMin, _xmax=globalXMax, _ymin=globalYMin, _ymax=globalYMax):
		(x,y) = _state[1]
		world = _state[0]
		print _action
		if _action == 'left':
			if x!=globalXMin:
				x = x-1
			else:
				return None
		elif _action == 'right':
			if x!=globalXMax:
				x = x+1
			else:
				return None
		elif _action == 'up':
			if y!=globalYMin:
				y = y-1
			else:
				return None
		elif _action == 'down':
			if y!=globalYMax:
				y = y+1
		elif _action == 'suck':
			if has_dirt(world,x,y)==True:
				clean_world(world,x,y)
			else:
				return None

		return [world,(x,y)]

	def child_node(self, _state, _parent, _action):
		childState = self.successor_function(_state, _action)
		if childState==None:
			return None
		elif childState == _state:
			return None
		else:
			childNode = TreeNode(childState, _parent, _action, _parent.pathCost + step_cost(_action))
			#if childNode == _parent: # TODO: CONSIDER WHEN THE CHILD IS SAME AS NODE BECAUSE OF END POINT CONSTRAINTS
			return childNode

#-- Iterative Deepening DFS Algorithm

	def depth_limited_search(self, goalState, limit):
		return self.recursive_dls(TreeNode(self.state), goalState, maxDepth)

	def recursive_dls(self, node, goalState, limit):
		
		print " SAPOIJGPOAJSG"
		
		if limit<=0:
			print 'cutoff'
			return 'cutoff'
		elif(goalTest(node.state, goalState)):
			print "Found Solution"
			return 'TODO: return solution'
		else:
			flag = False # tracks cutoff

			print "STATES: ", possible_actions(self.state)

			for action in self.possible_actions(self.state):
				child = self.child_node(self.state, self, action)
				
				if child!=None:
					result = self.recursive_dls(child, goalState, limit-1)
				else:
					result = 'cutoff'
					flag = True

				if result=='cutoff':
					flag = True
				elif result!='failure': 
					return result

			if flag==True:
				return 'cutoff'
			else:
				return 'failure'

	def iterative_deepening_search(self, state, goalState):
		for depth in range(1):
			result = self.depth_limited_search(goalState, depth)
			if result!='cutoff':
				return result

# stack structure

class stack:
	val = []

	def __init__():
		val = []

	def push(v):
		val.append(v)

	def pop():
		if(len(val)==0):
			return None
		else:
			return val.pop(len(val)-1)

	def __len__():
		return len(val)

TreeNode(initState).iterative_deepening_search(initState, goalState)