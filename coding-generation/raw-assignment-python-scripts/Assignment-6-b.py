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

# Function to simulate the integration error showing its scaling is 
# independent of the dimension and that the error scales as $1/\sqrt{N}$. 
# The number of points and dimensions has been provided. 

ns = np.logspace(1, 7, num=18, base=10, dtype=int)
dimensions = range(2,7)

targets = {
    2: np.pi,
    3: 4/3*np.pi,
    4: 1/2*np.pi**2,
    5: 8/15*np.pi**2,
    6: 1/6*np.pi**3,
}

# Initialize the results array including an additional row for the theoretical scaling
results = np.zeros((len(dimensions) + 1, len(ns)))

for i, dim in enumerate(dimensions):
    for j, n in enumerate(ns):
        results[i, j] = abs(targets[dim] - integrate(n, dim))

# Store the theoretical error scaling in the last row of the results array
results[-1, :] = [1 / np.sqrt(n) for n in ns]

# In addition to integrating functions using Monte Carlo methods, we can also create a distribution of points according to an arbitrary function. This task involves generating values of $x$ between 0 and 10 distributed according to a given probability density function:
# $$ \frac{1}{\mathcal{N}} \left( 1 + \frac{2}{1+x^2}+ \cos(\sqrt{3 x})^2\right) $$
# with 
# $$ \mathcal{N} = \int\limits_0^{10} f(x) dx \;.$$
# This defines the function:

norm = (179 + 24*numpy.arctan(10)+numpy.cos(2*numpy.sqrt(30))+2*numpy.sqrt(30)*numpy.sin(2*numpy.sqrt(30)))/12

def f(x):
    return  (1 + (2/(1+x**2)+ numpy.cos(numpy.sqrt(3*x))**2))/norm

# This implements the function over a linspace from 0 to 10
xs = numpy.linspace(0, 10, 200)
fs = f(xs)

# Define a function `genSample` that generates a sample of `npts` values $x$ distributed according to $f(x)$.
def genSample(n_points):
    sample = []
    # find the maximum
    xs = numpy.linspace(0,10,1000)
    fs = f(xs)
    maxf = max(fs) + 0.01  # small margin of safety
    # create the sample
    while len(sample) < n_points:
        x = 10 * random.random()
        r = random.random()
        if r * maxf < f(x) :
            sample.append(x)

    return numpy.array(sample)

# ::: Task ::: Make a plot to show that the values generated are distributed in the right manner. The plot should have a title and axis labels. [5 marks]
# HERE HERE HERE
