from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, direction=None):
        self.steps = 0
        self.score = 0
        self.steps_since_last_snack = 1
        self.alive = True

        if direction is not None:
            self.direction = direction
        else:
            self.direction = (1, 0)
