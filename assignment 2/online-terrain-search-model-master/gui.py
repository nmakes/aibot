#Name:Samip Jasani ID:2015A7PS0127P
import turtle
import random
from dirtgenerator import generatedirt
from dirtgenerator import generatedirtwith
from idfs import doeverything as idfs
from bfs import doeverything as bfs
from h1 import doeverything as greedy
from h2 import doeverything as mst


def initialiseturtle():
    wn = turtle.Screen()
    # wn.screensize()  
    # wn.setup(width=1.0,height=1.0)
    wn.bgcolor("white")
    wn.title("AI Vaccum Cleaner")
    return wn

def make_partitions(wn):
    width= float(wn.window_width())
    height= float(wn.window_height())
    skk = turtle.Turtle()
    skk.ht()
    skk.speed(0)
    skk.pensize(3)
    skk.penup()
    skk.goto(width/3-width/2,-height/2)
    skk.setheading(90)
    skk.pendown()
    skk.forward(height)
    skk.penup()
    skk.goto(width/3-width/2,0)
    skk.setheading(0)
    skk.pendown()
    skk.forward(2*width/3)
    skk.penup()
    skk.goto(2*width/3-width/2,-height/2)
    skk.setheading(90)
    skk.pendown()
    skk.forward(height)
    return wn,skk

def fillp1(wn,skk):
    width= float(wn.window_width())
    height= float(wn.window_height())
    skk.penup()
    portion=height/11
    for i in range(11):
        skk.goto(-width/2,height/2-20-(i*portion))
        string=" R"+str(i+1)+" = "
        skk.write(string, True,font=("Arial", 12, "normal"))
    return skk.xcor()

def fillboard(wn,skk,xcord,ycord,i,j):
    # skk.color(random.random(),random.random(), random.random())
    width= float(wn.window_width())
    height= float(wn.window_height())
    hi=height/20
    wj=width/30
    skk.penup()
    # print (xcord,j,wj,ycord,i,hi)
    skk.goto(xcord+j*wj,ycord-i*hi)
    skk.setheading(0)
    skk.begin_fill()
    skk.pendown()
    skk.forward(wj)
    skk.right(90)
    skk.forward(hi)
    skk.right(90)
    skk.forward(wj)
    skk.right(90)
    skk.forward(hi)
    skk.right(90)
    skk.penup()
    skk.end_fill()


def fillp2(wn,skk,board,matrixsize):
    width= float(wn.window_width())
    height= float(wn.window_height())
    def makeg1andg2():
        j=width/30
        for i in range(1,21):
            skk.penup()
            skk.goto(width/3-width/2+i*j,0)
            skk.setheading(90)
            skk.pendown()
            skk.forward(height/2)
        j=height/20
        for i in range(1,11):
            skk.penup() 
            skk.goto(width/3-width/2,i*j)
            skk.setheading(0)
            skk.pendown()
            skk.forward(2*width/3)
    makeg1andg2()
    reststates=[(0,0),(0,matrixsize-1),(matrixsize-1,0),(matrixsize-1,matrixsize-1)]
    skk.pen(fillcolor="brown",pencolor="black")
    for i in reststates:
        fillboard(wn,skk,width/3-width/2,height/2,i[0],i[1])        
    for i in reststates:
        fillboard(wn,skk,2*width/3-width/2,height/2,i[0],i[1])  
    skk.pen(fillcolor="grey",pencolor="black")
    for i in range(matrixsize):
        for j in range(matrixsize):
            if board[i][j]==1:
                fillboard(wn,skk,width/3-width/2,height/2,i,j)        
    for i in range(matrixsize):
        for j in range(matrixsize):
            if board[i][j]==1:
                fillboard(wn,skk,2*width/3-width/2,height/2,i,j)     

def fillg1(bfs,wn):
    skk = turtle.Turtle()
    skk.speed(10)
    width= float(wn.window_width())
    height= float(wn.window_height())
    hi=height/20
    wj=width/30
    skk.pen(fillcolor="pink",pencolor="red",pensize=2)
    skk.penup()
    getpath(skk,width/3-width/2+bfs[0][1]*wj+.5*wj,height/2-bfs[0][0]*hi-.5*hi,bfs[2],wj,hi)

