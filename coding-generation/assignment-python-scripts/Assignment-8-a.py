# Welcome to the Physics Coding Assignment on Random Walks.
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
# Analyze the movement of 1D walkers through a plot of average position and average squared position.

# Objective:
# 1. Simulate 100 1D walkers, each using 1000 steps.
# 2. Plot the average position and the average squared position of these walkers.
# 3. Ensure your plot includes a legend, a descriptive title, and labels for each axis. [5 marks]

# Suggestions:
# - Consider using different colors or markers to distinguish between the average position and the average squared position on the plot.
# - Ensure the plot scales are appropriate to clearly display the data trends.
# - Make the legend, title, and axis labels informative to accurately convey the plot's data and purpose.

# HERE HERE HERE