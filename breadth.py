class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop()
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(0)
            return node


class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()


        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point 'A'")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one start point 'B'")


        contents = contents.splitlines() #
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # keep track of the walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    cell = contents[i][j]
                except IndexError:
                    row.append(False)
                    continue

                if cell == "A":
                    self.start = (i, j)
                    row.append(False)
                elif cell == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif cell == "#":
                    row.append(True)
                else:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def neighbours(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self, method='bfs'):
        """solves the maze using bfs or dfs"""
        start_node = Node(state=self.start, parent=None, action=None)

        if method =='bfs':
            self.frontier = QueueFrontier()
        else:
            self.frontier = StackFrontier()
        self.frontier.add(start_node)

        #initialize the explored set to keep track of the visited nodes

        self.explored = set()
        self.num_explored = 0

        while True:
            #if nonthing left in frontier, then no path exists
            if self.frontier.empty():
                raise Exception("no solution")

            #choose a node from the frontier
            node = self.frontier.remove()
            self.num_explored += 1

            #if node is goal  then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbours(node.state):
                if not self.frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    self.frontier.add(child)



        


        