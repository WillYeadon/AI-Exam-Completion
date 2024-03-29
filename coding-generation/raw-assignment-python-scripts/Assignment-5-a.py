# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy as np
from matplotlib import pyplot as plt
import random

# Implement a function that tells whether a transition has occured, based on the transition probability and a random number. Use the random number `r` from `random.random()` and use the procedure described in the notes so that the checks can work in a reproducible way.
def has_transitioned(prob):
    r = random.random()
    return r < prob

# Define a function that takes as arguments the current state and a list of such transition rules and implements the transition (or not) and returns the new state
def evolveOne(currentState, rules):
    for initial_state, final_state, probability in rules:
        if currentState == initial_state:
            if has_transitioned(probability):
                return final_state
    return currentState

# Now implement a function that takes a list of states and transition them according to the rules passed as argument. This function should return a new vector of states, it should not modify the state passed as an argument!
def evolveMany(states, rules):
    return [evolveOne(state, rules) for state in states]

# Define a function that evolves a system that starts with initial amounts `NA`, `NB` and `NC` of $A$, $B$ and $C$ nuclei and evolved it in `n_timestep` from time $t=0$ to $t=t_{max}$. The function should return three arrays, one for each atom type, of the number of nuclei of that type at each time step. Each array should contain `n_timestep+1` elements including the initial amount. 
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

# ::: Task ::: Create a plot with the number of $A$, $B$ and $C$ nuclei, starting with 250 $C$ nuclei and evolving the system for 100 hours using 200 steps and with neutron flux on. Evolve the system for another 100 hours (using 200 steps) without neutron flux (i.e. no transitions from $C$ to $A$).
# The half life of the $A$ atoms is 10.1 hours, the half life of $B$ nuclei is 15.7 hours and we can caracterise the rate of activation of $C$ into $A$ when the neutron flux is on with and effective half-life of 3.2 hours.
# The plot should have the appropriate labels and legend. [8 marks]   
#
n_steps = 200
t_total = 100
dt = t_total/n_steps

t_half_A = 10.1
t_half_B = 15.7
t_half_C = 3.2

# HERE HERE HERE