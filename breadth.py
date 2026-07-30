import sys
import argparse
import random


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

    def write_solution(self, filename, mark_path='O', mark_explored='.'):
        """
        Write a visualization of the maze to `filename` with the solution path and explored cells marked.
        Path cells are marked with `mark_path` (except 'A' and 'B'). Explored cells are marked with `mark_explored`.
        """
        # build base char grid from walls
        grid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if self.walls[i][j]:
                    row.append('#')
                else:
                    row.append(' ')
            grid.append(row)

        # place start and goal
        if hasattr(self, 'start') and self.start:
            r, c = self.start
            grid[r][c] = 'A'
        if hasattr(self, 'goal') and self.goal:
            r, c = self.goal
            grid[r][c] = 'B'

        # mark explored
        if self.explored:
            for (r, c) in self.explored:
                if grid[r][c] == ' ':
                    grid[r][c] = mark_explored

        # mark path (override explored marks but keep A/B)
        if self.solution and self.solution[1]:
            for (r, c) in self.solution[1]:
                if grid[r][c] not in ('A', 'B'):
                    grid[r][c] = mark_path

        # write to file
        with open(filename, 'w', encoding='utf-8') as f:
            for row in grid:
                f.write(''.join(row) + '\n')

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



        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a maze file")
    parser.add_argument("filename", nargs='?', help="Path to maze file")
    parser.add_argument("method", nargs='?', choices=['bfs', 'dfs'], default='bfs', help="Search method (bfs or dfs)")
    parser.add_argument("--output", "-o", help="Output file to write visualization to")
    parser.add_argument("--generate", "-g", nargs=2, metavar=("WIDTH", "HEIGHT"), type=int, help="Generate a random maze with odd WIDTH HEIGHT and save to filename provided as positional arg (overwrites file if present)")
    args = parser.parse_args()

    maze_file = args.filename
    method = args.method
    out_file = args.output
    gen = args.generate

    # if generate requested, create a maze and save it to maze_file
    if gen:
        if not maze_file:
            print('Please provide a filename to save the generated maze (positional filename).')
            sys.exit(1)
        w, h = gen
        def generate_maze(width, height):
            # ensure odd dimensions
            if width % 2 == 0:
                width -= 1
            if height % 2 == 0:
                height -= 1
            grid = [['#' for _ in range(width)] for _ in range(height)]
            # carve using recursive backtracker
            stack = [(1,1)]
            grid[1][1] = ' '
            while stack:
                x,y = stack[-1]
                neighbors = []
                for dx,dy in ((2,0),(-2,0),(0,2),(0,-2)):
                    nx, ny = x+dx, y+dy
                    if 0 < nx < width and 0 < ny < height and grid[ny][nx] == '#':
                        neighbors.append((nx,ny,dx,dy))
                if neighbors:
                    nx,ny,dx,dy = random.choice(neighbors)
                    grid[ny - dy//2][nx - dx//2] = ' '
                    grid[ny][nx] = ' '
                    stack.append((nx,ny))
                else:
                    stack.pop()
            # place A at (1,1) and B at farthest open cell from A (simple BFS)
            from collections import deque
            start = (1,1)
            q = deque([start])
            visited = {start}
            last = start
            while q:
                cx,cy = q.popleft()
                last = (cx,cy)
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny = cx+dx, cy+dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == ' ' and (nx,ny) not in visited:
                        visited.add((nx,ny))
                        q.append((nx,ny))
            gx, gy = last
            grid[1][1] = 'A'
            grid[gy][gx] = 'B'
            return [''.join(row) for row in grid]

        maze_lines = generate_maze(w, h)
        with open(maze_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(maze_lines) + '\n')
        print(f'Generated maze saved to {maze_file}')

    if not maze_file:
        print('No maze file provided.')
        sys.exit(1)

    try:
        m = Maze(maze_file)
    except Exception as e:
        print('Error loading maze:', e)
        sys.exit(1)

    try:
        m.solve(method=method)
    except Exception as e:
        print('Error solving maze:', e)
        sys.exit(1)

    print('Actions:', m.solution[0])
    print('Path:', m.solution[1])
    print('Explored:', m.num_explored)

    if out_file:
        m.write_solution(out_file)
        print(f'Visualization written to {out_file}')

        




