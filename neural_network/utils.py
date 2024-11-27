import numpy as np

def softmax(inp):
    '''
    converts vector of values to vector of probabilities
    '''
    inp_exp = np.exp(inp)
    return inp_exp / np.sum(inp_exp, axis=1)