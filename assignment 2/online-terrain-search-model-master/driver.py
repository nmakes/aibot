from gui import *

def runfull():
    matrixsize=10
    board=generatedirt(matrixsize)
    print "board generated"
    wn=initialiseturtle()
    wn,skk=make_partitions(wn)
    skk.pensize(1)
    for_text_xcor = fillp1(wn,skk)
    fillp2(wn,skk,board,matrixsize)
    print "T2 h1 started executing"
    b=greedy(board,matrixsize)
    # print b
    # print len(b[2])
    fillg2h1(b,wn)
    writer(6,str(b[4])+" nodes",wn,skk,for_text_xcor,"blue")
    writer(7,str(b[5])+" Bytes",wn,skk,for_text_xcor,"blue")
    writer(8,str(b[3])+" cost",wn,skk,for_text_xcor,"blue")
    writer(9,str(b[6])+" seconds",wn,skk,for_text_xcor,"blue")
    writer(10.3,str(round(b[7]*float(b[5])/1024,2))+" KBytes",wn,skk,for_text_xcor,"blue")
    print "T2 h2 started executing"
    d=mst(board,matrixsize)
    # print d
    fillg2h2(d,wn)
    writer(6.5,str(d[4])+" nodes",wn,skk,for_text_xcor,"green")
    writer(7.5,str(d[5])+" Bytes",wn,skk,for_text_xcor,"green")
    writer(8.5,str(d[3])+" cost",wn,skk,for_text_xcor,"green")
    writer(9.5,str(d[6])+" seconds",wn,skk,for_text_xcor,"green")
    writer(10.6,str(round(d[7]*float(d[5])/1024,2))+" KBytes",wn,skk,for_text_xcor,"green")
    print "T1 started executing"
    a=idfs(board,matrixsize)
    # print a
    fillg1(a,wn)
    writer(1,str(a[4])+" nodes",wn,skk,for_text_xcor,"red")
    writer(2,str(a[5])+" Bytes",wn,skk,for_text_xcor,"red")    
    writer(3,str(a[6])+" nodes",wn,skk,for_text_xcor,"red")
    writer(4,str(a[3])+" cost",wn,skk,for_text_xcor,"red")
    writer(5,str(a[7])+" seconds",wn,skk,for_text_xcor,"red")
    writer(10,str(round(a[6]*float(a[5])/1024,2))+" KBytes",wn,skk,for_text_xcor,"red")
    print "Calculating for R11 at 30% dirt in 5x5 Matrix"
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
    print "Generating G3 in range (4x4 to 21x21) Matrix at 100% dirt"
    for i in range(4,21,2):
        board=generatedirtwith(100,i)
        b=greedy(board,i)
        # print b
        coordb.append(40*b[6])
        d=mst(board,i)
        # print d
        coordd.append(40*d[6])
    makeg3(skk,x,y,coordb,coordd,space)
    space= (width/3-10)/(20)
    x=2*(width/3)-width/2+5
    y=-height/2+10
    coordb=[]
    coordd=[]
    print "Generating G4 in range (10 to 100)% dust in 6X6 Matrix"
    for i in range(10,101,10):
        board=generatedirtwith(i,6)
        b=greedy(board,6)
        # print b
        coordb.append(40*b[6])
        d=mst(board,6)
        # print d
        coordd.append(40*d[6])
    makeg3(skk,x,y,coordb,coordd,space)
    turtle.done()

def roomenv():
    matrixsize=10
    board=generatedirt(matrixsize)
    print "board generated"
    wn=initialiseturtle()
    wn,skk=make_partitions(wn)
    skk.pensize(1)
    for_text_xcor = fillp1(wn,skk)
    fillp2(wn,skk,board,matrixsize)
    turtle.done()

def T1():
    matrixsize=10
    board=generatedirt(matrixsize)
    i= idfs(board,matrixsize)
    print "Path Action :"
    print i[2]
    print "Path Start and End :"
    print i[0],i[1]
    print "Path Cost :"
    print i[3]
def T2():
    matrixsize=10
    board=generatedirt(matrixsize)
    i=int(raw_input("Enter 1 to run h1 and 2 for h2:"))
    if i==1:
        g= greedy(board,matrixsize)
        print "Path Action :"
        print g[2]
        print "Path Start and End :"
        print g[0],g[1] 
        print "Path Cost :"
        print g[3]
    if i==2:
        m= mst(board,matrixsize)
        print  "Path Action :"
        print m[2]
        print "Path Start and End :"
        print m[0],m[1]
        print "Path Cost :"
        print m[3]

if __name__=="__main__":
    i = int(raw_input("Option 1: Display the room environment\nOption 2: Find the path (action sequence) and path cost using T1\nOption 3: Find the path (action sequence) and path cost using T2\nOption 4: Show all results and graphs in the GUI.\n >> "))
    if i==1:
        roomenv()
    elif i==2:
        T1()
    elif i==3:
        T2()
    elif i==4:
        runfull()