# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy as np
import matplotlib.pyplot as plt

# Define the function `f`, such that $\textrm{f}(x) \equiv x^{2}\cos(2x)$. This is the function that we will be integrating.
def f(x):
    return x**2 * np.cos(2*x)

# Derive the indefinite integral of $f(x)$ analytically. Call this function $g(x)$ and implement it below. Set the constant of integration such that $g(0)=0$.
def g(x):
    return 0.5 * x * np.cos(2*x) + 0.25*(2*x**2-1) * np.sin(2*x)

# Now, using the analytically derived indefinite integral, $g(x)$, define a function which calculates the definite integral of $f(x)$ over the interval $(x_{min},~x_{max})$.
def integrate_analytic(xmin, xmax):
    return g(xmax) - g(xmin)

# Create a function which calculates the definite integral of the function $f(x)$ over the interval $(x_{min},~x_{max})$ using Simpson's rule with $N$ panels.
def integrate_numeric(xmin, xmax, N):
    xs = np.linspace(xmin, xmax, 2 * N + 1)
    ys = f(xs)
    coefficients = np.array(([2.0, 4.0] * N) + [1.0])
    coefficients[0] = 1.0
    coefficients[2 * N] = 1.0
    panel_width = (xmax - xmin) / float(N)
    return 1.0/6.0 * panel_width * sum(coefficients * ys)


# ::: Task ::: There will always be some discrepancy between a numerically calculated result and an analytically derived result. Produce a log-log plot showing the fractional error between these two results as the number of panels is varied. The plot should have labels and a title.
x0, x1 = 0, 2  # Bounds to integrate f(x) over
panel_counts = [4, 8, 16, 32, 64, 128, 256, 512, 1024]  # Panel numbers to use
result_analytic = integrate_analytic(x0, x1)  # Define reference value from analytical solution
# HERE HERE HERE