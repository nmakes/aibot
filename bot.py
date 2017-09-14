from random import randrange

#utilities

class stack:
	val = []

	def __init__():
		val = []

	def push(v):
		val.append(v)

	def pop():
		if(len(val)==0):
			return null
		else:
			return val.pop(len(val)-1)

	def __len__():
		return len(val)

# [P]ERFORMANCE
def goalTest(world, goalWorld):
	if world == goalWorld:
		return True
	else:
		return False

# agent definition
class agent:

	world = []
	state = []
	grid_X_min = 0
	grid_X_max = 9
	grid_Y_min = 0
	grid_Y_max = 9

	grid_X_size = 10
	grid_Y_size = 10

	def __init__(self, _world, _X_min=0, _X_max=9, _Y_min=0, _Y_max=9):
		self.x = (_X_max-1)*randrange(0,2) # either 0 or last
		self.y = (_Y_max-1)*randrange(0,2) # either 0 or last
		self.world = _world
		self.state = [ world, self.x, self.y ]
		self.grid_X_max = _X_max
		self.grid_X_min = _X_min
		self.grid_Y_max = _Y_max
		self.grid_Y_min = _Y_min
		self.grid_X_size = (grid_X_max - grid_X_min) + 1
		self.grid_Y_size = (grid_Y_max - grid_Y_min) + 1
		pass

# [P]ERFORMANCE
	def h1(self, subState): #subState = [[x,y], [neighbors]]
		posX, posY = subState[0]
		neighbors = subState[1]

		# 0 1 2
		# 3 4 5
		# 6 7 8

		nw = neighbors[0]
		n = neighbors[1]
		ne = neighbors[2]
		w = neighbors[3]
		curr = neighbors[4]
		e = neighbors[5]
		sw = neighbors[6]
		s = neighbors[7]
		se = neighbors[8]

		dirtCount.append(nw + n + ne)	# north (0)
		dirtCount.append(se + e + n)	# east (1)
		dirtCount.append(sw + s + se)	# south (2)
		dirtCount.append(nw + w + sw)	# west (3)
		
		maxDirtDirection = 0

		for i in range(len(dirtCount)):
			if(dirtCount[i]>dirtCount[maxDirtDirection]):
				maxDirtDirection = i

		return maxDirtDirection

# [E]NVIRONMENT

	def getWorld(self):
		return self.world # we will not use this world directly. this is only to store the DS of the world (instead of creating a global variable)

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def grid(x,y):
		return y*grid_X_size + x

# [A]CTUATORS

	def MR(self):
		if (self.x < grid_X_max):
			return grid(x+1,y)
	
	def ML(self):
		if (self.x > grid_X_min):
			return grid(x-1,y) 

	
	def MD(self):	
		if (self.y < grid_Y_max):
			return grid(x,y+1)
	
	def MU(self):
		if (self.y > grid_Y_min):
			return grid(x,y-1)

	def S(self, world):
		world[x + y*grid_X_size] = 0

	def N(self):
		pass

# [S]ENSORS

	def getUp(self):
		if(self.y==grid_Y_min):
			return null
		else:
			return (self.x + size*self.y-1)

	def getDown(self):
		if(self.y==grid_Y_max):
			return null
		else:
			return (self.x,self.y+1)

	def getLeft(self):
		if(self.x==grid_X_min):
			return null
		else:
			return (self.x-1,self.y)

	def getRight(self):
		if(self.x==grid_X_min):
			return null
		else:
			return (self.x+1,self.y)

# decision controls

	def makeUninformedMove(self, state, goalWorld, depth): # type=1
		if(world[])
		if(goalTest(goalWorld)==False && depth > 0):
			makeUninformedMove(goalWorld, getLeft(), goalWorld, depth -1)
			makeUninformedMove(goalWorld, getRight(), goalWorld, depth -1)
			makeUninformedMove(goalWorld, getUp(), goalWorld, depth -1)
			makeUninformedMove(goalWorld, getDown(), goalWorld, depth -1)

	def makeInformedMove(self, state, goalWorld):
		neighbors = []

		# 0 1 2
		# 3 4 5
		# 6 7 8

		nextMove = h1([[x,y], [neighbors]])

		moveStack.push(nextMove)

		if(goalTest(goalWorld)==False):
