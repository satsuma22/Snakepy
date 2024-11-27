import numpy as np

class Layer:
    '''
    Base class for all layers
    '''

    def __init___(self):
        pass

    def forward(self, inp):
        '''
        forward pass
        '''
        raise NotImplementedError('Forward method not implemented')

    #def backward(self, inp, out_grad):
    #    raise NotImplementedError('Backward Method not implemented')


class Dense(Layer):
    '''
    Fully connected layer. Computes the function f(x) = <xw> + b
    '''

    def __init__(self, input_units, output_units):
        ''' Initializes weights and biases of the layer'''
        self.weights = np.random.uniform(-1, 1, size=(input_units, output_units))
        self.biases = np.zeros((1, output_units))

    def forward(self, inp):
        '''
        Performs the forward pass by computing f(x) = <xw> + b
        Input:
            - inp : activations from the previous layer
        Returns:
            result of the forward pass
        '''
        return np.dot(inp, self.weights) + self.biases

    def __repr__(self):
        return '{}X{}'.format(self.weights.shape[0], self.weights.shape[1])

class ReLU(Layer):
    ''' Applies ReLU non-linearity '''

    def __init__(self):
        pass

    def forward(self, inp):
        '''
        Performs forward pass
        Inputs:
            - inp : input activations from previous layer
        Return:
            max(0, inp)
        '''
        return np.maximum(0, inp)

    def __repr__(self):
        return 'ReLU'

class Sigmoid(Layer):

    def __init__(self):
        pass

    def forward(self, inp):

        return (1 / (1 + np.exp(-1*inp)))

    def __repr__(self):
        return 'Sigmoid'