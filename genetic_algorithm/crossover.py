from typing import Dict
import numpy as np
import random

def uniform_crossover(parent1_params: Dict, parent2_params: Dict, uniform_crossover_prob=0.5) -> Dict:
    child1_params = {}
    child2_params = {}
    for key in parent1_params.keys():
        params_shape = parent1_params[key].shape

        probs = np.random.uniform(size=params_shape)
        probs = probs < uniform_crossover_prob

        child1_param = parent1_params[key] * probs + parent2_params[key] * (1 - probs)
        child2_param = parent1_params[key] * (1 - probs) + parent2_params[key] * probs

        child1_params[key] = child1_param
        child2_params[key] = child2_param

    return child1_params, child2_params

def single_point_crossover(parent1_params: Dict, parent2_params: Dict, order='r') -> Dict:
    if order == 'r':
        order = 'C' # C-style ordering or row-major
    elif order == 'c':
        order = 'F' # Fortran-style ordering or column-major
    else:
        raise Exception('Value of "order" parameter can only be one of r (row-major) or c (column-major). ')

    child1_params = {}
    child2_params = {}

    for key in parent1_params.keys():
        params_shape = parent1_params[key].shape
        number_of_weights = np.prod(params_shape)

        single_point = random.randint(0, number_of_weights-1)

        child1_param = np.zeros(number_of_weights)
        child2_param = np.zeros(number_of_weights)

        child1_param[:single_point] = parent1_params[key].ravel(order)[:single_point]
        child1_param[single_point:] = parent2_params[key].ravel(order)[single_point:]

        child2_param[:single_point] = parent2_params[key].ravel(order)[:single_point]
        child2_param[single_point:] = parent1_params[key].ravel(order)[single_point:]

        child1_param = child1_param.reshape(params_shape) if order == 'C' else child1_param.reshape(params_shape).T
        child2_param = child2_param.reshape(params_shape) if order == 'C' else child2_param.reshape(params_shape).T

        child1_params[key] = child1_param
        child2_params[key] = child2_param

    return child1_params, child2_params