from .layers import Dense, ReLU, Sigmoid
from .utils import softmax

class FeedForwardNetwork:
    '''
    Acts as the snake's brain
    '''

    def __init__(self, input_dim, layer_sizes, hidden_layer_activation='ReLU'):
        '''
        initializes the neural network
        '''
        self.inp_dim = input_dim
        self.layer_sizes = [self.inp_dim] + layer_sizes
        self.network = []
        self.hidden_layer_activation = hidden_layer_activation
        self._build()

    def _build(self):
        '''
        Builds the neural network
        '''
        for inp_dim, out_dim in zip(self.layer_sizes[:-2], self.layer_sizes[1:-1]):
            self.network.append(Dense(inp_dim, out_dim))
            if self.hidden_layer_activation == 'ReLU':
                self.network.append(ReLU())
            elif self.hidden_layer_activation == 'Sigmoid':
                self.network.append(Sigmoid())
            else:
                raise Exception(f'{self.hidden_layer_activation} is not implemented. Choose from ReLU and Sigmoid.')

        self.network.append(Dense(self.layer_sizes[-2], self.layer_sizes[-1]))
        

    def predict(self, inp):
        '''
        Predicts the best move
        '''

        for layer in self.network:
            inp = layer.forward(inp)

        return softmax(inp)

    @property
    def parameters(self):
        '''
        Return all the trainable/adjustable parameters of the network
        '''
        params = {}
        idx = 1
        for layer in self.network:
            if isinstance(layer, Dense):
                params['w' + str(idx)] = layer.weights
                params['b' + str(idx)] = layer.biases
                idx = idx + 1

        return params

    @parameters.setter
    def parameters(self, params):
        idx = 1
        for layer in self.network:
            if isinstance(layer, Dense):
                layer.weights = params['w' + str(idx)]
                layer.biases = params['b' + str(idx)]
                idx = idx + 1
    

    def __repr__(self):
        rep = ''
        for layer_size in self.layer_sizes[:-1]:
            rep += str(layer_size) + '-'
        rep += str(self.layer_sizes[-1])
        return rep
        #return f'Network:\nNumber of Hidden Layers: {len(self.network) // 2 + 1}\n'