def fillg2h1(bfs,wn):
    skk = turtle.Turtle()
    skk.speed(10)
    width= float(wn.window_width())
    height= float(wn.window_height())
    hi=height/20
    wj=width/30
    skk.pen(fillcolor="light blue",pencolor="blue",pensize=2)
    skk.penup()
    getpathforg2(skk,2*width/3-width/2+bfs[0][1]*wj+.5*wj,height/2-bfs[0][0]*hi-.5*hi,bfs[2],wj,hi,hi/2)

def fillg2h2(bfs,wn):
    skk = turtle.Turtle()
    skk.speed(10)
    width= float(wn.window_width())
    height= float(wn.window_height())
    hi=height/20
    wj=width/30
    skk.pen(fillcolor="light green",pencolor="green",pensize=2)
    skk.penup()
    getpathforg2(skk,2*width/3-width/2+bfs[0][1]*wj+.5*wj,height/2-bfs[0][0]*hi-.5*hi,bfs[2],wj,hi,-hi/2)


def getpath(skk,xcord,ycord,list,wj,hi):
    skk.goto(xcord,ycord)
    for i in list:
        if i=="suck":
            skk.penup()
            skk.setheading(0)
            skk.forward(.5*wj)
            skk.right(90)
            skk.forward(.5*hi)
            skk.begin_fill()
            skk.pendown()
            skk.right(90)
            skk.forward(wj)
            skk.right(90)
            skk.forward(hi)
            skk.right(90)
            skk.forward(wj)
            skk.right(90)
            skk.forward(hi)
            skk.penup()
            skk.end_fill()
            skk.setheading(0)
            skk.back(.5*wj)
            skk.left(90)
            skk.forward(.5*hi)
        elif i=="left":
            skk.pendown()
            skk.setheading(180)
            skk.forward(wj)
        elif i=="right":
            skk.pendown()
            skk.setheading(0)
            skk.forward(wj)
        elif i=="up":
            skk.pendown()
            skk.setheading(90)
            skk.forward(hi)
        elif i=="down":
            skk.pendown()
            skk.setheading(270)
            skk.forward(hi)


def getpathforg2(skk,xcord,ycord,list,wj,hi,fillh):
    skk.goto(xcord,ycord)
    for i in list:
        if i=="suck":
            skk.penup()
            skk.setheading(0)
            skk.forward(.5*wj)
            skk.right(90)
            skk.forward(fillh if fillh > 0 else 0)
            skk.begin_fill()
            skk.pendown()
            skk.right(90)
            skk.forward(wj)
            skk.right(90)
            skk.forward(abs(fillh))
            skk.right(90)
            skk.forward(wj)
            skk.right(90)
            skk.forward(abs(fillh))
            skk.penup()
            skk.end_fill()
            skk.setheading(0)
            skk.back(.5*wj)
            skk.left(90)
            skk.forward(fillh if fillh > 0 else 0)
        elif i=="left":
            skk.pendown()
            skk.setheading(180)
            skk.forward(wj)
        elif i=="right":
            skk.pendown()
            skk.setheading(0)
            skk.forward(wj)
        elif i=="up":
            skk.pendown()
            skk.setheading(90)
            skk.forward(hi)
        elif i=="down":
            skk.pendown()
            skk.setheading(270)
            skk.forward(hi)

# def writer(num,numnodes,wn,skk,for_text_xcor):
#     width= float(wn.window_width())
#     height= float(wn.window_height())
#     skk.penup()
#     skk.goto(for_text_xcor,height/2-20)
#     string=""+str(numnodes)+" nodes"
#     skk.write(string, True,font=("Arial", 12, "normal"))
#     return
def writer(num,str,wn,skk,for_text_xcor,color):
    skk.pen(pencolor=color)
    width= float(wn.window_width())
    height= float(wn.window_height())
    skk.penup()
    skk.goto(for_text_xcor,height/2-20-(num-1)*height/11)
    string=""+str#+" nodes"
    skk.write(string, True,font=("Arial", 12, "normal"))
    return

def makeg3(skk,x,y,blue,green,space):
    skk.pensize(2)
    skk.penup()
    skk.pen(pencolor="blue")
    i=0
    # print x
    skk.goto(x,y)
    skk.pendown()
    # print skk.pos()
    for b in blue:
        skk.goto(x+i*2*space,y+b) 
        i+=1
    skk.penup()
    skk.goto(x,y)
    skk.pendown()
    skk.pen(pencolor="green")
    i=0
    for g in green:
        skk.goto(x+i*2*space,y+g)
        i+=1
    return skk


