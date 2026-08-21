def a_star_search(graph, start, goal, heuristic):
    # Track candidates, completed nodes, and parent links for path recovery.
    open_list = [(heuristic[start], start)]
    closed_list = set()
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}

    # Always expand the candidate with the lowest estimated total cost.
    while open_list:
        f, current = min(open_list)
        open_list.remove((f, current))
        closed_list.add(current)

        # Stop as soon as the goal is selected for expansion.
        if current == goal:
            break

        # Relax each edge when it offers a cheaper route to a neighbor.
        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + graph[current][neighbor]

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]

                if neighbor not in open_list:
                    open_list.append((f_score[neighbor], neighbor))

    # Reconstruct the path by following parent links from the goal.
    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path