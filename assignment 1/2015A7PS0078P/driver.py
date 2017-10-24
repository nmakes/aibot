#ID: 2015A7PS0078P
#Name: Naveen Venkat

from structures import *

print ""
print "For an N x N world with p fraction of dirt, enter the following: "
print "N:",
n = int(raw_input())
print "p (0<=p<=1):",
p = float(raw_input())

World.set_global_limits(0, n-1, 0, n-1)

initialWorld = World.get_random_world(p)
initialState = World.get_random_state(initialWorld)
cleanTheRoomProblem = Problem(initialState)
rootNode = TreeNode(initialState)

while True:
	print "1. Display the room environment"
	print "2. Find the path using (BFS)"
	print "3. Exit"

	inp = int(raw_input())

	if inp==1:
		World.print_world(initialWorld)

	elif inp==2:
		print rootNode.breadth_first_search(cleanTheRoomProblem)

	elif inp==3:
		break