"""Solve breadth.txt with breadth-first search (BFS)."""

from collections import deque
from pathlib import Path


FOLDER = Path(__file__).resolve().parent
MAZE_FILE = FOLDER / "breadth.txt"
RESULTS_FILE = FOLDER / "breadth_result.txt"
Position = tuple[int, int]


def load_maze(filename: Path) -> tuple[list[str], Position, Position, set[Position]]:
    """Read a maze and return its grid, start, goal, and walls."""
    grid = filename.read_text(encoding="utf-8").splitlines()
    start = goal = None
    walls: set[Position] = set()

    for row, line in enumerate(grid):
        for column, character in enumerate(line):
            if character == "A":
                start = (row, column)
            elif character == "B":
                goal = (row, column)
            elif character == "#":
                walls.add((row, column))

    if start is None or goal is None:
        raise ValueError("The maze must contain both A (start) and B (goal).")
    return grid, start, goal, walls


def neighbors(grid: list[str], walls: set[Position], state: Position) -> list[Position]:
    """Return valid neighbouring positions."""
    row, column = state
    candidates = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]
    return [
        (next_row, next_column)
        for next_row, next_column in candidates
        if 0 <= next_row < len(grid)
        and 0 <= next_column < len(grid[next_row])
        and (next_row, next_column) not in walls
    ]


def solve_bfs(grid: list[str], start: Position, goal: Position, walls: set[Position]) -> tuple[list[Position], set[Position]]:
    """Find the shortest path from start to goal using BFS."""
    frontier = deque([start])
    parents: dict[Position, Position | None] = {start: None}
    explored: set[Position] = set()

    while frontier:
        current = frontier.popleft()
        explored.add(current)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parents[current]
            path.reverse()
            return path, explored

        for next_state in neighbors(grid, walls, current):
            if next_state not in parents:
                parents[next_state] = current
                frontier.append(next_state)

    raise ValueError("No solution exists for this maze.")


def save_results(grid: list[str], start: Position, goal: Position, path: list[Position], explored: set[Position]) -> None:
    """Save a solved maze and search summary."""
    path_cells = set(path)
    result = [
        "BREADTH-FIRST SEARCH RESULTS",
        "============================",
        "",
        f"Explored cells: {len(explored)}",
        f"Shortest path length: {len(path)}",
        "",
        "Legend: A = start, B = goal, # = wall, . = explored, * = shortest path",
        "",
    ]

    for row, line in enumerate(grid):
        rendered_row = []
        for column, character in enumerate(line):
            position = (row, column)
            if position == start:
                rendered_row.append("A")
            elif position == goal:
                rendered_row.append("B")
            elif position in path_cells:
                rendered_row.append("*")
            elif position in explored and character == " ":
                rendered_row.append(".")
            else:
                rendered_row.append(character)
        result.append("".join(rendered_row))

    RESULTS_FILE.write_text("\n".join(result) + "\n", encoding="utf-8")


def main() -> None:
    grid, start, goal, walls = load_maze(MAZE_FILE)
    path, explored = solve_bfs(grid, start, goal, walls)
    save_results(grid, start, goal, path, explored)
    print(f"BFS complete: shortest path is {len(path)} cells.")
    print(f"Results saved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()

