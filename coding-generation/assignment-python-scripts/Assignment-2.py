# Welcome to the Physics Coding Assignment on numerical integration and its accuracy .
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
import matplotlib.pyplot as plt

# Define the function f(x) = x^2 * cos(2x).
def f(x):
    return x**2 * np.cos(2*x)

# Define the analytical integral of f.
def g(x):
    return 0.5 * x * np.cos(2*x) + 0.25*(2*x**2-1) * np.sin(2*x)

# Function to calculate the analytical integral from xmin to xmax.
def integrate_analytic(xmin, xmax):
    return g(xmax) - g(xmin)

# Function to calculate the numerical integral using Simpson's rule.
def integrate_numeric(xmin, xmax, N):
    xs = np.linspace(xmin, xmax, 2 * N + 1)
    ys = f(xs)
    coefficients = np.array(([2.0, 4.0] * N) + [1.0])
    coefficients[0] = 1.0
    coefficients[2 * N] = 1.0
    panel_width = (xmax - xmin) / float(N)
    return 1.0/6.0 * panel_width * sum(coefficients * ys)

# ::: Task :::
# Investigate the fractional error in numerical analysis compared to analytical results across varying panel counts.

# Objective:
# 1. Create a log-log plot showing the fractional error between the numerical and analytical results as the number of panels is varied.
# 2. Ensure the plot includes labels, a descriptive title, and utilizes a log-log scale.
# 3. Determine appropriate panel counts and calculate errors for each panel count.
# 4. Include a legend in the plot if necessary.
# Suggested panel counts: [4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Suggestions:
# - Select a range of panel counts that effectively demonstrate the trend in fractional error.
# - Consider using different colors or styles in the plot for clarity.
# - Pay attention to the readability of the axes labels and the plot title.

# HERE HERE HERE