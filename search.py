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
        """
        We have not yet built the real maze.

        Later we will add:
            self.start
            self.goal
            self.walls
        """
        pass


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

        # For now we return every possible move.
        # Later we'll remove moves that hit walls
        # or go outside the maze.
        return candidates


    # ========================================================
    # STEP 5: BEGIN THE DEPTH FIRST SEARCH ALGORITHM
    # ========================================================

    def solve(self):

        # Create the start node
        # (Later this will use self.start)
        start = Node(
            state=(0, 0),
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
            # Later this will work after we define self.goal
            #
            # if node.state == self.goal:
            #
            #     actions = []
            #     cells = []
            #
            #     current = node
            #
            #     while current.parent is not None:
            #         actions.append(current.action)
            #         cells.append(current.state)
            #         current = current.parent
            #
            #     actions.reverse()
            #     cells.reverse()
            #
            #     return actions, cells

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