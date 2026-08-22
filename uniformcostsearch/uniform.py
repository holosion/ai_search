#implementing a uniform cost search algorithm
import heapq

def uniform_cost_search(graph, start, goal):
    # creating a frontier priority queue and a dictionary to store the cost of reaching each node
    frontier = []

    heapq.heappush(frontier, (0, start))
    explored = set()

    while frontier:
        # pop the node with the lowest cost from the priority queue
        cost, node = heapq.heappop(frontier)

        # if the node is the goal, return the cost and the path
        if node == goal:
            return cost, 

# if the node has already been explored, skip it
        if node in explored:
            continue
        explored.add(node)

        for neighbor, edge_cost in graph[node]:
            if neighbor not in explored:
                # calculate the total cost to reach the neighbor
                total_cost = cost + edge_cost
                heapq.heappush(frontier, (total_cost, neighbor))

    return None  # return None if there is no path from start to goal


graph = {
    "A": [("B", 2), ("C", 5)],
    "B": [("D", 3)],
    "C": [("D", 1)],
    "D": []
}

result = uniform_cost_search(graph, "A", "D")
print(result)
