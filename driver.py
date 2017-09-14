from dirtgen import *
from demograph import *
from bot import *

X_max = 9
X_min = 0
Y_max = 9
Y_min = 0

p = 0.2

world = []
goalWorld = []

# populating goal
for i in range(X_min, X_max+1):
	for j in range(Y_min, Y_max+1):
		goalWorld.append(0) # True means dirt is there

world = generateDirt(p, X_min, X_max, Y_min, Y_max)
print L

count = 0

for i in L:
	if i==0:
		count += 1

print count

bot = agent(world, X_min, X_max, Y_min, Y_max)