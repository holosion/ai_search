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





