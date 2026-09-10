#implementing a hill climbing algorithm
import numpy as np

#define the objective and generate neigbouring fucntions
def objective(x):
    return -x[0]**2 + 5

def generate_neighbors(x, step_size=0.1):
    return [np.array([x[0] + step_size]), np.array([x[0]-step_size])]

# implement the hill climbing algorithm

def hill_climbing(objective, initial_state, n_iterations=100, step_size= 0.1):
    current = np.array([initial_state])
    current_eval = objective(current)
    for i in range(n_iterations):
        neighbors = generate_neighbors(current, step_size)
        neighbor_evals = [objective(neighbor) for neighbor in neighbors]
        best_idx = np.argmax(neighbor_evals)
        if neighbor_evals[best_idx] > current_eval:
            current = neighbors[best_idx]
            current_eval = neighbor_evals[best_idx]
            print(f'step {i+1}: current state = {current[0]:4f}m  current eval = {current_eval:4f}')
        else:
            print('no better neighbors found algorithm had converged')
            break
        return current, current_eval


#intialize and run the algorithm
initial_guess = 2.0
solution, value = hill_climbing(
    objective, initial_guess, n_iterations=100, step_size=0.1)
print(f"\nBest solution x = {solution[0]:.4f}, f(x) = {value:.4f}")