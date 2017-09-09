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