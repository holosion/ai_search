# ============================================================
# STEP 1: CREATE THE NODE CLASS
# ============================================================

class Node:
    def __init__(self, state, parent, action):
        self.state = state      # Current position in the maze
        self.parent = parent    # Previous node
        self.action = action    # Action taken to reach this node


# ============================================================
# STEP 2: CREATE THE STACK FRONTIER (DFS)
# ============================================================

class StackFrontier:

    def __init__(self):
        self.frontier = []

    # Add a node to the stack
    def add(self, node):
        self.frontier.append(node)

    # Check if a state already exists in the frontier
    def contains_state(self, state):
        for node in self.frontier:
            if node.state == state:
                return True
        return False

    # Check if the frontier is empty
    def empty(self):
        return len(self.frontier) == 0

    # Remove the last node (LIFO)
    def remove(self):

        if self.empty():
            raise Exception("Empty Frontier")

        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


# ============================================================
# STEP 3: CREATE THE MAZE CLASS
# ============================================================

class Maze:

    def __init__(self):
        self.maze = [
            "########",
            "#A     #",
            "# ###  #",
            "#   #B #",
            "########"
        ]

        self.start = None
        self.goal = None
        self.walls = []

        for i,row in enumerate(self.maze):
            for j,col in enumerate(row):
                if col == "A":
                    self.start = (i,j)
                elif col == "B":
                    self.goal = (i,j)
                elif col == "#":
                    self.walls.append((i,j))

        


    # ========================================================
    # STEP 4: GENERATE NEIGHBOURING STATES
    # ========================================================

    def neighbors(self, state):

        row, col = state

        candidates = [

            ("up",    (row - 1, col)),
            ("down",  (row + 1, col)),
            ("left",  (row, col - 1)),
            ("right", (row, col + 1))

        ]

        result =[]
#checking each candidate to see if it is a valid move (not a wall and within bounds)
        for action, (r, c) in candidates:
            if 0 <= r < len(self.maze) and 0 <= c < len(self.maze[0]) and (r,c) not in self.walls:
                result.append((action, (r,c)))
        return result


    # ========================================================
    # STEP 5: BEGIN THE DEPTH FIRST SEARCH ALGORITHM
    # ========================================================

    def solve(self):

        # Create the start node
        start = Node(
            state=self.start,
            parent=None,
            action=None
        )

        # Create the frontier
        frontier = StackFrontier()

        # Add the start node
        frontier.add(start)

        # Keep track of explored states
        explored = set()

        # Main search loop
        while True:

            # No solution exists
            if frontier.empty():
                raise Exception("No Solution")

            # Remove one node from the frontier
            node = frontier.remove()

            # ------------------------------------------------
            # GOAL TEST
            # ------------------------------------------------
            if node.state == self.goal:

                actions = []
                cells = []

                current = node

                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent

                actions.reverse()
                cells.reverse()

                return actions, cells

            # Mark the node as explored
            explored.add(node.state)

            # Expand the current node
            for action, state in self.neighbors(node.state):

                # Ignore states already explored
                # or already in the frontier
                if (
                    not frontier.contains_state(state)
                    and state not in explored
                ):

                    child = Node(
                        state=state,
                        parent=node,
                        action=action
                    )

                    frontier.add(child)