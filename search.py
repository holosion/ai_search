#implementing a search algorithm for ai in python

class Node:
    def __init__(self, state,parent,action):
        self.state = state
        self.action = action
        self.parent = parent

#creating a starting point for the search algorithm
start = Node(
    state = (0,0),
    parent = None,
    action = None

)
node1 = Node(
    state = (0,1),
    parent = start,
    action = "right"
)

node2 = Node(
    state = (0,2),
    parent = node1,
    action = "right"
)
class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    #checking for an existing element wihtin the frontier
    def contains_state(self, state):
        for node in self.frontier:
            if node.state == state:
                return True
        return False

    #checking if the frontier is empty
    def empty(self):
        return not self.frontier

    #removing the las element from the frontier
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        

#def neighbors(state):
    row, col = state

    candidates=[
        ("up", (row -1, col)),
        ("down", (row +1, col)),
        ("left", (row, col -1)), 
        ("right",(row, col +1)),
    ]


class Maze:
    def __init__(self ):
        pass

    def neighbors(self, state):
        row, col = state
        candidates=[
            ("up", (row -1, col)),
            ("down", (row +1, col)),
            ("left", (row, col -1)), 
            ("right",(row, col +1)),
        ]
        return candidates


    def solve(self):
        #creating a start node for the search algorithm
        start = Node(
            state = (0,0),
            parent = None,
            action = None
        )
        #creating a frontier for the search algorithm
        frontier = StackFrontier()

        #adding the start node to the frontier
        frontier.add(start)

        #creating an explored set to keep track of the explored nodes
        explored = set()

