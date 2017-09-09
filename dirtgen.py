from random import randrange

#------------------
# WORLD DEFINITIONS
#------------------

def generateDirt(p):
	
	for i in range(X_min, X_max+1):
		for j in range(Y_min, Y_max+1):
			world.append(randrange(0,2)==1) # True means dirt is there