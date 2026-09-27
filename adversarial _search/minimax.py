def minimax(node, maximizing_player):

    if isinstance(node, int):
        return node

    children = tree[node]

    if maximizing_player:
        value = float('-inf')

        for child in children:
            value = max(value, minimax(child, False))

        return value

    else:
        value = float('inf')

        for child in children:
            value = min(value, minimax(child, True))

        return value


# The tree to be used for testing the minimax algorithm
tree = {
    "ROOT": ["A", "B", "C"],
    "A": ["D", "E"],
    "B": ["F", "G"],
    "C": ["H", "I"],

    "D": [4, 7],
    "E": [2, 9],
    "F": [6, 3],
    "G": [8, 5],
    "H": [1, 4],
    "I": [7, 2]
}


result = minimax("ROOT", True)

print(f"The optimal value for the maximizing player is: {result}")