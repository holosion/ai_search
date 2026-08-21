"""Solve a text maze using depth-first search (DFS)."""

from dataclasses import dataclass
from pathlib import Path


FOLDER = Path(__file__).resolve().parent
MAZE_FILE = FOLDER / "maze.txt"
RESULTS_FILE = FOLDER / "results.txt"
Position = tuple[int, int]


@dataclass
class Node:
    """One position in the search tree."""

    state: Position
    parent: "Node | None"
    action: str | None


class StackFrontier:
    """A last-in, first-out frontier. This produces DFS behaviour."""

    def __init__(self) -> None:
        # A list used as a stack gives DFS last-in, first-out behavior.
        self.frontier: list[Node] = []

    def add(self, node: Node) -> None:
        self.frontier.append(node)

    def contains_state(self, state: Position) -> bool:
        return any(node.state == state for node in self.frontier)

    def empty(self) -> bool:
        return not self.frontier

    def remove(self) -> Node:
        if self.empty():
            raise ValueError("Cannot remove a node from an empty frontier.")
        return self.frontier.pop()


class Maze:
    """A maze where A is the start, B is the goal, and # is a wall."""

    def __init__(self, filename: Path | str) -> None:
        # Read the maze and collect the special cells used by the solver.
        self.maze = Path(filename).read_text(encoding="utf-8").splitlines()
        if not self.maze:
            raise ValueError("The maze file is empty.")

        self.start: Position | None = None
        self.goal: Position | None = None
        self.walls: set[Position] = set()

        # Scan every cell to identify the start, goal, and walls.
        for row, line in enumerate(self.maze):
            for column, character in enumerate(line):
                position = (row, column)
                if character == "A":
                    if self.start is not None:
                        raise ValueError("The maze contains more than one start point A.")
                    self.start = position
                elif character == "B":
                    if self.goal is not None:
                        raise ValueError("The maze contains more than one goal point B.")
                    self.goal = position
                elif character == "#":
                    self.walls.add(position)

        if self.start is None:
            raise ValueError("The maze does not contain a start point A.")
        if self.goal is None:
            raise ValueError("The maze does not contain a goal point B.")

        self.explored: set[Position] = set()

    def neighbors(self, state: Position) -> list[tuple[str, Position]]:
        """Return valid moves from a position in a consistent order."""
        row, column = state
        # Consider moves in a stable order so runs are reproducible.
        candidates = [
            ("up", (row - 1, column)),
            ("down", (row + 1, column)),
            ("left", (row, column - 1)),
            ("right", (row, column + 1)),
        ]

        valid_moves = []
        for action, (next_row, next_column) in candidates:
            # Each row is checked independently, so uneven maze rows work too.
            is_in_maze = (
                0 <= next_row < len(self.maze)
                and 0 <= next_column < len(self.maze[next_row])
            )
            if is_in_maze and (next_row, next_column) not in self.walls:
                valid_moves.append((action, (next_row, next_column)))

        return valid_moves

    def solve(self) -> tuple[list[str], list[Position]]:
        """Find a path from A to B using DFS and return its moves and cells."""
        if self.start is None or self.goal is None:
            raise ValueError("The maze must have a start and goal before solving.")

        # Seed the DFS frontier with the start node.
        frontier = StackFrontier()
        frontier.add(Node(state=self.start, parent=None, action=None))
        self.explored = set()

        # Pop one node at a time and add its unvisited neighbors.
        while not frontier.empty():
            node = frontier.remove()
            self.explored.add(node.state)

            if node.state == self.goal:
                return self._build_solution(node)

            for action, state in self.neighbors(node.state):
                if state not in self.explored and not frontier.contains_state(state):
                    frontier.add(Node(state=state, parent=node, action=action))

        raise ValueError("No solution exists for this maze.")

    @staticmethod
    def _build_solution(node: Node) -> tuple[list[str], list[Position]]:
        """Trace parent links from the goal node back to the start."""
        # Follow parent links backward, then reverse both result lists.
        actions: list[str] = []
        cells: list[Position] = []

        while node.parent is not None:
            if node.action is not None:
                actions.append(node.action)
            cells.append(node.state)
            node = node.parent

        actions.reverse()
        cells.reverse()
        return actions, cells

    def save_results(self, solution: list[Position], filename: Path = RESULTS_FILE) -> None:
        """Write the maze, explored cells, and final solution to a text file."""
        # Convert the path to a set for efficient rendering checks.
        solution_cells = set(solution)
        rendered_maze = []

        # Overlay explored cells and the final route on the original maze.
        for row, line in enumerate(self.maze):
            rendered_row = []
            for column, character in enumerate(line):
                position = (row, column)
                if position == self.start:
                    rendered_row.append("A")
                elif position == self.goal:
                    rendered_row.append("B")
                elif position in self.walls:
                    rendered_row.append("#")
                elif position in solution_cells:
                    rendered_row.append("*")
                elif position in self.explored:
                    rendered_row.append(".")
                else:
                    rendered_row.append(character)
            rendered_maze.append("".join(rendered_row))

        report = [
            "DEPTH-FIRST SEARCH RESULTS",
            "==========================",
            "",
            f"Start: {self.start}",
            f"Goal: {self.goal}",
            f"Explored cells: {len(self.explored)}",
            f"Solution cells: {len(solution)}",
            "",
            "LEGEND",
            "======",
            "A = Start",
            "B = Goal",
            "# = Wall",
            ". = Explored by DFS",
            "* = Final solution path",
            "",
            "DFS RESULT",
            "==========",
            *rendered_maze,
            "",
        ]
        filename.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    """Run the DFS maze solver using the folder's maze.txt file."""
    # Run the complete load, search, and report workflow.
    maze = Maze(MAZE_FILE)
    actions, cells = maze.solve()
    maze.save_results(cells)

    print("DFS completed successfully!")
    print(f"\nActions: {actions}")
    print(f"\nSolution: {cells}")
    print(f"\nExplored cells: {sorted(maze.explored)}")
    print(f"\nResults saved to: {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
