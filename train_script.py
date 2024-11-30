import sys
import json
from genetic_algorithm.population import Population
from smart_player import SmartPlayer
from game.game import Game

def train(iterations):
    settings = None
    try:
        with open('config.json', 'r') as fin:
            settings = json.load(fin)
    except:
        print('No config file found. Please run main.py to create a config file.')
    
    game_grid_size = int(settings['game_settings']['grid_size'])
    input_type = settings['network_settings']['input_type']
    input_dim = 8 if input_type == 'vision' else (game_grid_size + 2)**2
    hidden_layers = settings['network_settings']['hidden_layers']
    hidden_layer_activation = settings['network_settings']['hidden_layer_activation']
    population_size = int(settings['genetic_algorithm_settings']['population_size'])
    parent_count = int(settings['genetic_algorithm_settings']['parents_size'])
    
    individuals = [SmartPlayer(input_dim, hidden_layers, hidden_layer_activation) for _ in range(population_size)]
    
    population = Population(individuals, parent_count)
    
    population.load_population_parameters(str(individuals[0].network), hidden_layer_activation)

    game = Game(game_grid_size)

    for _ in range(iterations):
        print('Simulating generation #{}'.format(population.generation))
        scores = []
        fitness = []

        for individual in population:
            while not game.is_game_finished and individual.alive:
                game_state = game.get_game_state(input_type == 'vision')
                individual.predict_direction(game_state)
                game.update(individual)
                if individual.steps_since_last_snack > 1000:
                    individual.alive = False
            scores.append(individual.score)
            fitness.append(individual.fitness)
            game.reset()

        print('Generation #{} Statistics'.format(population.generation))
        print('Average Score: {}'.format(sum(scores)/len(scores)))
        print('Average Fitness: {}'.format(sum(fitness)/len(fitness)))
        print('Highest Score: {}'.format(max(scores)))
        print()

        population.evolve_generation()
            
        for individual in population:
            individual.reset()
    
    population.save_population_parameters()

if __name__ == '__main__':
    iterations = 1
    if len(sys.argv) == 2:
        try:
            iterations = int(sys.argv[1])
        except:
            print('Usage: {} [iterations]'.format(sys.argv[0]))
            exit()
        
    train(iterations)