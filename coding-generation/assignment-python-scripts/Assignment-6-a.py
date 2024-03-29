# Welcome to the Physics Coding Assignment on Monte Carlo Integration.
# Please follow these steps to complete your assignment:
#
# 1. Read the section marked '::: Task :::' section to understand the primary goal of the assignment.
# 2. Review the 'Objective' section for specific instructions and criteria.
# 3. Implement your solution in the designated area marked 'HERE HERE HERE'.
# 4. Ensure to use 'plt.show()' after your plotting commands to display the results.
# 5. Your final plots should be visible and clear for assessment.
#
# Do not write comments, just the code to complete the assignment.
# Remember, a successful completion of the task involves not only writing functional code
# but also adhering to the given instructions and requirements. Good luck!

import numpy as np
import math
import matplotlib.pyplot as plt
import random

from scipy.special import gamma

# Function that gives the Monte Carlo 
# estimate for $\pi$ from `n_points`.
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

# Function that gives the Monte Carlo estimate
# for the volume of a unit ball in `dim` dimensions. 
# To do so we choose `n_points` worth of random numbers in the `dim`-dimensional 
# cube of sides $[-1,+1]$ that contains the unit ball.
def integrate(n_points, dim):
    rs = numpy.random.uniform(-1, 1, size=(n_points,dim)) 
    radii = numpy.sum( rs * rs, axis = 1)
    number_in = 0
    for radius in radii:
        if radius < 1:
            number_in += 1
    return number_in/n_points * 2**dim

# ::: Task :::
# Demonstrate the independence of integration error scaling from dimension and its relation to the number of points used.

# Objective:
# 1. Use the `integrate()` function to create a plot showing that the integration error scaling is independent of the dimension.
# 2. Additionally, demonstrate that the error scales as \(1/\sqrt{N}\).
# 3. Use the dimensions specified in the 'dimensions' list below.
# 4. Ensure the plot includes labels, a descriptive title, and a legend.

# Suggestions:
# - Clearly plot the error for each dimension to illustrate the independence from the dimension.
# - Use a suitable scale (like a log scale) on the axes to effectively demonstrate the \(1/\sqrt{N}\) scaling of the error.
# - Utilize distinct colors or markers for each dimension to enhance plot clarity.
# - Ensure the plot is well-labeled with an informative title and a legend explaining the various dimensions.

# Starter Code:
dimensions = [
    {"dimension": 2, "volume": np.pi},
    {"dimension": 3, "volume": 4/3*np.pi},
    {"dimension": 4, "volume": 1/2*np.pi**2},
    {"dimension": 5, "volume": 8/15*np.pi**2},
    {"dimension": 6, "volume": 1/6*np.pi**3}
]

# HERE HERE HERE