# Welcome to the Physics Coding Assignment on Monte Carlo methods for nuclei decay and activation.
# Please follow these steps to complete your assignment:
#
# 1. Read the section marked '::: Task :::' section to understand the primary goal of the assignment.
# 2. Implement your solution in the designated area marked 'HERE HERE HERE'.
# 3. Ensure to use 'plt.show()' after your plotting commands to display the results.
# 4. Your final plots should be visible and clear for assessment.
#
# Do not write comments, just the code to complete the assignment.
# Remember, a successful completion of the task involves not only writing functional code
# but also adhering to the given instructions and requirements. Good luck!

import numpy as np
from matplotlib import pyplot as plt
import random

# Function to determine if a transition occurs based on the transition probability
def has_transitioned(prob):
    r = random.random()
    return r < prob

# Function to evolve a single state according to the transition rules
def evolveOne(currentState, rules):
    for initial_state, final_state, probability in rules:
        if currentState == initial_state:
            if has_transitioned(probability):
                return final_state
    return currentState

# Function to evolve a list of states
def evolveMany(states, rules):
    return [evolveOne(state, rules) for state in states]

# Function to evolve the entire system over 'n_steps'
def evolve_system(NA, NB, NC, rules, n_steps):
    state = ['A'] * NA + ['B'] * NB + ['C'] * NC
    A_count = np.empty(n_steps + 1, dtype=int)
    B_count = np.empty(n_steps + 1, dtype=int)
    C_count = np.empty(n_steps + 1, dtype=int)
    A_count[0], B_count[0], C_count[0] = NA, NB, NC

    for step in range(n_steps):
        state = evolveMany(state, rules)
        A_count[step + 1] = state.count('A')
        B_count[step + 1] = state.count('B')
        C_count[step + 1] = state.count('C')

    return A_count, B_count, C_count

# Below is a simulation of the number of 'A', 'B' and 'C' nuclei,
# starting with 250 'C' nuclei and evolving the system for 100 hours using 200 steps and with neutron flux on.
# The system is evolved for another 100 hours (using 200 steps) without neutron flux (i.e. no transitions from 'C' to 'A').
#
# The half life of the 'A' atoms is 10.1 hours, the half life of 'B' nuclei is 15.7 hours 
# and we can caracterise the rate of activation of 'C' into 'A' when the neutron flux is on 
# with and effective half-life of 3.2 hours.

t_half_A = 10.1  # Half-life of A atoms in hours
t_half_B = 15.7  # Half-life of B nuclei in hours
t_half_C = 3.2   # Effective half-life of C to A transition in hours when neutron flux is on
t_total = 100    # Total time for each phase in hours
n_steps = 200    # Number of steps in each phase
dt = t_total / n_steps # dt step calculation

# Define transition probabilities
prob_A_to_B = 1 - np.exp(-dt * np.log(2) / t_half_A)
prob_B_to_C = 1 - np.exp(-dt * np.log(2) / t_half_B)
prob_C_to_A_on = 1 - np.exp(-dt * np.log(2) / t_half_C)
prob_C_to_A_off = 0

# Define transition rules with and without neutron flux
neutronFlux = [
    ('A', 'B', prob_A_to_B),
    ('B', 'C', prob_B_to_C),
    ('C', 'A', prob_C_to_A_on)
]

noNeutronFlux = [
    ('A', 'B', prob_A_to_B),
    ('B', 'C', prob_B_to_C)
]

def simulation():
    flux = evolve_system(0, 0, 250, neutronFlux, t_total)
    noflux = evolve_system(flux[0][-1], flux[1][-1], flux[2][-1], noNeutronFlux, t_total)

    As = np.concatenate((flux[0], noflux[0]))
    Bs = np.concatenate((flux[1], noflux[1]))
    Cs = np.concatenate((flux[2], noflux[2]))
    return As, Bs, Cs

As, Bs, Cs = simulation()

# ::: Task ::: 
# Run the above function 'simulation()' 20 times and use the results to calculate an average and uncertainty on the number of 'A' atoms as a function of time. Use `plt.errorbar` for the plot. You might be interested in the `numpy.average` and `numpy.std` functions. The plot should have axis labels and a title. [6 marks]

nsim = 20
# HERE HERE HERE