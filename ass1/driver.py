#ID: 2015A7PS0078P
#Name: Naveen Venkat

from structures import *

print ""
print "For an N x N world with p fraction of dirt, enter the following: "
print "N: "
n = int(raw_input())
print "p (0<=p<=1): "
p = float(raw_input())

while True:
	print "1. Display the room environment"
	print "2. Find the path using T1"
	
initialWorld = World.get_random_world(p)
print initialWorld
initialState = World.get_random_state(initialWorld)
print initialState
cleanTheRoomProblem = Problem(initialState)
#print cleanTheRoomProblem

rootNode = TreeNode(initialState)

print rootNode.breadth_first_search(cleanTheRoomProblem)