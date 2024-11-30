import pickle
import os
import random

def load_individual_parameters(layers, activation, player):
        save_dir = './checkpoints/'
        path = os.path.join(save_dir, '{}-{}-parameters.pkl'.format(layers, activation))
        try:
            with open(path, 'rb') as fin:
                save_file = pickle.load(fin)

            parameters = save_file['parameters']
            player.parameters = random.choice(parameters)
            print('Loading generation #{}'.format(save_file['generation']))
        except:
            print('No saved parameters found.')