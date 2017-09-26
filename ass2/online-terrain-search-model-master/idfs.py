#Name:Samip Jasani ID:2015A7PS0127P
from dirtgenerator import generatedirt
import sys
from time import time

# def get_size(obj, seen=None):
#     """Recursively finds size of objects"""
#     size = sys.getsizeof(obj)
#     if seen is None:
#         seen = set()
#     obj_id = id(obj)
#     if obj_id in seen:
#         return 0
#     # Important mark as seen *before* entering recursion to gracefully handle
#     # self-referential objects
#     seen.add(obj_id)
#     if isinstance(obj, dict):
#         size += sum([get_size(v, seen) for v in obj.values()])
#         size += sum([get_size(k, seen) for k in obj.keys()])
#     elif hasattr(obj, '__dict__'):
#         size += get_size(obj.__dict__, seen)
#     elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
#         size += sum([get_size(i, seen) for i in obj])
#     return size

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
    def __init__(self,state,parent,action,depth,cost):
        self.state = state
        self.parent=parent
        self.action=action
        self.depth = depth
        self.cost=cost
    def __repr__(self):
        return str(self.state)
 
    def __str__(self):
        return self.state

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
    if node.state in finalstates:
        return True
    else:
        return False

def solution(mynode,finalstates,numnode,maxstacksize,t0):
    solarr=[]
    cost = 0
    end= (mynode.state.row,mynode.state.col)
    while mynode.parent!=None:
        solarr.append(mynode.action)
        cost+=mynode.getcost(mynode.action)
        mynode=mynode.parent
    solarr= solarr[::-1]
    begin=(mynode.state.row,mynode.state.col)
    return (begin,end,solarr,cost,numnode,sys.getsizeof(node),maxstacksize,round(time()-t0,3))

def dls(initialstates,finalstates,matrixsize,depth,explored,numnode,t0):
    actions=["left","right","up","down"]
    stack=[]
    k=0
    z=0
    maxi=0
    for i in initialstates:
        curnode = node(i,None,None,1,0)
        if checksol(curnode,finalstates):
            print"YEs"
            return solution(curnode,finalstates,numnode,0,t0)
        stack.append(curnode)
        numnode+=1
        explored[i]=0
    while len(stack)>0 :
        maxi=len(stack) if len(stack)>maxi else maxi
        k+=1
        if(k%100000==0):
            k=0
            z+=1
            print z
        curnode = stack.pop()
        # print explored
        # print curnode.state
        act="suck"
        if curnode.check(act,matrixsize):
                childnode=node(curnode.do(act),curnode,act,curnode.depth,curnode.cost+curnode.getcost(act))
                if childnode.state not in explored:
                    if checksol(childnode,finalstates):
                        # print "Yes"
                        return solution(childnode,finalstates,numnode,maxi,t0)
                    elif (childnode.depth<=depth):
                        curnode=childnode
                        # stack.append(childnode)
                        numnode+=1
                        # explored[childnode.state]=childnode.cost  
                else:
                    if explored[childnode.state]>=childnode.cost:
                        if (childnode.depth<=depth):
                            curnode=childnode
                            # stack.append(childnode)
                            numnode+=1
                            # explored[childnode.state]=childnode.cost 
        
        for act in actions:
            # print act
            if curnode.check(act,matrixsize):
                childnode=node(curnode.do(act),curnode,act,curnode.depth+1,curnode.cost+curnode.getcost(act))
                if childnode.state not in explored:
                    if checksol(childnode,finalstates):
                        print "Yes"
                        return solution(childnode,finalstates,numnode,maxi,t0)
                    elif (childnode.depth<=depth):
                        stack.append(childnode)
                        numnode+=1
                        explored[childnode.state]=childnode.cost  
                else:
                    if explored[childnode.state]>=childnode.cost:
                        if (childnode.depth<=depth):
                            stack.append(childnode)
                            numnode+=1
                            explored[childnode.state]=childnode.cost 
                        
                # elif childnode.state not in explored:
                #     if (childnode.depth<=depth):
                #         stack.append(childnode)
                #         explored.add(childnode.state)  
    return None

def idfs(initialstates,finalstates,matrixsize):
    t0=time()
    explored={}
    depth = 1#2*len(initialstates[0].dirtylist)-1
    numnode=0
    while(True):
        print ("depth : %s"%(depth))
        result=dls(initialstates,finalstates,matrixsize,depth,explored,numnode,t0)
        if (result!=None):
            return result
        depth+=1

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
    return idfs(initialstates,finalstates,matrixsize)


if __name__=="__main__":
    matrixsize=10
    board=generatedirt(matrixsize)
    print doeverything(board,matrixsize)