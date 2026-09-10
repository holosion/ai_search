#implementing a hill climbing algorithm
import numpy as np

#define the objective and generate neigbouring fucntions
def objective(x):
    return -x[0]**2 + 5

def generate_neighbors(x, step_size=0.1):
    return [np.array([x[0] + step_size]), np.array([x[0]-step_size])]

