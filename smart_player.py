from game.player import Player
from neural_network.nn import FeedForwardNetwork

import numpy as np

class SmartPlayer(Player):
    def __init__(self, inp_dim):
        super().__init__()
        self.network = FeedForwardNetwork(inp_dim, [16, 8, 4])

    def predict_direction(self, input):
        input = input.reshape(1, -1)
        out = self.network.predict(input)
        print(out)
        choice = np.argmax(out)

        if choice == 0:
            print('Up')
            self.direction = (0, -1)
        elif choice == 1:
            print('Down')
            self.direction = (0, 1)
        elif choice == 2:
            print('Left') 
            self.direction = (-1, 0)
        elif choice == 3:
            print('Right')
            self.direction = (1, 0)

