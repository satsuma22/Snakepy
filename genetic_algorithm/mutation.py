from typing import Dict
import numpy as np

def uniform_mutation(parameters: Dict, mutation_rate: float = 0.05) -> Dict:
    '''
    Randomly mutates parameters with a probability equal to mutation_rate
    '''
    mutated_parameters = {}
    for key in parameters.keys():
        param_shape = parameters[key].shape
        probs = np.random.uniform(size=param_shape)
        probs = probs < mutation_rate
        mutated_genes = np.random.uniform(-1, 1, size=param_shape)
        mutated_parameter = probs * mutated_genes + (1 - probs) * parameters[key]
        mutated_parameter = np.clip(mutated_parameter, -1, 1)
        mutated_parameters[key] = mutated_parameter

    return mutated_parameters

def boundary_mutation(parameters: Dict, mutation_rate: float = 0.05) -> Dict:
    mutated_parameters = {}
    for key in parameters.keys():
        param_shape = parameters[key].shape
        probs = np.random.uniform(size=param_shape)
        positive_boundary_map = probs < mutation_rate
        negative_boundary_map = probs < (mutation_rate / 2)
        mutated_parameter = parameters[key]*(1-positive_boundary_map) + positive_boundary_map - 2*negative_boundary_map
        mutated_parameters[key] = mutated_parameter

    return mutated_parameters

def flip_mutation(parameters: Dict, mutation_rate: float = 0.05) -> Dict:
    mutated_parameters = {}
    for key in parameters.keys():
        param_shape = parameters[key].shape
        probs = np.random.uniform(size=param_shape)
        probs = probs < mutation_rate
        flip_map = np.ones(param_shape)
        flip_map[probs] = -1
        mutated_parameter = parameters[key] * flip_map
        mutated_parameters[key] = mutated_parameter

    return mutated_parameters