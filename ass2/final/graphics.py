import turtle as t
import time

#Set the title of the screen
t.title("My program title 1 goes here")

#Create a pen
p1 = t.Pen()
p1.hideturtle()
t.hideturtle()

#Set the colors
# p1.color("blue", "red")
# t.bgcolor("grey")

# raw_input()

# #Draw the picture
# p1.up()
# p1.pensize(3)
# p1.goto(0, -150)
# p1.down()
# p1.color("black", "yellow")
# p1.begin_fill()
# p1.circle(125)
# p1.end_fill()
# p1.up()

# raw_input()

xlow = -80
ylow = -80
cellSize = 40

t.tracer(1,0)

def drawSquare(fill,X,Y,W,H):
	t.penup()
	t.setpos(X,Y)
	t.pendown()
	t.setpos(X+W,Y)
	t.setpos(X+W,Y+H)
	t.setpos(X,Y+H)
	t.setpos(X,Y)
	t.pendown()
	t.setpos(X+W,Y)

def drawGrid(state,X,Y,R,C,cellSize):
	print state
	W = 40
	H = 40
	for y in range(R):
		for x in range(C):
			drawSquare(0, X+x*W, Y+y*H, W, H)

def getCellCenter(x,y):

	print x,y

	xTicks = int(x/40)
	yTicks = int(y/40)

	print xTicks, yTicks
	
	if x < 0:
		centerX = xTicks*40 - 20
	else:
		centerX = xTicks*40 + 20
	
	if y < 0:
		centerY = yTicks*40 - 30
	else:
		centerY = yTicks*40 + 10

	return (centerX, centerY)

def drawBlueCircle(x,y):
	(centerX,centerY) = getCellCenter(x,y)
	t.penup()
	t.goto(centerX,centerY)
	t.pendown()
	t.fillcolor("blue")
	t.begin_fill()
	t.circle(10)
	t.end_fill()

def drawRedCircle(x,y):
	(centerX,centerY) = getCellCenter(x,y)
	t.penup()
	t.goto(centerX,centerY)
	t.pendown()
	t.fillcolor("red")
	t.begin_fill()
	t.circle(10)
	t.end_fill()

humanPlayed = False

ns = None

def humanEvent(x,y):

	global ns

	drawBlueCircle(x,y)

	xTicks = int(x/40)

	if x<0:
		xTicks -= 1

	xTicks += 3

	ns = successor_function(ns, xTicks)

	(ns, compAction) = minimax_algorithm( ns )

	print ns[0]

	i = compAction - 1
	row = get_ith_column_free_cell_index(ns[0], i)
	row = 0 - row + 1
	i = i-2

	drawRedCircle(row * 40 + 10, i * 40 + 10 )

	if(terminal_test(ns)):
		print "GAME OVER"


# -------------------------------------------

drawGrid("drawing", xlow, ylow, 4, 4, cellSize)
initstate = [uf_zeroList(16),maxplayer]

# first random computer move
print "making first move..."
initstate[0][2] = 1
initstate[1] = minplayer

ns = initstate

t.onscreenclick(humanEvent)

#t.onscreenclick(humanEvent)

print "\n\n\n", ns
print "\n\n"
printBoard(ns)

raw_input("TYPE ANY KEY TO EXIT")