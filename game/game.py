import random
import numpy as np

class Game:
    def __init__(self, grid_size, start_pos = None, seed = None):
        self.grid_size = grid_size
        self.is_game_finished = False
        self.seed = seed
        self.start_pos = start_pos

        if self.start_pos is None:
            self.start_pos = (grid_size // 2, grid_size // 2)

        self.player_body = [self.start_pos] 
        
        self.snack = None
        self.generate_snack()

    def reset(self):
        self.is_game_finished = False
        self.player_body = [self.start_pos]
        self.generate_snack()


    def generate_snack(self):
        empty_pos = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) if (x, y) not in self.player_body]
        self.snack = random.choice(empty_pos)

    def get_game_state(self, vision=False):
        if vision:
            is_snack = lambda pos: pos == self.snack
            is_boundary = lambda pos: min(pos[0],pos[1]) < 0 or max(pos[0], pos[1]) == self.grid_size
            is_body = lambda pos: pos in self.player_body

            game_state = np.zeros(8)
            head = self.player_body[0]
            
            up = (head[0], head[1] - 1)
            down = (head[0], head[1] + 1)
            left = (head[0] - 1, head[1])
            right = (head[0] + 1, head[1])

            game_state[0] = is_snack(up) * 1 + is_body(up) * -1 + is_boundary(up) * -1
            game_state[1] = is_snack(down) * 1 + is_body(down) * -1 + is_boundary(down) * -1
            game_state[2] = is_snack(left) * 1 + is_body(left) * -1 + is_boundary(left) * -1
            game_state[3] = is_snack(right) * 1 + is_body(right) * -1 + is_boundary(right) * -1

            pos = up
            while not is_snack(pos) and not is_body(pos) and not is_boundary(pos):
                pos = (pos[0], pos[1] - 1)
            game_state[4] = is_snack(pos) * 1 + is_body(pos) * -1 + is_boundary(pos) * -1

            pos = down
            while not is_snack(pos) and not is_body(pos) and not is_boundary(pos):
                pos = (pos[0], pos[1] + 1)
            game_state[5] = is_snack(pos) * 1 + is_body(pos) * -1 + is_boundary(pos) * -1

            pos = left
            while not is_snack(pos) and not is_body(pos) and not is_boundary(pos):
                pos = (pos[0] - 1, pos[1])
            game_state[6] = is_snack(pos) * 1 + is_body(pos) * -1 + is_boundary(pos) * -1

            pos = right
            while not is_snack(pos) and not is_body(pos) and not is_boundary(pos):
                pos = (pos[0] + 1, pos[1])
            game_state[7] = is_snack(pos) * 1 + is_body(pos) * -1 + is_boundary(pos) * -1
            
            return game_state

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
        


    def update(self, player):
        direction = player.direction
        head = self.player_body[0]

        player.steps += 1
        
        new_head = (head[0] + direction[0], head[1] + direction[1])
        if new_head in self.player_body or new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            self.is_game_finished = True
            player.alive = False
            return
        
        if new_head == self.snack:
            player.score += 1
            player.steps_since_last_snack = 1
            self.generate_snack()
        else:
            self.player_body = self.player_body[:-1]
            player.steps_since_last_snack += 1

        self.player_body = [new_head] + self.player_body