# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

import numpy
import numpy as np
from matplotlib import pyplot as plt 

# To do our work we will implement a walker class. When initialised a list of possible steps is populated. In one dimension it is
# [+s] , [-s] 
# where s is the step size, it defaults to 1 but can be set as an argument in the constructor. In two dimensions the steps list contains
# [ +s , 0 ] , [ -s , 0 ] ,  [ 0 , +s ] , [ 0 , -s ]
# At each step the current position of the walker, saved in `self.pos`, is updated by adding one of the possible steps. The function `pickStep` chooses randomly one of the possible steps. Use this function to implement the `doSteps` function that performs `n` steps and returns a `(n+1) x ndim` array representing the trajectory of the walker, including the starting point. 

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

# ::: Task ::: Make a plot of average position and average squared position of 100 1D walkers using 1000 steps. Your plot needs a legend, title and labels. [5 marks]
#
# HERE HERE HERE