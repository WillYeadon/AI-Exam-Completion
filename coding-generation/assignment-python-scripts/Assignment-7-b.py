# Welcome to the Physics Coding Assignment on Root finding.
# Please follow these steps to complete your assignment:
#
# 1. Read the section marked '::: Task :::' section to understand the primary goal of the assignment.
# 2. Review the 'Objective' section for specific instructions and criteria.
# 3. Implement your solution in the designated area marked 'HERE HERE HERE'.
# 4. Ensure to use 'plt.show()' after your plotting commands to display the results.
# 5. Your final plots should be visible and clear for assessment.
# 6. Examine the 'Starter Code' provided as a base for your implementation.
#
# Do not write comments, just the code to complete the assignment.
# Remember, a successful completion of the task involves not only writing functional code
# but also adhering to the given instructions and requirements. Good luck!

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors
from random import random

# You will illustrate the different behaviours of the gradient descent (GD) method
# when finding the minima of Rosenbrock's Banana Function, $$f(x,y) \equiv (1-x)^{2} + 100(y-x^{2})^{2}~.$$
# You will generate a plot demonstrating how the behaviour of the GD method changes
# with different values of the step-size parameter, $\eta$. 
# To do this, you will plot example GD trajectories using three different $\eta$ values. 
# Note `r` is a two component array of coordinates.

# Function to define the banana function
def banana(r):
    '''Function to be minimised'''
    x, y = r
    return (1 - x)**2 + 100*(y - x**2)**2
    
# Function to define the gradient of the banana function
def banana_grad(r):
    '''Calculate gradient of banana function at coordinates r = (x,y)'''
    x, y = r
    partial_x = -2*(1-x) - 400*x*(y-x**2)
    partial_y = 200*(y-x**2)
    
    return numpy.array([partial_x, partial_y])

# Function to implement `gradientDescent` to perform gradient descent optimization.
def gradientDescent(df, r0, eta, n_steps):
    xy = r0
    history = numpy.empty((n_steps+1, 2))
    history[0] = xy 
    for i in range(n_steps):
        der = df(xy)
        xy = xy - eta * der
        history[i+1] = xy
    return history

# ::: Task :::
# Explore the impact of different step sizes on the optimization trajectory of the gradient descent algorithm when applied to the banana function.

# Objective:
# 1. Using the provided plot `im = plt.imshow(data, ...`, populate `data` with the values of the banana function, creating a backdrop for your trajectories.
# 2. Using only the functions defined above, create a series of trajectories using different step sizes, denoted as `etas`, to observe their effect on the convergence paths of the algorithm. 
# 3. Start all trajectories from the point r_0 = (0.2,1).
# 4. Use plt.plot to plot the trajectories on the same figure as `im = plt.imshow(data, ...`
# 5. Ensure your plot includes labels, a descriptive title, and a legend to differentiate between trajectories for each step size. [5 marks]

# Suggestions:
# - Do not use a step size above 0.005 as it will cause errors.
# - Keep the cmap in `im` ad matplotlib.cm.gray so that your trajectories can be seen easily.
# - Consider using the above defined functions `banana(r)`, `banana_grad(r)` and `gradientDescent(df, r0, eta, n_steps)`.

# Starter Code:
# Initialize parameters for the banana function plot
N = 100  # Resolution of the plot
x0, x1 = -0.2, 1.2  # x-axis bounds
y0, y1 = -0.2, 1.2  # y-axis bounds
xs = np.linspace(x0, x1, N)
ys = np.linspace(y0, y1, N)
data = np.zeros((N, N))  # Placeholder for data
plt.figure(figsize=(8,8))

# Consider using this additional plot starter code
im = plt.imshow(data, extent=(x0, x1, y0, y1), origin='lower', cmap=matplotlib.cm.gray, norm=matplotlib.colors.LogNorm(vmin=0.01, vmax=200))
plt.colorbar(im, orientation='vertical', fraction=0.03925, pad=0.04)

# HERE HERE HERE