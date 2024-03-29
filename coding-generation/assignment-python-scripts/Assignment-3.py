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
import matplotlib.pyplot as plt

# Define a function to calculate the mean lifetime from the half-life.
def meanLifetime(halfLife):
    return halfLife / np.log(2)

# Half-life of Carbon-14 in years.
T_HALF = 5730.
TAU = meanLifetime(T_HALF)

# Function for the radioactive decay process.
def f_rad(N, t):
    return -N / TAU

# Analytical solution of the decay equation.
def analytic(N0, t):
    return N0 * np.exp(-t/TAU)

# Euler's method for solving the ODE.
def solve_euler(f, n0, t0, dt, n_steps):
    n_t = np.empty((n_steps+1))
    n = n0
    t = t0
    for i in range(n_steps+1):
        n_t[i] = n
        n += dt * f(n, t)
        t += i * dt
    return n_t

# RK4 method for solving the ODE.
def solve_RK4(f, n0, t0, dt, n_steps):
    ans = np.zeros((n_steps + 1))
    ans[0] = n0
    t = t0
    for i in range(1, len(ans)):
        k1 = f(ans[i - 1], t)
        k2 = f(ans[i - 1] + (dt * k1)/2, t + (dt/2))
        k3 = f(ans[i - 1] + (dt * k2)/2, t + (dt/2))
        k4 = f(ans[i - 1] + (dt * k3), t + dt)
        ans[i] = ans[i - 1] + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
        t += dt
    return ans

# ::: Task :::
# Compare the errors in Euler's and RK4 methods through a log-log plot.

# Objective:
# 1. Plot the error versus the number of steps for both Euler's method (solve_euler) and RK4 method (solve_RK4) using a log-log scale.
# 2. Calculate the error by comparing the results of both methods with the analytical solution.
# 3. Ensure the plot includes appropriate legends, axis labels, and a descriptive title.

# Suggestions:
# - Choose a range of step counts that effectively demonstrate the error trends in both methods.
# - Use different colors or markers for each method to enhance plot clarity.
# - Ensure the axis labels and plot title are informative and accurately describe the plotted data.

# HERE HERE HERE
