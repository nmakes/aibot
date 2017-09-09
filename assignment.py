from random import randrange
import demograph
#------------------
# WORLD DEFINITIONS
#------------------

# setting world size
X_max = 9
X_min = 0
Y_max = 9
Y_min = 0

# defining world
world = []
goalWorld = []

# world properties
world_clean = False

# populating goal
for i in range(X_min, X_max+1):
	for j in range(Y_min, Y_max+1):
		goalWorld.append(0) # True means dirt is there

# populating world
for i in range(X_min, X_max+1):
	for j in range(Y_min, Y_max+1):
		world.append(randrange(0,2)==1) # True means dirt is there

# goal test
def goalTest(currentState, goalState):
	if currentState == goalState:
		world_clean = True
		return True
	else:
		world_clean = False
		return False

# agent definition
class agent:
	def __init__(self):
		self.x = (X_max-1)*randrange(0,2) # either 0 or last
		self.y = (Y_max-1)*randrange(0,2) # either 0 or last
		pass

	def MR(self):
		if (self.x < X_max):
			self.x += 1

	
	def ML(self):
		if (self.x > X_min):
			self.x -= 1

	
	def MD(self):	
		if (self.y < Y_max):
			self.y += 1

	
	def MU(self):
		if (self.y > Y_min):
			self.y -= 1

	def S(self, world):
		pass

	def N(self):
		pass

	def makeNextMove(self, world):
		br = {}
		br[up] = getUp

# creating a bot
bot = agent()

#bot.makeNextMove(world)

print world