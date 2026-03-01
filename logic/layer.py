""" Contains logic for a single map layer and how it interacts with other layers. """

import numpy as np

class Layer:
    def __init__(self, basis: np.array):
        self.basis = basis
        self.debase = None
        try:
            self.debase = np.linalg.inv(basis)
        except:
            print("ERROR: Invalid basis")