import heapq
# Imports Python's heap-based priority queue.
# GBFS needs a priority queue so that the node with the
# smallest heuristic value is selected first.


def greedy_best_first_search(graph, heuristic, start, goal):
    # graph       -> Dictionary containing each node and its neighbors
    # heuristic   -> Dictionary containing h(n) for every node
    # start       -> Starting node
    # goal        -> Destination node

    priority_queue = []
    # Creates an empty priority queue.
    # Each item will be stored as:
    # (heuristic_value, node)


    heapq.heappush(priority_queue, (heuristic[start], start))
    # Adds the starting node to the priority queue.
    # heuristic[start] determines its priority.
    # The node with the LOWEST heuristic value has the highest priority.


    visited = set()
    # Keeps track of nodes that have already been explored.
    # This prevents the algorithm from repeatedly visiting the same node.


    parent = {start: None}
    # Stores where each node came from.
    # This allows us to reconstruct the final path after reaching the goal.
    #
    # The start node has no parent, so:
    # start -> None


    while priority_queue:
        # Continue searching as long as there are nodes
        # waiting in the priority queue.


        _, current = heapq.heappop(priority_queue)
        # Removes the node with the SMALLEST heuristic value.
        #
        # Example:
        # (2, 'E')
        # (4, 'B')
        # (6, 'A')
        #
        # 'E' will be selected first because its heuristic is 2.
        #
        # "_" ignores the heuristic value because we only need the node here.


        if current in visited:
            # Checks whether this node has already been explored.

            continue
            # If it has already been explored, skip it
            # and move to the next node in the priority queue.


        visited.add(current)
        # Marks the current node as explored.


        if current == goal:
            # Checks whether we have reached the destination.


            path = []
            # Creates an empty list that will store the path.


            while current is not None:
                # Walk backwards through the parent dictionary
                # until we reach the starting node.


                path.append(current)
                # Adds the current node to the path.


                current = parent[current]
                # Moves to the parent of the current node.


            return path[::-1]
            # The path was constructed backwards:
            #
            # Goal -> ... -> Start
            #
            # [::-1] reverses it:
            #
            # Start -> ... -> Goal
            #
            # Then returns the final path.


        for neighbor in graph[current]:
            # Goes through every neighbor connected to the current node.


            if neighbor not in visited:
                # Only process the neighbor if we haven't explored it yet.


                parent[neighbor] = current
                # Records that the current node is the parent
                # of this neighbor.
                #
                # Example:
                # If A -> B
                # parent[B] = A


                heapq.heappush(
                    priority_queue,
                    (heuristic[neighbor], neighbor)
                )
                # Adds the neighbor to the priority queue.
                #
                # Its heuristic value determines its priority.
                #
                # Smaller heuristic = explored sooner.


    return None
    # If the priority queue becomes empty without reaching
    # the goal, there is no path from start to goal.