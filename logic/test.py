""" Once we get to the unit testing part of my swe class I'll make some unit tests. """

import numpy as np
import matplotlib.pyplot as plt

import transform
from layer import Layer

layer1: Layer = transform.createLayer((0, 0), (0, 1), (1, 0), (1, 1))
layer2: Layer = transform.createLayer((0, 0), (.25, 1.25), (1.25, .25), (1.25, 1.25))

n = 100
stop = 1
r = np.arange(0, stop, stop/n)
locus1 = [(0, i) for i in r] + [(i, 0) for i in r] + [(stop, i) for i in r] + [(i, stop) for i in r]
locus2 = [transform.transform(point, layer1, layer2) for point in locus1]

plt.scatter(*zip(*locus1))
plt.scatter(*zip(*locus2))
plt.show()

# We can see that the unit square is properly transformed.