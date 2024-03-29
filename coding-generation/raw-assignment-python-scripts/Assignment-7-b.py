# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors
from random import random

# You will illustrate the different behaviours of the gradient descent (GD) method when finding the minima of 
# *Rosenbrock's Banana Function*,
# $$f(x,y) \equiv (1-x)^{2} + 100(y-x^{2})^{2}~.$$
# You will generate a plot demonstrating how the behaviour of the GD method changes with different values of the step-size parameter, $\eta$. To do this, you will plot example GD trajectories using three different $\eta$ values. 
# First, define the functions `banana` and `banana_grad` which implement the *banana* function and its **analytical** derivative. 
# `r` is a two component array of coordinates.

def banana(r):
    '''Function to be minimised'''
    x, y = r
    return (1 - x)**2 + 100*(y - x**2)**2
    
def banana_grad(r):
    '''Calculate gradient of banana function at coordinates r = (x,y)'''
    x, y = r
    partial_x = -2*(1-x) - 400*x*(y-x**2)
    partial_y = 200*(y-x**2)
    
    return numpy.array([partial_x, partial_y])

def gradientDescent(df, r0, eta, n_steps):
    xy = r0
    history = numpy.empty((n_steps+1, 2))
    history[0] = xy 
    for i in range(n_steps):
        der = df(xy)
        xy = xy - eta * der
        history[i+1] = xy
    return history

# ::: Task ::: Visualize the optimization path of the gradient descent algorithm applied to the banana function. Your task is to populate `data` with the values of the banana function to create a backdrop for your plots. Experiment with different step sizes, denoted as `etas`, to analyze their influence on the convergence paths of the algorithm. All trajectories should start from $r_0=(0.2,1)$. Starter code has been provided that creates a $100 \times 100$ point grid. Your plot should have labels, a title and a legend [5 marks]
# 
# Initialize parameters for the banana function plot
N = 100  # Resolution of the plot
x0, x1 = -0.2, 1.2  # x-axis bounds
y0, y1 = -0.2, 1.2     # y-axis bounds
xs = np.linspace(x0, x1, N)
ys = np.linspace(y0, y1, N)
# Placeholder for data
data = np.zeros((N, N))
# Implement the banana function on data 
# Plot starter code
plt.figure(figsize=(8,8))
im = plt.imshow(data, extent=(x0, x1, y0, y1), origin='lower', cmap=matplotlib.cm.gray)
plt.colorbar(im, orientation='vertical', fraction=0.03925, pad=0.04)

# HERE HERE HERE
