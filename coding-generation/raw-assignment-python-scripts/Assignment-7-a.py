# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors
from random import random

# Implement the Newton-Raphson method below. 
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

# Implement the bisection method below.
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

# Implement the secant method below.
def secant(f, x0, x1, tol, max_iter=100):
    xs = [x0, x1]
    for _ in range(max_iter):
        x = xs[-1] - f(xs[-1]) * (xs[-1] - xs[-2]) / (f(xs[-1]) - f(xs[-2]))
        xs.append(x)
        if abs(xs[-1] - xs[-2]) < tol:
            break
    return xs

def f(x): 
    return x-numpy.tanh(2*x)

def df(x): 
    return 1.0-2.0/numpy.cosh(2*x)**2

# ::: Task ::: We are now going to look at the three methods and see how they compare. Plot a graph that compares the convergence of the Newton-Raphson, Secant, and Bisection methods for finding roots of the function $f(x) = x - \tanh(2x)$.
# HERE HERE HERE
