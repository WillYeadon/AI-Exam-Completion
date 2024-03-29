# Welcome to the Physics Coding Assignment on Random Walks.
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

# Definition of Walker class
class walker:
    def __init__(self,x0,ndim=1, step_size=1.0):
        self.pos=x0
        self.ndim=ndim
        self.possibleSteps=[]
        for i in range(ndim):
            step=numpy.zeros(ndim)
            step[i]= - step_size
            self.possibleSteps.append(numpy.array(step,dtype='f'))
            step[i]= + step_size
            self.possibleSteps.append(step.copy())
        self.npossible=len(self.possibleSteps)

    def pickStep(self):
        istep = numpy.random.choice(range(self.npossible))
        return self.possibleSteps[istep]
        
    def doSteps(self,n):
        positions=numpy.ndarray((n+1,self.ndim),dtype='f')
        positions[0] = self.pos
        for i in range(n):
            step = self.pickStep()
            self.pos += step
            positions[i+1] = self.pos
        return positions

# ::: Task ::: 
# Simulate the diffusion of 1000 particles (walkers) randomly distributed within the unit square.
# The initial positions of these particles are given in the array `rand_pos`. Each particle moves with a step size of 0.05. 
# 
# Objective:
# 1. Plot the position of the walkers after 10, 100, and 500 steps separately on each subplot: plt.subplot(1, 3, 1), plt.subplot(1, 3, 2) and plt.subplot(1, 3, 3).
# 2. Each plot should be clearly labeled with the number of steps and have a descriptive title.
# 3. Use different colors to distinguish the plots for different step counts.
# 
# Suggestions:
# - Utilize `plt.scatter` for plotting. Adjust the `alpha` parameter to enhance plot aesthetics.
# - Allocate 6 marks for this task.
# 
# Starter Code:
ndim = 2
nwalkers = 1000  # Note: Adjusted to match the task description
rand_pos = numpy.random.uniform(size=(nwalkers, ndim))
colours = ['red', 'green', 'blue']

plt.figure(figsize=(18,6))
for i, step_count in enumerate([10, 100, 500]): 
    plt.subplot(1, 3, i+1)
    plt.title(f"Positions after {step_count} steps")
    plt.xlim((-3, 4))
    plt.ylim((-3, 4))
    # Initial scatter plot for starting positions
    plt.scatter(rand_pos[:,0], rand_pos[:,1], color = colours[i])
    # HERE HERE HERE