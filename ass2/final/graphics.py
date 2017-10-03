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

def get_cell_center(x,y):

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

def draw_blue_circle(x,y):
	(centerX,centerY) = get_cell_center(x,y)
	t.penup()
	t.goto(centerX,centerY)
	t.pendown()
	t.fillcolor("blue")
	t.begin_fill()
	t.circle(config.circleRadius)
	t.end_fill()

def draw_red_circle(x,y):
	(centerX,centerY) = get_cell_center(x,y)
	t.penup()
	t.goto(centerX,centerY)
	t.pendown()
	t.fillcolor("red")
	t.begin_fill()
	t.circle(config.circleRadius)
	t.end_fill()

def get_index_from_coordinates(x,y):

	if x > 0 and y > 0:

		xTicks = int(x/config.cellSize)
		yTicks = int(y/config.cellSize)

		row = 3 - yTicks
		col = xTicks

		if row in range(0,4) and col in range(0,4):
			return 4*row + col

	return None

def get_coordinates_from_index(Idx):

	row = int(Idx/4)
	col = Idx % 4
	action = col + 1

	yTicks = 3 - row
	xTicks = col

	x = xTicks * config.cellSize + config.cellSize/2
	y = yTicks * config.cellSize + config.cellSize/2

	return (x,y)


# config.state = [ [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], -1 ]
# (x,y) = get_coordinates_from_index(0)
# draw_red_circle( x,y )

def terminator():
	config.state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 0 ]
	config.gameRunning = None

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
					terminator()
					config.guiWinner = config.minplayer
					declare_winner()

				# computer plays
				prevState = config.state
				config.state = alphabeta_algorithm( config.state )

				compIdx = get_ith_column_free_cell_index(prevState[0], config.guiAction - 1)
				compRow = int(compIdx / 4)
				compCol = config.guiAction - 1

				(x,y) = get_coordinates_from_index(compRow*4 + compCol)
				draw_red_circle(x,y)

				if(terminal_test(config.state)):
					terminator()
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
					terminator()
					config.guiWinner = config.minplayer
					declare_winner()

				# computer plays
				prevState = config.state
				config.state = minimax_algorithm( config.state )

				compIdx = get_ith_column_free_cell_index(prevState[0], config.guiAction - 1)
				compRow = int(compIdx / 4)
				compCol = config.guiAction - 1

				(x,y) = get_coordinates_from_index(compRow*4 + compCol)
				draw_red_circle(x,y)

				if(terminal_test(config.state)):
					terminator()
					config.guiWinner = config.maxplayer
					declare_winner()

def gui_print_board():
	initialize_gui()

def play_gui_alphabeta_game():

	initialize_gui()

	config.gameRunning = config.alphaBetaGame
	config.state = state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1 ]
	
	# computer plays
	config.state = alphabeta_algorithm( config.state )

	compIdx = get_ith_column_free_cell_index(config.state[0], config.guiAction - 1)
	compRow = int(compIdx / 4) - 1
	compCol = config.guiAction - 1

	(x,y) = get_coordinates_from_index(compRow*4 + compCol)
	draw_red_circle(x,y)


def play_gui_minimax_game():

	config.t1 = time()
	config.R2 = getsizeof(TreeNode)

	initialize_gui()

	config.gameRunning = config.miniMaxGame
	config.state = state = [ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1 ]

	# computer plays
	config.state = minimax_algorithm( config.state )

	compIdx = get_ith_column_free_cell_index(config.state[0], config.guiAction - 1)
	compRow = int(compIdx / 4) - 1
	compCol = config.guiAction - 1

	(x,y) = get_coordinates_from_index(compRow*4 + compCol)
	draw_red_circle(x,y)


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

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-40 )
	t.write("Minimax based analysis:-", False, "left")

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-60 )
	t.write("R1 (number of nodes generated) = " + str(config.R1), False, "left")
	
	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-80 )
	t.write("R2 (memory allocated to one node) = " + str(config.R2), False, "left")
	
	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-100 )
	t.write("R3 (maximum growth of the implicit stack) = " + str(config.R3), False, "left")
	
	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-120 )
	t.write("R4 (total time to play the game) = " + str(config.R4), False, "left")
	
	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-140 )
	t.write("R5 (number of nodes created in one micro second) = " + str(config.R5), False, "left")

	# Alpha Beta Pruning based stats

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-180 )
	t.write("Alpha Beta pruning based analysis:-", False, "left")

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-200 )
	t.write("R6 (number of nodes generated) = " + str(config.R6), False, "left")

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-220 )
	t.write("R7 (saving using pruning) = " + str(config.R7), False, "left")

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-240 )
	t.write("R8 (total time to play a game) = " + str(config.R8), False, "left")

	# Comparative analysis

	t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-280 )
	t.write("Comparative Analysis:-", False, "left")

	if config.R6==0 or R1==0:
		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-300 )
		t.write("Please play both the games for comparative Analysis", False, "left")		
	
	else:
		config.R9 = config.R1 / config.R6
		
		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-300 )
		t.write("R9 (minimax/alphabeta) = " + str(config.R9), False, "left")

		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-320 )
		t.write("R10 (average time to play the game) = " + str(config.R10), False, "left")

		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-340 )
		t.write("R11 (number of times player M wins) = " + str(config.R11), False, "left")

		t.setpos( -(config.guiWidth/2) + 20, (config.guiHeight/2)-360 )
		t.write("R12 (average number of times player M wins) = " + str(config.R12), False, "left")

t.onscreenclick(humanEvent)