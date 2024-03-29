# Welcome to the Physics Coding Assignment on Root finding.
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
from matplotlib import pyplot as plt
import matplotlib.colors
from random import random

# Function implementing the Newton-Raphson method. 
def NewtonRaphson(f, df, x0, tol, max_iter=100):
    xs = [x0]
    x = x0
    for _ in range(max_iter):
        dx = -f(x) / df(x)
        x += dx
        xs.append(x)
        if abs(dx) < tol:
            break
    return xs

# Function implementing the bisection method.
def bisect(f, a, b, tol, max_iter=100):
    xs = []
    for _ in range(max_iter):
        x = (a + b) / 2.0
        xs.append(x)
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        if abs(b - a) < tol:
            break
    return xs

# Function implementing the secant method.
def secant(f, x0, x1, tol, max_iter=100):
    xs = [x0, x1]
    for _ in range(max_iter):
        x = xs[-1] - f(xs[-1]) * (xs[-1] - xs[-2]) / (f(xs[-1]) - f(xs[-2]))
        xs.append(x)
        if abs(xs[-1] - xs[-2]) < tol:
            break
    return xs

# Function and its derivative
def f(x): 
    return x-numpy.tanh(2*x)

def df(x): 
    return 1.0-2.0/numpy.cosh(2*x)**2

# ::: Task :::
# Compare the convergence efficiency of three root-finding methods: `NewtonRaphson`, `secant`, and `bisect`.

# Objective:
# 1. Plot a graph comparing the convergence of the above `NewtonRaphson()`, `secant()`, and `bisect()` functions for finding the root of the function 'f(x)' at `[0.9575040240772687, 0]`.
# 2. The plot should illustrate the evolution of the error with increasing iterations for each method.
# 3. Ensure the plot includes labels, a descriptive title, and a legend to differentiate between the methods. [4 marks]

# Suggestions:
# - Use different colors or styles for each method to clearly distinguish their convergence patterns on the graph.
# - Consider a logarithmic scale if it enhances the visualization of the convergence.
# - Make sure the axis labels, title, and legend are informative and accurately reflect the contents of the plot.

# HERE HERE HERE
