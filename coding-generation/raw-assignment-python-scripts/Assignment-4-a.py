# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy as np
from matplotlib import pyplot as plt

# Define constants for the simulation
r_cb = 0.15  # Radius of cannonball in m
rho_iron = 7874  # Density of iron in kg/m^3
g = 9.81  # Acceleration due to gravity in m/s^2
kappa = 0.47  # Drag coefficient of a sphere
rho_air = 1.23  # Density of air in kg/m^3
v0 = 125.00  # Initial speed in m/s

# From this information, calculate the following two variables:
def get_area(r):
    area = numpy.pi * r**2  # Cross sectional area of sphere
    return area

def get_mass(r):
    mass = rho_iron * (4/3) * numpy.pi * r**3  # Mass of sphere
    return mass

area_cb = get_area(r_cb)
mass_cb = get_mass(r_cb)

def f(state, t):
    x, y, vx, vy = state
    v = np.sqrt(vx**2 + vy**2)
    k = 0.5 * rho_air * kappa * area_cb
    
    dx_dt = vx
    dvx_dt = -(k/mass_cb)*v*vx
    dy_dt = vy
    dvy_dt = -(k/mass_cb)*v*vy - g
    
    return np.array([dx_dt, dy_dt, dvx_dt, dvy_dt])

def solve_euler(state_initial, t1, n_steps):
    history = np.empty((n_steps+1, 4))
    history[0] = state_initial
    dt = t1 / n_steps
    
    for i in range(n_steps):
        t = i * dt
        history[i+1] = history[i] + f(history[i], t) * dt
    
    return history

# To find the range of the projectile we will look for the $x$ coordinate when the trajectory crosses the $y=0$ line. In most cases that point will not be one of the steps but will be between two steps. We will use a linear approximation to determine this point given the last point with a positive $y$ value and the first point with a negative $y$ value. Implement the function `find_zero_linear` that takes as argument the two values of $x$ `x1` and `x2` and the heights `y1` and `y2` and returns the value of $x$ at which the line between $(x_1,y_1)$ and $x_2,y_2$ crosses the $y=0$ line.
def find_zero_linear(x1, x2, y1, y2):
    return (x1*y2 - x2*y1) / (y2 - y1)

# Given the function above we can use it in another function to determine the range.
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

# ::: Task ::: Create a plot to show the trajectories for different values of the initial angle. Use the same velocity $v_0=125\rm{m/s}$ for all angles. The plot should have axis labels and a title. [4 marks]

n_steps = 1000
thetas = range(5, 90, 5)  # Angles in degrees
# HERE HERE HERE