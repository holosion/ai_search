def depth_limited_search(graph, start, goal, limit):

    def dls(node, depth):
        # Check if we found the goal
        if node == goal:
            return [node]

        # Stop searching if we reached the depth limit
        if depth == limit:
            return None

        # Explore the neighbors
        for neighbor in graph[node]:

            path = dls(neighbor, depth + 1)

            if path is not None:
                return [node] + path

        return None

    return dls(start, 0)


# Example graph
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H"],
    "E": [],
    "F": [],
    "G": [],
    "H": []
}


result = depth_limited_search(graph, "A", "H", 2)

print(result)