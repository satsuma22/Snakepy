from game.player import Player

import random
import numpy as np

class Game:
    def __init__(self, player:Player, grid_size, start_pos = None, seed = None):
        self.grid_size = grid_size
        self.is_game_finished = False
        self.seed = seed
        self.player = player
        self.start_pos = start_pos

        if self.start_pos is None:
            self.start_pos = (grid_size // 2, grid_size // 2)

        self.player_body = [self.start_pos] 
        
        self.snack = None
        self.generate_snack()

        self.score = 0

    def reset(self):
        self.is_game_finished = False
        self.score = 0
        self.player_body = [self.start_pos]
        self.generate_snack()


    def generate_snack(self):
        empty_pos = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) if (x, y) not in self.player_body]
        self.snack = random.choice(empty_pos)

    def get_game_state(self, vision=False):
        if vision:
            pass
        else:
            game_state = np.zeros((self.grid_size+2, self.grid_size+2))
            for i in [0, self.grid_size + 1]:
                for j in range(self.grid_size+2):
                    game_state[i][j] = -1
                    game_state[j][i] = -1
            
            for pos in self.player_body:
                game_state[pos[0]][pos[1]] = -1

            game_state[self.snack[0]][self.snack[1]] = 1

            return game_state
        


    def update(self):
        direction = self.player.direction
        head = self.player_body[0]

        new_head = (head[0] + direction[0], head[1] + direction[1])
        if new_head in self.player_body or new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            self.is_game_finished = True
            return
        
        if new_head == self.snack:
            self.score += 1
            self.generate_snack()
        else:
            self.player_body = self.player_body[:-1]

        self.player_body = [new_head] + self.player_body