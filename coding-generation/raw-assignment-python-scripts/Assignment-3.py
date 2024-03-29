# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy as np
import matplotlib.pyplot as plt

# define a function to calculate the mean lifetime from the half life
def meanLifetime(halfLife):
    return halfLife / np.log(2)

T_HALF = 5730.
TAU = meanLifetime(T_HALF)

# Implement the function `f_rad` such that the differential equation 
# $$ \frac{dN}{dt} = f_{rad}(N,t)$$
# describes the radioactive decay process.
# Your function should return values using years as the time unit.*
# The function should use the constant* `TAU`.
def f_rad(N, t):
    return -N / TAU

# Solve this first order, ordinary differential equation analytically. Implement this function below, naming it `analytic`. The function should take an initial number of atoms `N0` at time `t=0`, and a time argument. The function should return nuclei count at the time argument. Make sure the function also works for numpy arrays.
def analytic(N0, t):
    return N0 * np.exp(-t/TAU)

# Create a function which takes as its arguments the initial number of atoms, `n0`, the initial time `t0`, the time step, `dt`, and the number of steps to perform, `n_steps`.  This function should return an array of the number of counts at each time step using Euler's method. This array should contain the initial and final values, so the array length should be `n_steps+1` 
def solve_euler(f, n0, t0, dt, n_steps):
    n_t = np.empty((n_steps+1))
    n = n0
    t = t0
    for i in range(n_steps+1):
        n_t[i] = n
        n += dt * f(n, t)
        t += i * dt
    return n_t

# Implement the RK4 method in the `solve_RK4` function. The arguments are the same as for `solve_euler`.
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

# ::: Task ::: Create a plot to show that the RK4 method has an error that scales better with the number of steps than the Euler method. [5 marks]
# HERE HERE HERE