"""
Contains the logic to do projective transformations.

Given 4 reference points, transform back and forth from one layer to another.
"""

import numpy as np
from layer import Layer

# https://math.stackexchange.com/questions/296794/finding-the-transform-matrix-from-4-projected-points-with-javascript/339033#339033

def createLayer(p1: tuple, p2: tuple, p3: tuple, p4: tuple) -> Layer:
    """ Given four reference points as tuples, create a basis in the projective space. """
    A = np.array([[p1[0], p2[0], p3[0]],
                  [p1[1], p2[1], p3[1]],
                  [1,     1,     1    ]], dtype=np.float64)
    b = np.array([[p4[0]], [p4[1]], [1]], dtype=np.float64)
    try:
        x = np.linalg.inv(A) @ b
    except:
        raise f"ERROR: Cannot create a layer with reference points {p1}, {p2}, {p3}, {p4}: Likely collinearity"
    
    # Multiply each column with a coefficient from x.
    # Since scale is arbitrary this imposes that the fourth point be a lin comb of the other basis vectors.
    scaled = np.transpose([A[:, 0] * x[0], A[:, 1] * x[1], A[:, 2] * x[2]])

    return Layer(scaled)

def transform(point: tuple, layer1: Layer, layer2: Layer) -> tuple:
    """ Transforms a point from basis layer1 to basis layer2. """
    # Go from layer1's basis to standard basis to layer2's basis
    T = layer2.basis @ layer1.debase
    result = T @ [point[0], point[1], 1]
    # Using homogenous coordinates, so scale down
    try:
        return (result[0]/result[2], result[1]/result[2])
    except:
        # I have no idea how often this might happen. So I'll keep this here for now and see if it ever comes up
        print("ERROR: VANISHING POINT")