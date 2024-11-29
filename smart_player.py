from game.player import Player
from genetic_algorithm.individual import Individual
from neural_network.nn import FeedForwardNetwork

import numpy as np

class SmartPlayer(Player, Individual):
    def __init__(self, inp_dim):
        super().__init__()
        self.network = FeedForwardNetwork(inp_dim, [8, 4])

    def predict_direction(self, input):
        input = input.reshape(1, -1)
        out = self.network.predict(input)
        choice = np.argmax(out)

        if choice == 0:
            self.direction = (0, -1)
        elif choice == 1:
            self.direction = (0, 1)
        elif choice == 2:
            self.direction = (-1, 0)
        elif choice == 3:
            self.direction = (1, 0)

    @property
    def fitness(self):
        return (self.score << 9) + ((self.score/self.steps) * 100) + min(self.steps, 10)

    @property
    def parameters(self):
        return self.network.parameters

    @parameters.setter
    def parameters(self, params):
        self.network.parameters = params

    def reset(self):
        self.score = 0
        self.steps_since_last_snack = 1
        self.steps = 0
        self.alive = True

