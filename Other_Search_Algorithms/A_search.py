def a_star_search(graph, start, goal, heuristic):
    open_list = [(heuristic[start], start)]
    closed_list = set()
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}

    while open_list:
        f, current = min(open_list)
        open_list.remove((f, current))
        closed_list.add(current)

        if current == goal:
            break

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + graph[current][neighbor]

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]

                if neighbor not in open_list:
                    open_list.append((f_score[neighbor], neighbor))

    # Reconstruct the path
    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path