if __name__=="__main__":
    matrixsize=10
    board=generatedirt(matrixsize)
    wn=initialiseturtle()
    wn,skk=make_partitions(wn)
    skk.pensize(1)
    for_text_xcor = fillp1(wn,skk)
    fillp2(wn,skk,board,matrixsize)
    b=greedy(board,matrixsize)
    print b
    print len(b[2])
    fillg2h1(b,wn)
    writer(6,str(b[4])+" nodes",wn,skk,for_text_xcor,"blue")
    writer(7,str(b[5])+" Bytes",wn,skk,for_text_xcor,"blue")
    writer(8,str(b[3])+" cost",wn,skk,for_text_xcor,"blue")
    writer(9,str(b[6])+" seconds",wn,skk,for_text_xcor,"blue")
    writer(10.3,str(round(b[7]*float(b[5])/1024,2))+" KBytes",wn,skk,for_text_xcor,"blue")


    d=mst(board,matrixsize)
    print d
    fillg2h2(d,wn)
    writer(6.5,str(d[4])+" nodes",wn,skk,for_text_xcor,"green")
    writer(7.5,str(d[5])+" Bytes",wn,skk,for_text_xcor,"green")
    writer(8.5,str(d[3])+" cost",wn,skk,for_text_xcor,"green")
    writer(9.5,str(d[6])+" seconds",wn,skk,for_text_xcor,"green")
    writer(10.6,str(round(d[7]*float(d[5])/1024,2))+" KBytes",wn,skk,for_text_xcor,"green")

    # c=bfs(board,matrixsize)
    # print c
    # print len(c[2])
    # fillg1(c,wn)
    
    a=idfs(board,matrixsize)
    print a
    fillg1(a,wn)
    writer(1,str(a[4])+" nodes",wn,skk,for_text_xcor,"red")
    writer(2,str(a[5])+" Bytes",wn,skk,for_text_xcor,"red")    
    writer(3,str(a[6])+" nodes",wn,skk,for_text_xcor,"red")
    writer(4,str(a[3])+" cost",wn,skk,for_text_xcor,"red")
    writer(5,str(a[7])+" seconds",wn,skk,for_text_xcor,"red")
    writer(10,str(round(a[6]*float(a[5])/1024,2))+" KBytes",wn,skk,for_text_xcor,"red")
    bsum=0
    dsum=0
    asum=0
    for i in range(10):
        board=generatedirtwith(30,5)
        b=greedy(board,5)
        d=mst(board,5)
        a=idfs(board,5)
        bsum+=b[3]
        dsum+=d[3]
        asum+=a[3]
    bsum=round(float(bsum)/10,2)
    dsum=round(float(dsum)/10,2)
    asum=round(float(asum)/10,2)
    writer(11,str(asum)+" Avg Cost",wn,skk,for_text_xcor,"red")
    writer(11.3,str(bsum)+" Avg Cost",wn,skk,for_text_xcor,"blue")
    writer(11.6,str(dsum)+" Avg Cost",wn,skk,for_text_xcor,"green")


    skk.penup()
    width= float(wn.window_width())
    height= float(wn.window_height())  
    space= (width/3-10)/(18)
    x=(width/3)-width/2+5
    y=-height/2+10
    coordb=[]
    coordd=[]
    for i in range(4,21,2):
        board=generatedirtwith(100,i)
        b=greedy(board,i)
        print b
        coordb.append(40*b[6])
        d=mst(board,i)
        print d
        coordd.append(40*d[6])
    # print "this is sparta"
    # print x
    makeg3(skk,x,y,coordb,coordd,space)

    space= (width/3-10)/(20)
    x=2*(width/3)-width/2+5
    y=-height/2+10
    coordb=[]
    coordd=[]
    for i in range(10,101,10):
        board=generatedirtwith(i,8)
        b=greedy(board,8)
        print b
        coordb.append(20*b[6])
        d=mst(board,8)
        print d
        coordd.append(20*d[6])
    makeg3(skk,x,y,coordb,coordd,space)


        # pass
        # pass
        # skk.penup()
        # skk.setheading(0)
        # skk.forward(space*2)




    turtle.done()