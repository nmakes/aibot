"""
NAME: Naveen Venkat
ID: 2015A7PS0078P
"""

# ========
# SETTINGS
# ========

verbose = False
neat = True
gui = True
suppressGuiClicks = True

guiWidth = 800
guiHeight = 600

cellSize = 60
circleRadius = 20

# ================
# GLOBAL VARIABLES
# ================

maxint = float('inf')
minint = float('-inf')
maxplayer = 1
minplayer = -1
alphaBetaGame = 10
miniMaxGame = 11
initial = 0

minimaxAgentTime = 0
alphaBetaAgentTime = 0

tempStackSize = 0
maxStackSize = 0

guiAction = None
guiWinner = None

state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 0 ]
gameRunning = None

t1 = 0

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
R10 = "TODO" # average time to play the game ( 10 times )
R11 = 0 # the number of times player M wins
R12 = 10 # average number of times player M wins ( repeating the step in R10 for 20 times)