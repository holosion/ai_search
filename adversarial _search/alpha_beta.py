#implementing alpha beta pruning algorithm for adversarial search
def minimax(node, maximizing_player, alpha, beta):

    if isinstance(node, int):
        return node

    children = tree[node]

    if maximizing_player:

        value = float('-inf')

        for child in children:

            value = max(
                value,
                minimax(child, False, alpha, beta)
            )

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:

        value = float('inf')

        for child in children:

            value = min(
                value,
                minimax(child, True, alpha, beta)
            )

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value
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

print("The optimal value for the maximizing player is:", minimax("ROOT", True, float('-inf'), float('inf')))