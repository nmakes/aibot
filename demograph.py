import turtle as t
from random import randrange

'''
x = "p"

while(x!="x"):

	for i in range(16):
		if i%2==0:
			t.pendown()
			t.fd(5*i)
			t.right(45)
		else:
			#t.penup()
			t.fd(5*i)
			t.right(45)
'''

#default value of tracer is (1,10)
#set tracer to (0,0) for immediate transition

'''
t.setposition(100,100)
t.reset()
t.circle(200)
'''
'''
colors = ["blue", "green", "purple", "cyan", "magenta", "violet"]
t.reset()
t.tracer(0, 0)
for i in range(45):
	t.color(colors[i % 6])
	t.pendown()
	t.fd(2 + i * 5)
	t.left(45)
	t.width(i)
	t.penup()
t.update()
'''

'''
t.reset()
t.color("red")
for angle in range(0, 360, 15):
	t.seth(angle)
	t.circle(100)
'''

'''
t.reset()
t.width(0)
t.begin_fill()
t.fd(150)
t.seth(45)
t.fd(150)
t.seth(90)
t.fd(150)
t.color("blue")
t.end_fill()
x = raw_input()
'''

'''
def drawfib(n, len_ang):
	t.forward(2 * len_ang)
	if n == 0:
		pass # Do nothing.
	elif n == 1:
		pass # Do nothing.
	else:
		t.left(len_ang)
		drawfib(n - 1, len_ang)
		t.right(2 * len_ang)
		drawfib(n - 2, len_ang)
		t.left(len_ang)
	t.backward(2 * len_ang)
# Six different starting points for six different trees.
start_points = [[-300, 250], [-150, 250],[-300, 110], [-80, 110],[-300, -150], [50, -150]]
# For each starting point, draw a tree with n varying
# between 1 and 6 and len_ang set to 30.
n = 0
for start_point in start_points:
	x, y = start_point
	n = n + 1
	t.penup()
	t.setpos(x, y)
	t.pendown()
	drawfib(n, 30)
'''


# -----------
# USABLE CODE
# -----------

V_max = 800
H_max = 1366
H_padding = 50
V_padding = 50

Text_X = 20
Text_Y = V_max - 50
Text_V_Space = 50

def initScreen(H_max, V_max, H_padding, V_padding):
	
	t.tracer(1,0)
	t.setup(H_max, V_max, H_padding, V_padding) #
	t.setworldcoordinates(llx=0, lly=V_max, urx=H_max, ury=0)

def publishStats(Text_X, Text_Y, Text_V_Space, xpos, ypos):

	Text_V = Text_Y

	t.penup()
	t.setpos(Text_X, Text_V)
	t.write(arg="xpos = ", move=True, align="left", font=("Arial", 20, "bold"))
	t.write(arg=xpos, move=True, align="left", font=("Arial", 20, "normal"))

	Text_V = Text_V - Text_V_Space

	t.setpos(Text_X, Text_V)
	t.write(arg="ypos = ", move=True, align="left", font=("Arial", 20, "bold"))
	t.write(arg=ypos, move=True, align="left", font=("Arial", 20, "normal"))

def renderScreen():
	t.hideturtle()
	t.reset()

	publishStats(Text_X, Text_Y, Text_V_Space, 0,0)

	#Vertical divider
	t.penup()
	t.setpos(int(H_max/3), 0)
	t.pendown()
	t.setpos(int(H_max/3), V_max)

	# Second quadrant - horizontal
	t.penup()
	t.setpos(H_max/3, V_max/2)
	t.pendown()
	t.setpos(H_max, V_max/2)

	# Second quadrant - vertical
	t.penup()
	t.setpos(2*H_max/3, 0)
	t.pendown()
	t.setpos(2*H_max/3, V_max)

# Set window to be 300 by 200 with the point (0, 0) as the
# lower left corner and (300, 200) as the upper right corner.

def shapedrawer(x, y):
	t.penup()
	# Set the position of the turtle to the clicked location.
	t.pendown()
	t.setpos(x, y)
	xpos,ypos = t.pos()
	publishStats(Text_X, Text_Y, Text_V_Space, xpos, ypos)
	t.penup()

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

def drawGrid(state,X,Y,R,C,W=40,H=40):
	print state
	for y in range(R):
		for x in range(C):
			drawSquare(0, X+x*W, Y+y*H, W, H)

initScreen(H_max, V_max, H_padding, V_padding)

renderScreen()

# drawGrid(0,-V_max/12,H_max/3,0,10,10)

# t.onscreenclick(shapedrawer)

t.setpos(0,0)

t.mainloop()