# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy
import numpy as np
import math
import matplotlib.pyplot as plt
import random

from scipy.special import gamma

# Implement the function `findPi` that gives the Monte Carlo estimate for $\pi$ from `n_points`.
def findPi(n_points):
    # Unit square
    radius = 1
    # Random numbers in two dimensions x and y
    ran = numpy.random.uniform(0, 1, size=(n_points, 2)) 
    radii = numpy.sum(ran * ran, axis = 1)
    number_in = 0
    for radius in radii:
        if radius < 1:
            number_in += 1
    return 4 * (number_in/n_points)

# Implement the function `integrate` that gives the Monte Carlo estimate for the volume of a unit ball in `dim` dimensions. To do so we choose `n_points` worth of random numbers in the `dim`-dimensional cube of sides $[-1,+1]$ that contains the unit ball.
def integrate(n_points, dim):
    rs = numpy.random.uniform(-1, 1, size=(n_points,dim)) 
    radii = numpy.sum( rs * rs, axis = 1)
    number_in = 0
    for radius in radii:
        if radius < 1:
            number_in += 1
    return number_in/n_points * 2**dim

# ::: Task ::: Use your function to show that the integration error scaling is independent of the dimension and that the error scales as $1/\sqrt{N}$. Use the provided number of points and dimensions. Your plot should have labels, a title and a legend [5 marks].
dimensions = [
    {"dimension": 2, "volume": np.pi},
    {"dimension": 3, "volume": 4/3*np.pi},
    {"dimension": 4, "volume": 1/2*np.pi**2},
    {"dimension": 5, "volume": 8/15*np.pi**2},
    {"dimension": 6, "volume": 1/6*np.pi**3}
]
# HERE HERE HERE
