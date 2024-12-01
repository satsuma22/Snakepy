import random
import os
import pickle
import json

from .selection import roulette_wheel_selection, tournament_selection
from .crossover import single_point_crossover, uniform_crossover
from .mutation import boundary_mutation, flip_mutation, uniform_mutation

class Population:
    def __init__(self, individuals, save_dir='./checkpoints/'):
        self.individuals = individuals
        self.save_dir = save_dir
        self.generation = 0
        self.current_individual = 0
        self.settings = None
        with open('config.json', 'r') as fin:
            self.settings = json.load(fin)

        self.number_of_parents = self.settings['genetic_algorithm_settings']['parents_size']
        self.selection_type = self.settings['genetic_algorithm_settings']['selection_type']
        self.crossover_type = self.settings['genetic_algorithm_settings']['crossover_type']
        self.mutation_type = self.settings['genetic_algorithm_settings']['mutation_type']
        self.mutation_rate = self.settings['genetic_algorithm_settings']['mutation_rate']

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_individual < len(self.individuals):
            self.current_individual += 1
            return self.individuals[self.current_individual-1]
        self.current_individual = 0
        raise StopIteration
    
    def evolve_generation(self):
        self.individuals.sort(key=lambda individual: individual.fitness, reverse=True)
        
        parents = self.individuals[:self.number_of_parents]
        next_generation_parameters = []

        # Carry forward the current generation of parent parameters to next generation
        for parent in parents:
            next_generation_parameters.append(parent.parameters)

        for _ in range(self.number_of_parents, len(self.individuals), 2):
            selected_parents = []
            if self.selection_type == 'roulette wheel selection':
                selected_parents = roulette_wheel_selection(parents)
            elif self.selection_type == 'tournament selection':
                selected_parents = tournament_selection(parents, 50)
            else:
                raise Exception('Invalid Selection Type. Choose from "roulette wheel selection" and "tournament selection"')
            
            parent1_chromosomes = selected_parents[0].parameters
            parent2_chromosomes = selected_parents[1].parameters

            child1_chromosomes = None
            child2_chromosomes = None

            if self.crossover_type == 'single point crossover':
                child1_chromosomes, child2_chromosomes = single_point_crossover(parent1_chromosomes, parent2_chromosomes)
            elif self.crossover_type == 'uniform crossover':
                child1_chromosomes, child2_chromosomes = uniform_crossover(parent1_chromosomes, parent2_chromosomes)
            else:
                raise Exception('Invalid Crossover Type. Choose from "single point crossover" and "uniform crossover"')

            if self.mutation_type == 'boundary mutation':
                child1_chromosomes = boundary_mutation(child1_chromosomes, self.mutation_rate)
                child2_chromosomes = boundary_mutation(child2_chromosomes, self.mutation_rate)
            elif self.mutation_type == 'flip mutation':
                child1_chromosomes = flip_mutation(child1_chromosomes, self.mutation_rate)
                child2_chromosomes = flip_mutation(child2_chromosomes, self.mutation_rate)
            elif self.mutation_type == 'uniform mutation':
                child1_chromosomes = uniform_mutation(child1_chromosomes, self.mutation_rate)
                child2_chromosomes = uniform_mutation(child2_chromosomes, self.mutation_rate)

            next_generation_parameters.append(child1_chromosomes)
            next_generation_parameters.append(child2_chromosomes)

        random.shuffle(next_generation_parameters)
        
        for i, individual in enumerate(self.individuals):
            individual.parameters = next_generation_parameters[i]

        self.generation += 1
        
    def save_population_parameters(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        all_params = []
        for individual in self.individuals:
            all_params.append(individual.parameters)

        save_file = {'parameters': all_params, 'generation': self.generation}

        with open(os.path.join(self.save_dir, '{}-{}-parameters.pkl'.format(str(self.individuals[0].network), self.individuals[0].network.hidden_layer_activation)), 'wb') as fout:
            pickle.dump(save_file, fout)

        print('Saving Parameters...')

    def load_population_parameters(self, layers, activation):
        path = os.path.join(self.save_dir, '{}-{}-parameters.pkl'.format(layers, activation))
        try:
            with open(path, 'rb') as fin:
                save_file = pickle.load(fin)

            parameters = save_file['parameters']
            generation = save_file['generation']
            
            for i, parameter in enumerate(parameters):
                self.individuals[i].parameters = parameter
            self.generation = generation

            print('Generation #{} loaded.'.format(self.generation))
        except:
            print('No saved parameters found.')