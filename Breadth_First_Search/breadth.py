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

        