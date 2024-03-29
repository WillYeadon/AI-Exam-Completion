# Welcome to the Physics Coding Assignment on the difference between analytical and numerical derivatives.
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

import numpy
import matplotlib.pyplot as plt

# Define the function f(x) = sin(2x).
def f(x):
    return numpy.sin(2 * x)

# Define the analytical derivative of f.
def df_analytic(x):
    return 2 * numpy.cos(2 * x)

# Implement the forward difference method for numerical differentiation.
def forward_difference(f, x, dx):
    return (f(x + dx) - f(x)) / dx

# ::: Task :::
# Investigate the accuracy of numerical derivatives by comparing them with the analytical derivative.

# Objective:
# 1. Plot the difference between the analytical derivative and the numerical derivative for three different values of dx.
# 2. Include a legend, labelled axes, and a descriptive title in your plot.
# Note: You are responsible for determining appropriate values for dx and other plot details.

# Suggestions:
# - Choose the third value of dx judiciously to highlight differences in the accuracy of the numerical derivative.
# - Consider using plot styles and colors to make the comparison clear and visually engaging.
# - Make sure the axes are properly labeled to reflect what is being plotted.

# Starter Code:
xs = numpy.linspace(-2 * numpy.pi, 2 * numpy.pi, 100)
# Calculate numerical derivatives with different dx values.
df_dx_1 = forward_difference(f, xs, dx=1e-4)
df_dx_2 = forward_difference(f, xs, dx=1e-6)
# Calculate the analytical derivative.
df_dx_analytical = df_analytic(xs)
# Create the initial plot setup.
plt.figure(figsize=(8, 4))
plt.plot(xs, df_dx_1 - df_dx_analytical, label='dx=1e-4')
plt.plot(xs, df_dx_2 - df_dx_analytical, label='dx=1e-6')

# HERE HERE HERE