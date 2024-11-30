class Individual:

    def __init__(self):
        pass
    

    @property
    def fitness(self):
        raise NotImplementedError('Please implement the fitness function for your class')

    @property
    def parameters(self):
        raise NotImplementedError('Please implement the parameters function for your class')