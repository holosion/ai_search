#implementing a breadth first search algorithm in python
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class QueueFrontier:
    def __init__(self):
        self.frontier = []

        def add(self, node):
            self.frontier.append(node)

        def contains_state(self, state):
            for node in self.frontier:
                if node.state == state:
                    return True

            return False

        def empty(self):
            return len(self.frontier) == 0

        def remove(self):
            if self.empty():
                raise Exception("empty frontier")

            # Remove the FIRST element -> FIFO -> BFS
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.maze = [line.strip("\n") for line in file]
            self.start = None
            self.goal = None
            self.walls = []

        # find the start(A ) and goal(B) positions in the maze and the walls
        for i,row in enumerate(self.maze):
            for j, col in enumerate(row):
                if col == "A":
                    self.start = (i, j)
                elif col == "B":
                    self.goal = (i, j)
                elif col == "#":
                    self.walls.append((i, j))

        # check if the start and goal positions were found
        if self.start is None:
            raise Exception("Start position not found in the maze")
        if self.goal is None:
            raise Exception("Goal position not found in the maze")

        #create a set of valid actions for the maze
        self.explored = set()

        # generating  valid neighbors for a given state in the maze
        def neighbors(self, state):
            row, col = state
            candidates = [
                ("up", (row -1, col)),
                ("down", (row + 1, col)),   
                ("left", (row, col - 1)),
                ("right", (row, col + 1))
            ]

            result = []

            #check if and every possible valid movements
            for action, (r, c) in candidates:
                if 0 <= r < len(self.maze) and 0 <= c < len(self.maze[0]) and (r,c) not in self.walls:
                    result.append((action, (r,c)))

                    return result

        #implementing the breadth first search algorithm to solve the maze
        def solve(self):
            #initialize the frontier with the start position
            start = Node(state=self.start, parent=None, action=None)
            frontier = QueueFrontier()
            frontier.add(start)

            #explore the maze until the goal is found or the frontier is empty
            while True:
                if frontier.empty():
                    raise Exception("No solution")

                node = frontier.remove()

                #check if the goal has been reached
                if node.state == self.goal:
                    actions = []
                    cells = []
                    while node.parent is not None:
                        actions.append(node.action)
                        cells.append(node.state)
                        node = node.parent
                    actions.reverse()
                    cells.reverse()
                    return actions, cells

                #mark the current state as explored
                self.explored.add(node.state)

                #add neighbors to the frontier
                for action, state in self.neighbors(node.state):
                    if not frontier.contains_state(state) and state not in self.explored:
                        child = Node(state=state, parent=node, action=action)
                        frontier.add(child)

                
                #implementing the goal test to check if the goal has been reached
                if node.state == self.goal:
                    actions = []
                    cells = []

                    while node.parent is not None:
                        actions.append(node.action)
                        cells.append(node.state)
                        current = current.parent  # or use current = current.parent

                    actions.reverse()
                    cells.reverse()
                    return actions, cells


                    

