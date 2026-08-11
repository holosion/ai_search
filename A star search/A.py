#implementing an A* search algorithm in Python
def a_star_search(graph, start, goal, heuristic):

    # nodes that still need to be explored
    open_list = [start]

    #nodes that have already been explored
    closed_list = set()

    #cost from start to each node
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    #estimated total cost from start to goal through each node
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]

    #to reconstruct the final path
    came_from = {}

    while open_list:
        pass
