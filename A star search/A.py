import heapq


def reconstruct_path(came_from, start, goal):
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    return path


def a_star_search(graph, start, goal, heuristic):
    open_heap = [(heuristic[start], 0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    while open_heap:
        f_score, current_cost, current = heapq.heappop(open_heap)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        if current_cost > g_score[current]:
            continue

        for neighbor, weight in graph[current].items():
            tentative_g_score = current_cost + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                heapq.heappush(
                    open_heap,
                    (tentative_g_score + heuristic[neighbor], tentative_g_score, neighbor),
                )

    return None


if __name__ == "__main__":
    graph = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "C": 2, "D": 5},
        "C": {"A": 4, "B": 2, "D": 1},
        "D": {"B": 5, "C": 1, "E": 2},
        "E": {"D": 2},
    }

    heuristic = {
        "A": 5,
        "B": 3,
        "C": 2,
        "D": 2,
        "E": 0,
    }

    path = a_star_search(graph, "A", "E", heuristic)
    print("Graph:", graph)
    print("Heuristic:", heuristic)
    print("Path from A to E:", path)
