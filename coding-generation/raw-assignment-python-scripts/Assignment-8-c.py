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

# A simulation of average position and average squared position of 100 1D 
# walkers using 1000 steps. 
nsteps = 100
nwalkers = 1000
pos = np.zeros((nwalkers, nsteps + 1))
sqa = np.zeros((nwalkers, nsteps + 1))
for i in range(nwalkers):
    w = walker(numpy.zeros(1))
    ys = w.doSteps(nsteps)
    pos[i] = ys[:,0]
    sqa[i] = ys[:,0]**2
    
# A simulation showing that the average squared distance scaling is independent
# of the dimension in which the walker moves. Uses 100 steps and 400 walkers
# and uses $D=1,2,3,4$.
nsteps = 100
nwalkers = 400
for dim in range(1,5):
    sqa = np.zeros((nwalkers, nsteps + 1))
    for i in range(nwalkers):
        w = walker(numpy.zeros(1), dim)
        ys = w.doSteps(nsteps)
        sqa[i] = np.sum(ys**2, axis = 1)

# ::: Task ::: Use 1000 walkers randomly distributed in the unit square (the positions are given in the array `rand_pos`) simulate the diffusion of particles with step size 0.05. Make a plot of the position of the walkers after 10, 100 and 500 steps. The plots should have labels and titles.
ndim = 2
nwalkers = 500
rand_pos = numpy.random.uniform(size=(nwalkers, ndim))
colours = ['red','green', 'blue']

plt.figure(figsize=(18,6))
for i in range(3): 
    plt.subplot(1, 3, i+1)
    plt.title(f"Plot {i+1}")
    plt.xlim((-3, 4))
    plt.ylim((-3, 4))
    plt.scatter(rand_pos[:,0], rand_pos[:,1], color = colours[i])
# HERE HERE HERE
