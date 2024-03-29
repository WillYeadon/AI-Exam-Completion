# Please read this script and then complete the plot described by the text
# labelled '::: Task :::' writing your code where the script says 'HERE HERE HERE'

# First we need to import a few modules, execute the cell below:
import numpy
import matplotlib.pyplot as plt

# Define a function `f` that is equivalent to $f(x)=\sin(2x)$. 
# It should work both for single arguments and `numpy` arrays.
def f(x):
    return numpy.sin(2 * x)

# Define the analytic derivative of the function`f` here (again, it should work both for single numbers and numpy arrays).
def df_analytic(x):
    return 2 * numpy.cos(2 * x)

# Now define the numerical derivative using the forward difference method. The function `forward_difference` takes three arguments, `f`, the function to calculate the derivative for, `x` the position to calculate the derivative at and `dx` the interval length.
def forward_difference(f, x, dx):
    return (f(x + dx) - f(x)) / dx

# ::: Task ::: Here is a skeleton code to plot the difference between the analytical derivative and the numerical implementation. Modify and expand it to provide a plot with three curves for the difference for a case where $dx$ is too large, about right and too small. The plot should have a legend, labelled axes and a title.

xs = numpy.linspace(-2*numpy.pi,2*numpy.pi,100)
df_dx_1 = forward_difference(f, xs, dx=1e-4)
df_dx_2 = forward_difference(f, xs, dx=1e-6)
df_dx_analytical = df_analytic(xs)
plt.figure(figsize=(8, 4))
plt.plot(xs, df_dx_1 - df_dx_analytical)
plt.plot(xs, df_dx_2 - df_dx_analytical)

# HERE HERE HERE