#Name:Samip Jasani ID:2015A7PS0127P
from dirtgenerator import generatedirt
import sys
from time import time
class mystate:
    def __init__(self,dirtylist,row,col):
        self.dirtylist=dirtylist
        self.row=row
        self.col=col
        
    def __repr__(self):
        return "Row :%s Coloumn :%s List:%s"%(self.row,self.col,self.dirtylist)
 
    def __str__(self):
        return "Row :%s Coloumn :%s List:%s"%(self.row,self.col,self.dirtylist)
    
    def __eq__(self,other):
        return self.__dict__==other.__dict__
    
    def __hash__(self):
        return hash(self.__repr__())


class node:
    def __init__(self,state,parent,action,cost):
        self.state = state
        self.parent=parent
        self.action=action
        self.cost=cost
        self.key=self.calkey()
    def __repr__(self):
        return str(self.state)
 
    def __str__(self):
        return self.state
    
    def calkey(self):
        key=0
        if (self.state.row,self.state.col) in self.state.dirtylist:
            key+=3
        if (self.state.row-1,self.state.col) in self.state.dirtylist:
            key+=2
        if (self.state.row+1,self.state.col) in self.state.dirtylist:
            key+=2
        if (self.state.row,self.state.col+1) in self.state.dirtylist:
            key+=2
        if (self.state.row,self.state.col-1) in self.state.dirtylist:
            key+=2
        if (self.state.row-1,self.state.col-1) in self.state.dirtylist:
            key+=1
        if (self.state.row-1,self.state.col+1) in self.state.dirtylist:
            key+=1
        if (self.state.row+1,self.state.col-1) in self.state.dirtylist:
            key+=1       
        if (self.state.row+1,self.state.col+1) in self.state.dirtylist:
            key+=1        
        # for i in range(-1,2):
        #     for j in range(-1,2):
        #         if (self.state.row+i,self.state.col+j) in self.state.dirtylist:
        #             key+=1
        # if (self.state.row+i,self.state.col+j) in self.state.dirtylist:
        #     key+=1
        return key

    def check(self,action,matrixsize):
        if action == "up" and self.state.row!=0:
            return True
        elif action == "down" and self.state.row!=matrixsize-1:
            return True
        elif action == "left" and self.state.col!=0:
            return True
        elif action == "right" and self.state.col!=matrixsize-1:
            return True
        elif action == "suck" and (self.state.row,self.state.col) in self.state.dirtylist :
            return True
        else:
            return False

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

    def getcost(self,action):
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
    if(row<(matrixsize/2)):
        if(col<(matrixsize/2)):
            act=["left","up"]
        else:
            act=["right","up"]
    else:
        if(col<(matrixsize/2)):
            act=["left","down"]
        else:
            act=["right","down"]
    while(curnode.state not in finalstates):
        if curnode.check(act[0],matrixsize):
            childnode=node(curnode.do(act[0]),curnode,act[0],curnode.cost+curnode.getcost(act[0]))
        else :
            childnode=node(curnode.do(act[1]),curnode,act[1],curnode.cost+curnode.getcost(act[1]))
        curnode=childnode
    return curnode

def solution(mynode,finalstates,matrixsize,numnodes,t0,maxi):
    solarr=[]
    cost = 0
    mynode = gotofinal(mynode,finalstates,matrixsize)
    end= (mynode.state.row,mynode.state.col)
    while mynode.parent!=None:
        solarr.append(mynode.action)
        cost+=mynode.getcost(mynode.action)
        mynode=mynode.parent
    solarr= solarr[::-1]
    begin=(mynode.state.row,mynode.state.col)
    return (begin,end,solarr,cost,numnodes,sys.getsizeof(node),round(time()-t0,3),maxi)

def greedy(initialstates,finalstates,matrixsize):
    t0=time()
    numnodes=0
    explored={}
    actions=["left","right","up","down"]
    stack=[]
    k=0
    z=0
    # childnodes= sorted(childnodes, key=lambda x: x.key,reverse=True)
    #     print "going in array"
    #     for child in childnodes:
    #         print child.key
    #         stack.append(childnode)
    #         explored[childnode.state]=childnode.cost 
    childnodes=[]
    for i in initialstates:
        curnode = node(i,None,None,0)
        if checksol(curnode,finalstates):
            return solution(curnode,finalstates,matrixsize,0,t0,0)
        childnodes.append(curnode)
    childnodes= sorted(childnodes, key=lambda x: x.key,reverse=False)
    # print "going in array"
    for childnode in childnodes:
        # print childnode.key
        stack.append(childnode)
        numnodes+=1
        explored[childnode.state]=childnode.cost 
    maxi=0
    while len(stack)>0 :
        maxi=len(stack) if len(stack)>maxi else maxi
        k+=1
        if(k%100000==0):
            k=0
            z+=1
            print z
        curnode = stack.pop()
        childnodes=[]
        act = "suck"
        if curnode.check(act,matrixsize):
                childnode=node(curnode.do(act),curnode,act,curnode.cost+curnode.getcost(act))
                if childnode.state not in explored:
                    if checksol(childnode,finalstates):
                        return solution(childnode,finalstates,matrixsize,numnodes,t0,maxi)
                    else:
                        childnodes.append(childnode) 
                        explored[childnode.state]=childnode.cost
                else:
                    if explored[childnode.state]>=childnode.cost:
                        childnodes.append(childnode)
        else:                
            for act in actions:
                if curnode.check(act,matrixsize):
                    childnode=node(curnode.do(act),curnode,act,curnode.cost+curnode.getcost(act))
                    if childnode.state not in explored:
                        if checksol(childnode,finalstates):
                            return solution(childnode,finalstates,matrixsize,numnodes,t0,maxi)
                        else:
                            childnodes.append(childnode) 
                            explored[childnode.state]=childnode.cost
                    else:
                        if explored[childnode.state]>=childnode.cost:
                            childnodes.append(childnode)
        childnodes= sorted(childnodes, key=lambda x: x.key,reverse=False)
        # print "going in array"
        for childnode in childnodes:
            # print childnode.key
            stack.append(childnode)
            numnodes+=1
            explored[childnode.state]=childnode.cost 
    return None

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
    return greedy(initialstates,finalstates,matrixsize)


if __name__=="__main__":
    matrixsize=4
    board=generatedirt(matrixsize)
    print doeverything(board,matrixsize)