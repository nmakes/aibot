import turtle as t

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


def publishStats():

	Text_V = Text_Y

	t.penup()
	t.setpos(Text_X, Text_V)
	t.write(arg="Home = ", move=True, align="left", font=("Arial", 20, "bold"))
	t.write(arg=251, move=True, align="left", font=("Arial", 20, "normal"))

	Text_V = Text_V - Text_V_Space

	t.setpos(Text_X, Text_V)
	t.write(arg="Other Stuff = ", move=True, align="left", font=("Arial", 20, "bold"))
	t.write(arg=5613.61, move=True, align="left", font=("Arial", 20, "normal"))


t.tracer(1,0)

V_max = 800
H_max = 1366
H_padding = 50
V_padding = 50

Text_X = 20
Text_Y = V_max - 50
Text_V_Space = 50

# Set window to be 300 by 200 with the point (0, 0) as the
# lower left corner and (300, 200) as the upper right corner.

t.setup(H_max, V_max, H_padding, V_padding) #
t.setworldcoordinates(llx=0, lly=0, urx=H_max, ury=V_max)
t.hideturtle()

#Vertical divider
t.penup()
t.setpos(int(H_max/3), 0)
t.pendown()
t.setpos(int(H_max/3), V_max)

publishStats()

'''
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

'''

def shapedrawer(x, y):
	t.penup()
	# Set the position of the turtle to the clicked location.
	t.pendown()
	t.setpos(x, y)
	t.penup()

t.onscreenclick(shapedrawer)
t.mainloop()