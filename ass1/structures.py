from random import ( randrange, sample )

failure = None

class World(object):

    globalXmin = 0
    globalXmax = 1
    globalYmin = 0
    globalYmax = 1

    @staticmethod
    def get_pos(x,y,xmax=globalXmax):
        return y*xmax + x

    @staticmethod
    def has_dirt(world,x,y):
        return world[World.get_pos(x,y)]

    @staticmethod
    def clean(world,x,y):
        world[World.get_pos(x,y)] = False

    @staticmethod
    def get_goal_world(xmin=globalXmin, xmax=globalXmax, ymin=globalYmin, ymax=globalYmax):
        goalWorld = []
        for x in range(xmax+1):
            for y in range(ymax+1):
                goalWorld.append(False)
        return goalWorld

    @staticmethod
    def get_random_world(p=.2, xmin=globalXmin, xmax=globalXmax, ymin=globalYmin, ymax=globalYmax):
        randomWorld = []
        size = (xmax-xmin+1) * (ymax-ymin+1)
        
        for _ in range( size ):
            randomWorld.append(False)

        for x in sample(range( size ), int(size*p)):
            randomWorld[x] = True

        return randomWorld

    @staticmethod
    def get_goal_states(goalWorld, xmin=globalXmin, xmax=globalXmax, ymin=globalYmin, ymax=globalYmax):
        goalStates =    [                             \
                            [goalWorld, (xmin,ymax)], \
                            [goalWorld, (xmax,ymin)], \
                            [goalWorld, (xmin,ymax)], \
                            [goalWorld, (xmax,ymin)]  \
                        ]
        return goalStates

    @staticmethod
    def get_random_state(randomWorld, xmin=globalXmin, xmax=globalXmax, ymin=globalYmin, ymax=globalYmax):
        return [randomWorld, (sample([xmin,xmax],1)[0], sample([ymax,ymin],1)[0])]

    @staticmethod
    def print_world(world, xmin=globalXmin, xmax=globalXmax, ymin=globalYmin, ymax=globalYmax):
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                print 

    def __str__(self):
        retStr = ""
        retStr = retStr + "xm: " + globalXmin + ", xM: " + globalXmax + ", ym: ", + globalYmin + ", yM: " + globalYmax
        return retStr

class Queue(object):

    def __init__(self, queueObjects=[]):
        if type(queueObjects!=list):
            queueObjects = [queueObjects]
        self.queue = queueObjects

    def insert(self, v):
        self.queue.append(v)

    def pop(self):
        if len(self.queue)>0:
            return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue)<=0

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)

    def __iter__(self):
        return iter(self.queue)

class Problem(object):

    # constructor
    def __init__(self, _initialState, _xmin=World.globalXmin, _xmax=World.globalXmax, _ymin=World.globalYmin, _ymax=World.globalYmax):
        
        goalWorld = World.get_goal_world(_xmin, _xmax, _ymin, _ymax)

        self.initialState = _initialState
        self.goalStates = World.get_goal_states(goalWorld, _xmin, _xmax, _ymin, _ymax)
        self.xmin = _xmin
        self.xmax = _xmax
        self.ymin = _ymin
        self.ymin = _ymax

    # possible actions: gives the possible actions in a state (does not return the impossible actions)
    def possible_actions(self, state, _xmin=World.globalXmin, _xmax=World.globalXmax, _ymin=World.globalYmin, _ymax=World.globalYmax):
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
        print "gt1"
        if state in self.goalStates:
            print "gt2"
            return True
        else:
            print "gt3"
            return False

    def compute_heuristic1(self, state):
        """search in other three quadrants"""
        pass

    def compute_heuristic2(self, state):
        """TODO: move in the direction you came towards"""
        pass

    def __str__(self):
        retStr = str(self.initialState) + " " + str(self.goalStates)

class TreeNode:

    def __init__(self, _state, _parent=None, _action=None, _path_cost=0):
        
        self.state = _state
        self.parent = _parent
        self.action = _action
        self.path_cost = _path_cost
        self.depth = 0

        if self.parent!=None:
            self.depth = self.parent.depth + 1

    def child_node(self, problem, action):
        nextState = problem.successor_function(self.state, action)
        childNode = TreeNode(nextState, self, action)
        return childNode

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        mov = self
        soln = []

        while mov!=None:
            soln.append(mov.action)
            mov = mov.parent
        
        #return soln
        return soln[::-1]

    def breadth_first_search(self, problem):

        node = TreeNode(problem.initialState)
        print "bfs1"
        
        if problem.goal_test(node.state)==True:
            print "bfs2"
            return node.solution()

        print "bfs3"

        frontier = []
        print node.state
        print node.parent
        frontier.append(node)
        #exploredStates = set()
        exploredStates = []

        print "LEN: ", len(frontier)
        print "bfs4"
        #print frontier

        while True:
            print "---"

            if(len(frontier)==0):
                print "bfs5.5"
                return failure

            node = frontier.pop(0)
            
            #print node

            exploredStates.append(node.state)
            
            #print "bfs8"
            #print exploredStates

            for action in problem.possible_actions(node.state):
                print "bfs9", action            
                child = node.child_node(problem, action)
                #print child
                if (child.state not in exploredStates) or (child not in frontier):
                    print "bfs10"
                    if problem.goal_test(child.state):
                        return child.solution()
                    frontier.append(child)
                    #print frontier

#---- TESTING ----

initialWorld = World.get_random_world(0.4)
print initialWorld
initialState = World.get_random_state(initialWorld)
print initialState
cleanTheRoomProblem = Problem(initialState)
#print cleanTheRoomProblem

rootNode = TreeNode(initialState)

print rootNode.breadth_first_search(cleanTheRoomProblem)