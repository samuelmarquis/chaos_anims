import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# Define the control points
points = np.array([[0, 0], [0.2, 0.5], [0.4, 0.2], [0.21, 0.4], [1, 1]])

# Sort the control points by their x-coordinates
points = points[points[:, 0].argsort()]

# Create a cubic spline interpolation
cs = CubicSpline(points[:, 0], points[:, 1])

# Sample the curve at 256 points
x = np.linspace(0, 1, 256)
y = cs(x)

# Plot the curve
plt.plot(x, y)
plt.scatter(points[:, 0], points[:, 1], c='r')
plt.show()