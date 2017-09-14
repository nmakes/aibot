from random import randrange
from random import sample
#------------------
# WORLD DEFINITIONS
#------------------

def generateDirt(p, grid_X_min, grid_X_max, grid_Y_min, grid_Y_max):

	tempWorld = []

	size = (grid_X_max-grid_X_min+1) * (grid_Y_max-grid_Y_min+1)

	for _ in range( size ):
		tempWorld.append(0)

	for x in sample(range( size ), int(size*p)):
		tempWorld[x] = 1

	#print tempWorld

	return tempWorld