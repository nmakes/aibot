#Name:Samip Jasani ID:2015A7PS0127P

from dirtgenerator import generatedirt
from collections import deque

# board=generatedirtwith(5)
# dirty=[1,1]
# for i in range(10):
#     for j in range(10):
#         if board[i][j]==1:
#             dirty.append((i,j))

# print dirty
global k
global z

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

    def __ne__(self, other):
        return (not self.__eq__(other))
    
    def __hash__(self):
        return hash(self.__repr__())


class node:
    def __init__(self,state,parent,action,matrixsize):
        self.state = state
        self.parent=parent
        self.action=action

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
    # if node.state in finalstates:
    #     return True
    # else:
    #     return False
    for x in finalstates:
        if node.state.dirtylist==x.dirtylist:
            return True
        else:
            return False

def checksolclean(node,finalstates):
    if node.state in finalstates:
        return True
    else:
        return False

def solution(node,finalstates,matrixsize):
    solarr=[]
    cost = 0
    node=bfsclean(node,finalstates,matrixsize)
    end= (node.state.row,node.state.col)
    while node.parent!=None:
        solarr.append(node.action)
        cost+=node.cost(node.action)
        node=node.parent
    solarr= list(reversed(solarr))
    begin=(node.state.row,node.state.col)
    return (begin,end,solarr,cost)
    # print cost
    # return solarr

def bfsclean(curnode,finalstates,matrixsize):
    k=0
    frontier=deque()
    explored = set()
    frontier.append(curnode)
    explored.add(curnode.state)
    action=["up","down","left","right"]
    for x in frontier:
        if checksolclean(x,finalstates):
            # print "Yay"
            return x
    while(len(frontier)!=0):
        k+=1
        if(k%100000==0):
            k=0
            z+=1
            print z
        curnode=frontier.popleft()
        # print "currentstate"
        # print (curnode.state)
        explored.add(curnode.state)
        act = "suck"
        if(curnode.check(act,matrixsize)):
                childnode=node(curnode.do(act),curnode,act,matrixsize)
                # print act
                if childnode.state not in explored:
                #         pass# print "alredy present"
                # else :
                    if checksolclean(childnode,finalstates):
                            # print "Yay"
                            return childnode
                    else:
                        frontier.append(childnode)
                        explored.add(childnode.state)
                        # print "to be explored"
                       
        else:
            for act in action:
                if(curnode.check(act,matrixsize)):
                    # print act
                    childnode=node(curnode.do(act),curnode,act,matrixsize)
                    if childnode.state not in explored:
                    #     # print "alredy present"
                    # else :
                        if checksolclean(childnode,finalstates):
                            # print "Yay"
                            return childnode
                        else:
                            frontier.append(childnode)
                            explored.add(childnode.state)
                            # print "to be explored"

def bfs(initialstates,finalstates,matrixsize):
    k=0
    z=0
    frontier=deque()
    explored = set()
    for i in initialstates:
        frontier.append(node(i,None,None,matrixsize))
        explored.add(i)
    action=["up","down","left","right"]
    for x in frontier:
        if checksol(x,finalstates):
            # print "Yay"
            return solution(x,finalstates,matrixsize)
    while(len(frontier)!=0):
        k+=1
        if(k%100000==0):
            k=0
            z+=1
            print z
            print "{} nodes".format(len(frontier))
        curnode=frontier.popleft()
        # print "currentstate"
        # print (curnode.state)
        # explored.add(curnode.state)
        act = "suck"
        if(curnode.check(act,matrixsize)):
                childnode=node(curnode.do(act),curnode,act,matrixsize)
                # print act
                if childnode.state not in explored:
                #         pass# print "alredy present"
                # else :
                    if checksol(childnode,finalstates):
                            # print "Yay"
                            return solution(childnode,finalstates,matrixsize)
                    else:
                        frontier.append(childnode)
                        explored.add(childnode.state)
                        # print "to be explored"
                       
        else:
            for act in action:
                if(curnode.check(act,matrixsize)):
                    # print act
                    childnode=node(curnode.do(act),curnode,act,matrixsize)
                    if childnode.state not in explored:
                    #     # print "alredy present"
                    # else :
                        if checksol(childnode,finalstates):
                            # print "Yay"
                            return solution(childnode,finalstates,matrixsize)
                        else:
                            frontier.append(childnode)
                            explored.add(childnode.state)
                            # print "to be explored"

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
    return bfs(initialstates,finalstates,matrixsize)


if __name__=="__main__":
    matrixsize=20
    board=generatedirt(matrixsize)
    print doeverything(board,matrixsize)