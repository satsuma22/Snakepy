from typing import List
import random
import numpy as np

def roulette_wheel_selection(parents: List) -> List:
    selections = []
    sum_fitness = 0
    for parent in parents:
        sum_fitness += parent.fitness

    for _ in range(2):
        number = random.uniform(0, sum_fitness)
        csum = 0
        for parent in parents:
            csum += parent.fitness
            if csum >= number:
                selections.append(parent)
                break

    return selections

def tournament_selection(parents: List, tournament_size: int=75) -> List:
    selections = []
    for _ in range(2):
        tournament_candidate = np.random.choice(parents, tournament_size)
        winner = max(tournament_candidate, key=lambda candidate: candidate.fitness)
        selections.append(winner)
    
    return selections