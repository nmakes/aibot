#ID: 2015A7PS0078P
#Name: Naveen Venkat

from random import ( randrange, sample )

failure = None

globalXmin = 0
globalXmax = 0
globalYmin = 0
globalYmax = 0

class World(object):

    @staticmethod 
    def set_global_limits(xmin, xmax, ymin, ymax):
        global globalXmin
        global globalYmin
        global globalXmax
        global globalYmax

        globalXmin = xmin
        globalXmax = xmax
        globalYmin = ymin
        globalYmax = ymax        

    @staticmethod
    def get_pos(x,y,xmax=None):

        global globalXmax

        if xmax==None:
            xmax = globalXmax

        return y*xmax + x

    @staticmethod
    def has_dirt(world,x,y):
        return world[World.get_pos(x,y)]

    @staticmethod
    def clean(world,x,y):
        world[World.get_pos(x,y)] = False

    @staticmethod
    def get_goal_world(xmin=None, xmax=None, ymin=None, ymax=None):

        global globalXmin
        global globalYmin
        global globalXmax
        global globalYmax

        if(xmin==None):
            xmin = globalXmin
            xmax = globalXmax
            ymin = globalYmin
            ymax = globalYmax

        goalWorld = []
        for x in range(xmax+1):
            for y in range(ymax+1):
                goalWorld.append(False)
        return goalWorld

    @staticmethod
    def get_random_world(p=.2, xmin=None, xmax=None, ymin=None, ymax=None):

        global globalXmin
        global globalYmin
        global globalXmax
        global globalYmax

        if(xmin==None):
            xmin = globalXmin
            xmax = globalXmax
            ymin = globalYmin
            ymax = globalYmax

        randomWorld = []
        #print globalXmin, globalXmax, globalYmin, globalYmax
        size = (xmax-xmin+1) * (ymax-ymin+1)
        
        for _ in range( size ):
            randomWorld.append(False)

        for x in sample(range( size ), int(size*p)):
            randomWorld[x] = True

        return randomWorld

    @staticmethod
    def get_goal_states(goalWorld, xmin=None, xmax=None, ymin=None, ymax=None):

        global globalXmin
        global globalYmin
        global globalXmax
        global globalYmax

        if(xmin==None):
            xmin = globalXmin
            xmax = globalXmax
            ymin = globalYmin
            ymax = globalYmax

        goalStates =    [                             \
                            [goalWorld, (xmin,ymax)], \
                            [goalWorld, (xmax,ymin)], \
                            [goalWorld, (xmin,ymax)], \
                            [goalWorld, (xmax,ymin)]  \
                        ]
        return goalStates

    @staticmethod
    def get_random_state(randomWorld, xmin=None, xmax=None, ymin=None, ymax=None):

        global globalXmin
        global globalYmin
        global globalXmax
        global globalYmax

        if(xmin==None):
            xmin = globalXmin
            xmax = globalXmax
            ymin = globalYmin
            ymax = globalYmax

        return [randomWorld, (sample([xmin,xmax],1)[0], sample([ymax,ymin],1)[0])]

    @staticmethod
    def print_world(world, xmin=None, xmax=None, ymin=None, ymax=None):

        global globalXmin
        global globalYmin
        global globalXmax
        global globalYmax

        if(xmin==None):
            xmin = globalXmin
            xmax = globalXmax
            ymin = globalYmin
            ymax = globalYmax

        print "---"

        for y in range(ymin, ymax+1):
            for x in range(xmin, xmax+1):
                if world[World.get_pos(x,y)]:
                    print 1,
                else:
                    print 0,
            print ""

        print "---"

    def __str__(self):
        retStr = ""
        retStr = retStr + "xm: " + globalXmin + ", xM: " + globalXmax + ", ym: ", + globalYmin + ", yM: " + globalYmax
        return retStr


class Problem(object):

    # constructor
    def __init__(self, _initialState, _xmin=globalXmin, _xmax=globalXmax, _ymin=globalYmin, _ymax=globalYmax):
        
        goalWorld = World.get_goal_world(_xmin, _xmax, _ymin, _ymax)

        self.initialState = _initialState
        self.goalStates = World.get_goal_states(goalWorld, _xmin, _xmax, _ymin, _ymax)
        self.xmin = _xmin
        self.xmax = _xmax
        self.ymin = _ymin
        self.ymin = _ymax

    # possible actions: gives the possible actions in a state (does not return the impossible actions)
    def possible_actions(self, state, _xmin=globalXmin, _xmax=globalXmax, _ymin=globalYmin, _ymax=globalYmax):
        possibleActions = ['l','r','u','d','s']
        actions = []

        world = state[0]
        (x,y) = state[1]
        
        for a in possibleActions:
            if a=='l':
                if x>_xmin:
                    actions.append(a)
            elif a=='r':
                if x<_xmax:
                    actions.append(a)
            elif a=='u':
                if y>_ymin:
                    actions.append(a)
            elif a=='d':
                if y<_ymax:
                    actions.append(a)
            elif a=='s':
                if World.has_dirt(world,x,y):
                    actions.append(a)

        return actions

    # successor function: gives the next state based on the action on a state
    def successor_function(self, state, action):
        world = state[0]
        (x,y) = state[1]

        if (action=='l'):
            x -= 1
        elif (action=='r'):
            x += 1
        elif (action=='u'):
            y -= 1
        elif (action=='d'):
            y += 1
        elif (action=='s'):
            World.clean(world, x,y)

        return [world, (x,y)]

    def goal_test(self, state):
        if state in self.goalStates:
            return True
        else:
            return False

    def compute_heuristic1(self, state):
        """
        TODO

        Heuristic: number of dirt cells around the cell in the partially observable 3x3 space
        Optimization: move towards the direction with a lower value of this heuristic. 
        """
        pass

    def compute_heuristic2(self, state):
        """
        TODO
        
        Heuristic: number of clean cells in the surrounding cells
        Optimization: move towards the direction with a higher value of this heuristic
        """
        pass

    def __str__(self):
        retStr = str(self.initialState) + " " + str(self.goalStates)

class TreeNode:

    def __init__(self, _state, _parent=None, _action=None):
        
        self.state = _state
        self.parent = _parent
        self.action = _action
        self.depth = 0

        if self.parent!=None:
            self.depth = self.parent.depth + 1

    def __str__(self):
        return "\nSTATE: " + str(self.state) + "\nACTION: " + str(self.action)

    def __repr__(self):
        return "\nSTATE: " + str(self.state) + "\nACTION: " + str(self.action)

    # child node: gives the child node pertaining to the given action on the state contained in the problem
    def child_node(self, problem, action):
        nextState = problem.successor_function(self.state, action)
        childNode = TreeNode(nextState, self, action)
        return childNode

    # solution resulting the path to the goal states
    def solution(self):
        mov = self
        soln = []

        while mov!=None:
            soln.append(mov.action)
            mov = mov.parent
        
        return soln[::-1]

    # T1: BFS
    def breadth_first_search(self, problem):

        node = TreeNode(problem.initialState)
        
        if problem.goal_test(node.state)==True:
            return node.solution()

        frontier = []

        frontier.append(node)
        exploredStates = []

        while True:

            if(len(frontier)==0):
                return failure

            node = frontier.pop(0)

            exploredStates.append(node.state)
            
            for action in problem.possible_actions(node.state):
                
                child = node.child_node(problem, action)
                
                if (child.state not in exploredStates) or (child not in frontier):                    
                    if problem.goal_test(child.state): 
                        return child.solution()

                    frontier.append(child)
