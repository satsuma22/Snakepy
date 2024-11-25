from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, direction=None):
        
        if direction is not None:
            self.direction = direction
        else:
            self.direction = (1, 0)
