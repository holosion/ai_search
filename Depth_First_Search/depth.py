# ============================================================
# DEPTH-FIRST SEARCH MAZE SOLVER
# Reads maze.txt and creates results.txt
# ============================================================

from pathlib import Path

FOLDER = Path(__file__).resolve().parent

# ============================================================
# STEP 1: NODE
# ============================================================

class Node:

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# ============================================================
# STEP 2: STACK FRONTIER
# This is what makes our search DFS.
# The last node added is the first node removed.
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

        # Remove the LAST element -> LIFO -> DFS
        node = self.frontier[-1]

        self.frontier = self.frontier[:-1]

        return node


# ============================================================
# STEP 3: MAZE
# ============================================================

class Maze:

    def __init__(self, filename):

        # Read the maze from the text file
        with open(filename, "r") as file:

            self.maze = [
                line.rstrip("\n")
                for line in file
            ]

        self.start = None
        self.goal = None
        self.walls = []

        # Find A, B and the walls
        for i, row in enumerate(self.maze):

            for j, col in enumerate(row):

                if col == "A":
                    self.start = (i, j)

                elif col == "B":
                    self.goal = (i, j)

                elif col == "#":
                    self.walls.append((i, j))

        # Make sure A and B actually exist
        if self.start is None:
            raise Exception("Maze does not contain a start point A")

        if self.goal is None:
            raise Exception("Maze does not contain a goal point B")

        # This will store all cells DFS explores
        self.explored = set()


    # ========================================================
    # STEP 4: GENERATE VALID NEIGHBOURS
    # ========================================================

    def neighbors(self, state):

        row, col = state

        candidates = [

            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))

        ]

        result = []

        # Check every possible movement
        for action, (r, c) in candidates:

            # 1. Is the position inside the maze?
            # 2. Is the position NOT a wall?
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
    # STEP 5: DEPTH-FIRST SEARCH
    # ========================================================

    def solve(self):

        # Create the starting node
        start = Node(
            state=self.start,
            parent=None,
            action=None
        )

        # Create the DFS frontier
        frontier = StackFrontier()

        # Add starting node
        frontier.add(start)

        # Reset explored cells
        self.explored = set()

        # Keep searching
        while True:

            # No nodes left = no solution
            if frontier.empty():
                raise Exception("No Solution")

            # Remove the LAST node
            node = frontier.remove()

            # Record that DFS visited this cell
            self.explored.add(node.state)

            # =================================================
            # GOAL TEST
            # =================================================

            if node.state == self.goal:

                actions = []
                cells = []

                current = node

                # Follow parents backwards
                while current.parent is not None:

                    actions.append(current.action)
                    cells.append(current.state)

                    current = current.parent

                # We collected the path backwards,
                # so reverse it.
                actions.reverse()
                cells.reverse()

                return actions, cells


            # =================================================
            # EXPAND THE CURRENT NODE
            # =================================================

            for action, state in self.neighbors(node.state):

                # Don't add something we already explored
                # or something already waiting in the frontier.
                if (
                    state not in self.explored
                    and not frontier.contains_state(state)
                ):

                    child = Node(
                        state=state,
                        parent=node,
                        action=action
                    )

                    frontier.add(child)


    # ========================================================
    # STEP 6: CREATE results.txt
    # ========================================================

    def save_results(self, solution):

        # Convert the solution into a set so that
        # checking whether a cell belongs to the path
        # is easy.
        solution_cells = set(solution)

        result = []

        # Go through every cell in the original maze
        for i, row in enumerate(self.maze):

            new_row = ""

            for j, character in enumerate(row):

                position = (i, j)

                # Start
                if position == self.start:
                    new_row += "A"

                # Goal
                elif position == self.goal:
                    new_row += "B"

                # Wall
                elif position in self.walls:
                    new_row += "#"

                # Final solution path
                elif position in solution_cells:
                    new_row += "*"

                # Explored by DFS but not part of final path
                elif position in self.explored:
                    new_row += "."

                # Unexplored open space
                else:
                    new_row += " "

            result.append(new_row)


        # ====================================================
        # WRITE RESULTS TO results.txt
        # ====================================================

        with open(FOLDER / "results.txt", "w") as file:

            file.write("DEPTH-FIRST SEARCH RESULTS\n")
            file.write("==========================\n\n")

            file.write(f"Start: {self.start}\n")
            file.write(f"Goal: {self.goal}\n")
            file.write(f"Explored cells: {len(self.explored)}\n")
            file.write(f"Solution cells: {len(solution)}\n\n")

            file.write("LEGEND\n")
            file.write("======\n")
            file.write("A = Start\n")
            file.write("B = Goal\n")
            file.write("# = Wall\n")
            file.write(". = Explored by DFS\n")
            file.write("* = Final solution path\n")
            file.write("  = Unexplored\n\n")

            file.write("DFS RESULT\n")
            file.write("==========\n")

            for row in result:
                file.write(row + "\n")


# ============================================================
# STEP 7: RUN THE PROGRAM
# ============================================================

maze = Maze(FOLDER / "maze.txt")

actions, cells = maze.solve()

# Display result in terminal
print("DFS completed successfully!")

print("\nActions:")
print(actions)

print("\nSolution:")
print(cells)

print("\nExplored cells:")
print(maze.explored)

# Create results.txt
maze.save_results(cells)

print("\nresults.txt has been created.")
