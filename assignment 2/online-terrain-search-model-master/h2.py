#Name:Samip Jasani ID:2015A7PS0127P
from dirtgenerator import generatedirt
from heapq import *
import sys
from time import time 

class mystate:
    def __init__(self,dirtylist,row,col):
        self.dirtylist = dirtylist
        self.row = row
        self.col = col 

    def __repr__(self):
        return "Row :%s Coloumn :%s List:%s"%(self.row,self.col,self.dirtylist)
 
    def __str__(self):
        return "Row :%s Coloumn :%s List:%s"%(self.row,self.col,self.dirtylist)
    
    def __eq__(self,other):
        return self.__dict__==other.__dict__

    def __ne__(self, other):
        return (not self.__eq__(other))
    
    def __hash__(self):
        return hash(self.__repr__())

class node:
    def __init__(self,state,parent,action,matrixsize,score):
        self.state = state
        self.parent = parent
        self.action = action
        self.score = score
        self.matrixsize=matrixsize

    def __repr__(self):
        return self.state
 
    def __str__(self):
        return self.state

    def check(self,action,matrixsize):
        if action == "up" and self.state.row!=0:
            return True
        elif action == "down" and self.state.row!=matrixsize:
            return True
        elif action == "left" and self.state.col!=0:
            return True
        elif action == "right" and self.state.col!=matrixsize:
            return True
        elif action == "suck" and (self.state.row,self.state.col) in self.state.dirtylist :
            return True
        else:
            return False

    def getscore(self,action):
        score=self.score
        if action == "up":
            score += 2
            if (self.state.row-1,self.state.col) in self.state.dirtylist:
                score += -self.matrixsize
            if (self.state.row-1,self.state.col-1) in self.state.dirtylist:
                score +=-1
            if (self.state.row-1,self.state.col+1) in self.state.dirtylist:
                score +=-1
        elif action == "down":
            score += 2
            if (self.state.row+1,self.state.col) in self.state.dirtylist:
                score += -self.matrixsize
            if (self.state.row+1,self.state.col-1) in self.state.dirtylist:
                score +=-1
            if (self.state.row+1,self.state.col+1) in self.state.dirtylist:
                score +=-1
        elif action == "left":
            score += 2
            if (self.state.row,self.state.col-1) in self.state.dirtylist:
                score += -self.matrixsize
            if (self.state.row+1,self.state.col-1) in self.state.dirtylist:
                score +=-1
            if (self.state.row-1,self.state.col-1) in self.state.dirtylist:
                score +=-1
        elif action == "right":
            score += 2
            if (self.state.row,self.state.col+1) in self.state.dirtylist:
                score += -self.matrixsize
            if (self.state.row+1,self.state.col+1) in self.state.dirtylist:
                score +=-1
            if (self.state.row-1,self.state.col+1) in self.state.dirtylist:
                score +=-1
        return score
            


    def do(self,action):
        if action == "up":
            return mystate(self.state.dirtylist,self.state.row-1,self.state.col)
        elif action=="down":
            return mystate(self.state.dirtylist,self.state.row+1,self.state.col)
        elif action =="left":
            return mystate(self.state.dirtylist,self.state.row,self.state.col-1)
        elif action=="right":
            return mystate(self.state.dirtylist,self.state.row,self.state.col+1)
        elif action=="suck":
            ind=self.state.dirtylist.index((self.state.row,self.state.col))
            return mystate(self.state.dirtylist[:ind]+self.state.dirtylist[ind+1:],self.state.row,self.state.col)

    def cost(self,action):
        if action == "suck":
            return 1
        else:
            return 2

def checksol(node,finalstates):
    for x in finalstates:
        if x.dirtylist==node.state.dirtylist:
            return True
        else:
            return False

def gotofinal(curnode,finalstates,matrixsize):
    row=curnode.state.row
    col=curnode.state.col
    # if(row<(matrixsize/2)):
    #     if(col<(matrixsize/2)):
    #         act=["left","up"]
    #     else:
    #         act=["right","up"]
    # else:
    #     if(col<(matrixsize/2)):
    #         act=["left","down"]
    #     else:
    #         act=["right","down"]
    step1=(col,"left") if col <matrixsize/2 else (matrixsize-col-1,"right")
    step2=(row,"up") if row <matrixsize/2 else (matrixsize-row-1,"down")
    # while(curnode.state not in finalstates):
    #     if curnode.check(act[0],matrixsize):
    #         childnode=node(curnode.do(act[0]),curnode,act[0],matrixsize,curnode.getscore(act[0]))
    #     else :
    #         childnode=node(curnode.do(act[1]),curnode,act[1],matrixsize,curnode.getscore(act[1]))
    #     curnode=childnode
    return curnode,step1,step2

