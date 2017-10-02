import sys

maxplayer = 1
minplayer = -1

minimaxAgentTime = 0
alphaBetaAgentTime = 0

# Minimax based analysis
R1 = 0 # number of nodes generated till the problem is solved
R2 = 0 # amount of memory allocated to one node
R3 = 0 # the maximum growth of the implicit stack
R4 = 0 # the total time to play the game
R5 = 0 # the number of nodes created in one micro second

# Alpha Beta pruning based analysis
R6 = 0 # the number of nodes generated till the problem is solved
R7 = 0 # (R1 - R6)/R1 : saving using pruning
R8 = 0 # the total time to play a game

# Comparative analysis
R9 = 0 # the memory used in both the techniques (Minimax and Alpha Beta pruning)
R10 = 0 # average time to play the game ( 10 times )
R11 = 0 # the number of times player M wins
R12 = 0 # average number of times player M wins ( repeating the step in R10 for 20 times)