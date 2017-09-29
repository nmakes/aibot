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

def humanEvent(x,y):
	pass

drawGrid("drawing", xlow, ylow, 4, 4, cellSize)

t.onscreenclick(drawBlueCircle)

raw_input()