def solution(mynode,finalstates,matrixsize,numnodes,t0,maxi):
    solarr=[]
    cost = 0
    # print "before"
    mynode,step1,step2 = gotofinal(mynode,finalstates,matrixsize)
    # print "after"
    for i in range(step1[0]):
        # print i
        cost+=2
        solarr.append(step1[1])
    # print solarr
    for i in range(step2[0]):
        cost+=2
        solarr.append(step2[1])
    # print solarr
    endcol=0 if step1[1]=="left" else matrixsize-1
    endrow=0 if step2[1]=="up" else matrixsize-1
    end= (endrow,endcol)
    while mynode.parent!=None:
        solarr.append(mynode.action)
        cost+=mynode.cost(mynode.action)
        mynode=mynode.parent
    solarr= solarr[::-1]
    begin=(mynode.state.row,mynode.state.col)
    return (begin,end,solarr,cost,numnodes,sys.getsizeof(node),round(time()-t0,3),maxi)

def addtodict(node,myplaces):
    if node.score in myplaces:
        myplaces[node.score].append(node)
    else:
        myplaces[node.score]=[node]

def mstparody(initialstates,finalstates,matrixsize):
    t0=time()
    k=0
    z=0
    numnodes=0
    explored=set()
    actions=["left","right","up","down"]
    scoreheap=[]
    myplaces={}
    for i in initialstates:
        x=node(i,None,None,matrixsize,0)
        if checksol(x,finalstates):
            # print "Yay"
            return solution(x,finalstates,matrixsize,0,t0,0)
        heappush(scoreheap,x.score)
        numnodes+=1
        addtodict(x,myplaces)
        explored.add(i)
    maxi=0
    while(len(scoreheap)!=0):
        maxi=len(scoreheap) if len(scoreheap)>maxi else maxi
        k+=1
        if(k%100000==0):
            k=0
            z+=1
            print ("{} lakh".format(z))
        score=heappop(scoreheap)
        # print score
        curnode=myplaces[score].pop()
        # print curnode.state
        act = "suck"
        if(curnode.check(act,matrixsize)):
            childnode=node(curnode.do(act),curnode,act,matrixsize,curnode.getscore(act))
            if childnode not in explored:
                if checksol(childnode,finalstates):
                    # print "yay"
                    return solution(childnode,finalstates,matrixsize,numnodes,t0,maxi)
                else:
                    curnode=childnode
                    # print curnode.state
                    # heappush(scoreheap,childnode.score)
                    # addtodict(childnode,myplaces)
                        # explored.add(childnode.state)
        for act in actions:
            if(curnode.check(act,matrixsize)):
                childnode=node(curnode.do(act),curnode,act,matrixsize,curnode.getscore(act))
                if childnode not in explored:
                    # if checksol(childnode,finalstates):
                    #     return solution(childnode,finalstates,matrixsize,numnodes,t0)
                    # else:
                    heappush(scoreheap,childnode.score)
                    numnodes+=1
                    addtodict(childnode,myplaces)
                                # explored.add(childnode.state)
            # frontier.sort(key=lambda x:x.score,reverse=True)

def getdirtylist(board,matrixsize):
    dirty=[]
    for i in range(matrixsize):
        for j in range(matrixsize):
            if board[i][j]==1:
                dirty.append((i,j))
    return dirty 

def doeverything(board,matrixsize):
    dirty=getdirtylist(board,matrixsize)
    initialstates=[mystate(dirty,0,0),mystate(dirty,matrixsize-1,0),mystate(dirty,0,matrixsize-1),mystate(dirty,matrixsize-1,matrixsize-1)]
    finalstates=[mystate([],0,0),mystate([],matrixsize-1,0),mystate([],0,matrixsize-1),mystate([],matrixsize-1,matrixsize-1)]
    return mstparody(initialstates,finalstates,matrixsize)


if __name__=="__main__":
    matrixsize=14
    board=generatedirt(matrixsize)
    print doeverything(board,matrixsize)