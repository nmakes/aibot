"""
NAME: Naveen Venkat
ID: 2015A7PS0078P
"""

import turtle as t
from modules import *
import config

t.setup(config.guiWidth,config.guiHeight)

def initialize_gui():
	t.reset()
	t.up()
	#Set the title of the screen
	t.title("Game Engine")
	t.hideturtle()
	draw_grid(0,0,4,4)
	t.up()

def uf_zeroList(n): #Creates a list of zeroes of size n
	if verbose:
		print "uf_zeroList: ", n
	tempList = []
	for i in range(n):
		tempList.append(0)
	pass
	return tempList

t.tracer(1,0)

def draw_square(fill,X,Y,W,H):
	t.penup()
	t.setpos(X,Y)
	t.pendown()
	t.setpos(X+W,Y)
	t.setpos(X+W,Y+H)
	t.setpos(X,Y+H)
	t.setpos(X,Y)
	t.pendown()
	t.setpos(X+W,Y)

def draw_grid(X,Y,R,C,cellSize=config.cellSize):
	W = cellSize
	H = cellSize
	for y in range(R):
		for x in range(C):
			draw_square(0, X+x*W, Y+y*H, W, H)

def get_cell_center(x,y): # convert the x,y coordinates to the coordinates of the center of the corresponding cell

	xTicks = int(x/config.cellSize)
	yTicks = int(y/config.cellSize)

	if x < 0:
		centerX = xTicks*config.cellSize - config.cellSize/2
	else:
		centerX = xTicks*config.cellSize + config.cellSize/2
	
	if y < 0:
		centerY = yTicks*config.cellSize - config.cellSize/2 - config.circleRadius
	else:
		centerY = yTicks*config.cellSize + config.cellSize/2 - config.circleRadius

	return (centerX, centerY)

def draw_blue_circle(x,y): # draw blue circle at the cell center

	(centerX,centerY) = get_cell_center(x,y)
	t.penup()
	t.goto(centerX,centerY)
	t.pendown()
	t.fillcolor("blue")
	t.begin_fill()
	t.circle(config.circleRadius)
	t.end_fill()

def draw_green_circle(x,y): # draw green circle at the cell center

	(centerX,centerY) = get_cell_center(x,y)
	t.penup()
	t.goto(centerX,centerY)
	t.pendown()
	t.fillcolor("green")
	t.begin_fill()
	t.circle(config.circleRadius)
	t.end_fill()

def get_index_from_coordinates(x,y): # gets index (0 through 15) of the board cell from click coordinates

	if x > 0 and y > 0:

		xTicks = int(x/config.cellSize)
		yTicks = int(y/config.cellSize)

		row = 3 - yTicks
		col = xTicks

		if row in range(0,4) and col in range(0,4):
			return 4*row + col

	return None

def get_coordinates_from_index(Idx): # gets coordinates of the cell based 

	row = int(Idx/4)
	col = Idx % 4
	action = col + 1

	yTicks = 3 - row
	xTicks = col

	x = xTicks * config.cellSize + config.cellSize/2
	y = yTicks * config.cellSize + config.cellSize/2

	return (x,y)

def alphabeta_terminator(): # Routines to be done at the end
	config.state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 0 ]
	config.gameRunning = None
	config.abT2 = time()
	config.R8 = config.abT2 - config.abT1
	if config.R1 == 0 or config.R1 == "Not Played":
		config.R7 = "Please play minimax followed by alphabeta game"
	else:
		config.R7 = float(float((config.R1 - config.R6))/float(config.R1))

def minimax_terminator(): # 
	config.state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 0 ]
	config.gameRunning = None
	config.mmT2 = time()
	config.R4 = config.mmT2 - config.mmT1
	config.R3 = config.maxStackSize
	config.maxStackSize = 0
	config.tempStackSize = 0
	config.mmT1 = 0
	config.mmT2 = 0
	config.R5 = (float(config.R1) / float(config.minimaxAgentTime)) / 100000

def declare_winner():
	t.up()

	t.setpos(0, -50)
	if config.guiWinner == config.minplayer:
		t.write("YOU WIN!")
	elif config.guiWinner == config.maxplayer:
		t.write("YOU LOSE!")
	else:
		t.write("GAME DRAW")

def humanEvent(x,y):

	if config.gameRunning == config.alphaBetaGame:
		
		Idx = get_index_from_coordinates(x,y)

		if Idx is not None:

			row = int(Idx/4)
			col = Idx % 4
			action = col + 1

			# print "row,col = ", row,col

			# print "state:"
			# print config.state
			# print "freeIdx: ", get_ith_column_free_cell_index(config.state[0], col)

			if (Idx in range(0,16)) and (Idx == get_ith_column_free_cell_index(config.state[0], col)):

				# print "!!! CORRECT !!!"
				draw_blue_circle(x,y)

				# human plays
				config.state = successor_function(config.state, action)

				if(terminal_test(config.state)):
					alphabeta_terminator()
					config.guiWinner = config.minplayer
					declare_winner()

				# computer plays
				prevState = config.state
				config.state = alphabeta_algorithm( config.state )

				compIdx = get_ith_column_free_cell_index(prevState[0], config.guiAction - 1)
				compRow = int(compIdx / 4)
				compCol = config.guiAction - 1

				(x,y) = get_coordinates_from_index(compRow*4 + compCol)
				draw_green_circle(x,y)

				if(terminal_test(config.state)):
					alphabeta_terminator()
					config.R11 += 1
					config.guiWinner = config.maxplayer
					declare_winner()

	elif config.gameRunning == config.miniMaxGame:
		
		Idx = get_index_from_coordinates(x,y)

		if Idx is not None:

			row = int(Idx/4)
			col = Idx % 4
			action = col + 1

			# print "row,col = ", row,col

			# print "state:"
			# print config.state
			# print "freeIdx: ", get_ith_column_free_cell_index(config.state[0], col)

			if (Idx in range(0,16)) and (Idx == get_ith_column_free_cell_index(config.state[0], col)):

				# print "!!! CORRECT !!!"
				draw_blue_circle(x,y)

				# human plays
				config.state = successor_function(config.state, action)

				if(terminal_test(config.state)):
					minimax_terminator()
					config.guiWinner = config.minplayer
					declare_winner()

				# computer plays
				prevState = config.state
				config.state = minimax_algorithm( config.state )

				compIdx = get_ith_column_free_cell_index(prevState[0], config.guiAction - 1)
				compRow = int(compIdx / 4)
				compCol = config.guiAction - 1

				(x,y) = get_coordinates_from_index(compRow*4 + compCol)
				draw_green_circle(x,y)

				if(terminal_test(config.state)):
					minimax_terminator()
					config.R11 += 1
					config.guiWinner = config.maxplayer
					declare_winner()

