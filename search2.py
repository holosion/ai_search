# ============================================================
# STEP 1: CREATE THE NODE CLASS
# ============================================================

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# ============================================================
# STEP 2: CREATE THE STACK FRONTIER (DFS)
# ============================================================

class StackFrontier:

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

        # Find A, B and all walls
        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):

                if col == "A":
                    self.start = (i, j)

                elif col == "B":
                    self.goal = (i, j)

                elif col == "#":
                    self.walls.append((i, j))

    # ========================================================
    # STEP 4: GENERATE VALID NEIGHBOURS
    # ========================================================

    def neighbors(self, state):

        row, col = state

        candidates = [

            ("up",    (row - 1, col)),
            ("down",  (row + 1, col)),
            ("left",  (row, col - 1)),
            ("right", (row, col + 1))

        ]

        result = []

        # Keep only legal moves
        for action, (r, c) in candidates:

            if (
                0 <= r < len(self.maze)
                and
                0 <= c < len(self.maze[0])
                and
                (r, c) not in self.walls
            ):
                result.append((action, (r, c)))

        return result

    # ========================================================
    # STEP 5: DEPTH FIRST SEARCH
    # ========================================================

    def solve(self):

        start = Node(
            state=self.start,
            parent=None,
            action=None
        )

        frontier = StackFrontier()
        frontier.add(start)

        explored = set()

        while True:

            if frontier.empty():
                raise Exception("No Solution")

            node = frontier.remove()

            print(f"Exploring: {node.state}")

            # Goal Test
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

            explored.add(node.state)

            for action, state in self.neighbors(node.state):

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


# ============================================================
# STEP 6: RUN THE ALGORITHM
# ============================================================

maze = Maze()

actions, cells = maze.solve()

print("\nActions:")
print(actions)

print("\nCells:")
print(cells)