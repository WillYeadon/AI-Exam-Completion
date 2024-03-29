# Welcome to the Physics Coding Assignment on trajectories of a cannonball.
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

# Define constants for the simulation
r_cb = 0.15  # Radius of cannonball in m
rho_iron = 7874  # Density of iron in kg/m^3
g = 9.81  # Acceleration due to gravity in m/s^2
kappa = 0.47  # Drag coefficient of a sphere
rho_air = 1.23  # Density of air in kg/m^3
v0 = 125.00  # Initial speed in m/s

# Function to calculate cross-sectional area of a sphere
def get_area(r):
    return np.pi * r**2

# Function to calculate the mass of an iron sphere
def get_mass(r):
    return rho_iron * (4/3) * np.pi * r**3

# Calculating area and mass of the cannonball
area_cb = get_area(r_cb)
mass_cb = get_mass(r_cb)

# Function to model cannonball's motion
def f(state, t):
    x, y, vx, vy = state
    v = np.sqrt(vx**2 + vy**2)
    k = 0.5 * rho_air * kappa * area_cb
    
    dx_dt = vx
    dvx_dt = -(k/mass_cb)*v*vx
    dy_dt = vy
    dvy_dt = -(k/mass_cb)*v*vy - g
    
    return np.array([dx_dt, dy_dt, dvx_dt, dvy_dt])

# Euler's method for solving the ODE
def solve_euler(state_initial, t1, n_steps):
    history = np.empty((n_steps+1, 4))
    history[0] = state_initial
    dt = t1 / n_steps
    
    for i in range(n_steps):
        t = i * dt
        history[i+1] = history[i] + f(history[i], t) * dt
    
    return history

# Function to find the x-coordinate where the trajectory crosses y=0
def find_zero_linear(x1, x2, y1, y2):
    return (x1*y2 - x2*y1) / (y2 - y1)

# Function to find the range of the projectile
def find_range(history):
    all_xs = history[:, 0]
    all_ys = history[:, 1]
    negatives = np.argwhere(all_ys < 0)
    if len(negatives) == 0:
        return all_xs[-1]
    index = negatives[0]
    y1, y2 = all_ys[index-1], all_ys[index]
    x1, x2 = all_xs[index-1], all_xs[index]
    return find_zero_linear(x1, x2, y1, y2)

# Stores the trajectories for different values of the initial angle. 
# Uses the same velocity v0=125 m/s for all angles. 
n_steps = 1000
thetas = range(5, 90, 5)
results = {}

for theta in thetas:
    v_y = 125 * np.sin(np.deg2rad(theta))
    v_x = 125 * np.cos(np.deg2rad(theta))
    initial_conditions = [0, 0, v_x, v_y]
    values_euler = solve_euler(initial_conditions, 300, n_steps)
    xs_euler, ys_euler = values_euler[:,0], values_euler[:,1]
    
    # Store the values in the results dictionary
    results[theta] = (xs_euler, ys_euler)

# ::: Task :::
# Analyze the effect of initial velocity on the range of a projectile, both with and without air resistance.

# Objective:
# 1. Plot the range for different initial velocities using a constant angle of theta=60 degrees.
# 2. Generate two curves for each velocity: one considering air resistance and the other without air resistance.
# 3. Ensure the plot includes axis labels, a descriptive title, and a legend to distinguish between the curves.

# Suggestions:
# - Select a range of initial velocities that effectively demonstrate the differences in range.
# - Use distinct styles or colors for the curves with and without air resistance for clarity.
# - Make sure the axis labels, title, and legend accurately convey the information being presented in the plot.

# Starter Code:
n_steps = 1000
max_time = 300
v0s = np.linspace(50, 1000, 20)  # Range of velocities
# HERE HERE HERE