def gui_print_board():
	initialize_gui()

def play_gui_alphabeta_game():

	config.alphaBetaAgentTime = 0
	config.R6 = 0 # the number of nodes generated till the problem is solved
	config.R7 = 0 # (R1 - R6)/R1 : saving using pruning
	config.R8 = 0 # the total time to play a game

	initialize_gui()

	config.gameRunning = config.alphaBetaGame
	config.state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1 ]
	config.abT1 = time()
	
	# computer plays
	prevState = config.state
	config.state = alphabeta_algorithm( config.state )

	compIdx = get_ith_column_free_cell_index(prevState[0], config.guiAction - 1)
	compRow = int(compIdx / 4)
	compCol = config.guiAction - 1

	(x,y) = get_coordinates_from_index(compRow*4 + compCol)
	draw_green_circle(x,y)


def play_gui_minimax_game():

	config.R1 = 0 # number of nodes generated till the problem is solved
	config.R2 = 0 # amount of memory allocated to one node
	config.R3 = 0 # the maximum growth of the implicit stack
	config.R4 = 0 # the total time to play the game
	config.R5 = 0 # the number of nodes created in one micro second
	config.minimaxAgentTime = 0

	initialize_gui()

	config.gameRunning = config.miniMaxGame
	config.state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1 ]
	config.mmT1 = time()

	config.R2 = getsizeof(TreeNode)

	# computer plays
	# prevState = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1 ]
	# config.state = [ [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], -1 ]
	# config.guiAction = 1

	prevState = config.state
	config.state = minimax_algorithm( config.state )

	compIdx = get_ith_column_free_cell_index(prevState[0], config.guiAction - 1)
	compRow = int(compIdx / 4)
	compCol = config.guiAction - 1

	(x,y) = get_coordinates_from_index(compRow*4 + compCol)
	draw_green_circle(x,y)


def gui_menu():

	if config.neat:
		uf_neatScreen()

	print
	print "Menu"
	print "----"
	print "1. Display empty board"
	print "2. Play the game using Minimax algorithm"
	print "3. Play the game using Alpha Beta pruning"
	print "4. Show all results (R1 - R12)"
	print "5. Exit"

def gui_publish_stats():

	initialize_gui()

	if config.publishPreCalculatedValues:
		config.R1 = 7251628
		config.R2 = str(896) + " Bytes" 
		config.R3 = 16
		config.R4 = str(84.4182) + " s"
		config.R5 = 0.9883
		config.R6 = 43910
		config.R7 = 0.9934
		config.R8 = str(6.42134) + " s"
		config.R9 = "minimax: " + str(16 * 896 / 1000.0) + " kB | alphabeta: " + str(16 * 896 / 1000.0) + " kB"
		config.R10 = "minimax: " + str(84.4182) + " s | alphabeta: " + str(6.4213) +" s"
		config.R11 = 10
		config.R12 = "30 times in 3 sets of 10 games"

	yPlacement = 40

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("Minimax based analysis:-", False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("------------------------", False, "left")
	yPlacement += 20


	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R1 (number of nodes generated) = " + str(config.R1), False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R2 (memory allocated to one node) = " + str(config.R2), False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R3 (maximum growth of the implicit stack) = " + str(config.R3), False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R4 (total time to play the game) = " + str(config.R4), False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R5 (nodes created per micro sec) = " + str(config.R5), False, "left")
	yPlacement += 80

	# Alpha Beta Pruning based stats

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("Alpha Beta pruning based analysis:-", False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("------------------------", False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R6 (number of nodes generated) = " + str(config.R6), False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R7 (saving using pruning) = " + str(config.R7), False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("R8 (total time to play a game) = " + str(config.R8), False, "left")
	yPlacement += 80

	# Comparative analysis

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("Comparative Analysis:-", False, "left")
	yPlacement += 20

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
	t.write("------------------------", False, "left")
	yPlacement += 20

	if not(config.publishPreCalculatedValues) and (config.R6==0 or config.R1==0 or config.R1=="Not Played" or config.R6 == "Not Played"):
		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
		t.write("Please play both the games for comparative Analysis", False, "left")		
		yPlacement += 20

	else:
		if not(config.publishPreCalculatedValues):
			config.R9 = config.R1 / config.R6
		
		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
		t.write("R9 (minimax/alphabeta) = " + str(config.R9), False, "left")
		yPlacement += 20

		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
		t.write("R10 (average time to play the game) = " + str(config.R10), False, "left")
		yPlacement += 20

		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
		t.write("R11 (number of times player M wins) = " + str(config.R11), False, "left")
		yPlacement += 20

		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-yPlacement )
		t.write("R12 (average number of times player M wins) = " + str(config.R12), False, "left")
		yPlacement += 20

t.onscreenclick(humanEvent)