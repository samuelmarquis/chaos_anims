from parameters import *
np.set_printoptions(suppress=True,precision=3)
song, sr, _, duration_f, duration_s = load_song("audio/test/sweep.wav")
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sympy.vector import *

A = Matrix([[2, 0], [0,1]])
B = Matrix([[1, 1], [0,1]])

x, y = symbols('x y')
point = Matrix([x, y])

AB = A*B
BA = B*A

print(BA)
print(AB)

# Apply the transformations in the reverse order: first A, then B
transformed_point = B * (A * point)

# Print the transformed point
print("\nTransformed point:")
print(transformed_point)

# Apply the transformation represented by BA directly to the point
directly_transformed_point = BA * point

# Print the directly transformed point
print("\nDirectly transformed point:")
print(directly_transformed_point)
