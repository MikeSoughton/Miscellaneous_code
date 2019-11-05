"""
    Tests the time for calculations
"""

import time
import random
import numpy as np
import matplotlib.pyplot as plt

# The number of calculations to compute times for
n_calcs = np.logspace(0,7,11)

# ==================== COMPARING TIMES FOR ZERO FLOAT MULTIPLICATION VS RANDOM FLOAT MULTIPLICATION ====================

def zero_float(n_calcs):
    # Create the floats beforehand then multiply them since creating them does take time (although almost negligible)
    # This is not actually the best way to go about this, since it does take some small amount of time to read through entries of a list
    f1s = []
    f2s = []
    for i in range(int(n_calcs)):
        f1s.append(0.0)
        f2s.append(0.0)

    # Now multiply floats
    t0 = time.time()
    for i in range(len(f1s)):
        result = f1s[i]*f2s[i]

    t_end = time.time()
    T = t_end - t0
    return T

def random_float(n_calcs):
    # Create the floats beforehand then multiply them since creating them does take time (although almost negligible)
    f1s = []
    f2s = []
    for i in range(int(n_calcs)):
        f1s.append(random.random())
        f2s.append(random.random())

    # Now multiply floats
    t0 = time.time()
    for i in range(len(f1s)):
        result = f1s[i]*f2s[i]

    t_end = time.time()
    T = t_end - t0
    return T

# The same functions including the time to create the floats
def zero_float_create(n_calcs):
    t0 = time.time()
    for i in range(int(n_calcs)):
        f1 = 0.0
        f2 = 0.0
        result = f1*f2
    t_end = time.time()
    T = t_end - t0
    return T

def random_float_create(n_calcs):
    t0 = time.time()
    for i in range(int(n_calcs)):
        f1 = random.random()
        f2 = random.random()
        result = f1*f2
    t_end = time.time()
    T = t_end - t0
    return T

zero_float_time = np.zeros(len(n_calcs))
random_float_time = np.zeros(len(n_calcs))
zero_float_time_create = np.zeros(len(n_calcs))
random_float_time_create = np.zeros(len(n_calcs))

for idx,n_calc in enumerate(n_calcs):
    zero_float_time[idx] = zero_float(n_calc)
    random_float_time[idx] = random_float(n_calc)
    zero_float_time_create[idx] = zero_float_create(n_calc)
    random_float_time_create[idx] = random_float_create(n_calc)

plt.close("all")

plt.figure(1)
plt.plot(n_calcs, zero_float_time, label = r"Zero float multiplication")
plt.plot(n_calcs, random_float_time, label = r"Random float multiplication")
plt.plot(n_calcs, zero_float_time_create, label = r"Zero float multiplication including float creation time")
plt.plot(n_calcs, random_float_time_create, label = r"Random float multiplication including float creation time")
plt.xlabel(r"Number of calculations")
plt.ylabel(r"Time (S)")
plt.title(r"Time for calculations")
plt.grid()
plt.legend(loc = "best")


# ============== COMPARING TIMES FOR ZERO FLOAT ARRAY MULTIPLICATION VS RANDOM FLOAT ARRAY MULTIPLICATION ==============

# How does calculation time scale for vector, matrix or tensor calculations? How is this different between different libraries e.g. scipy, numpy, tensorflow?

# Really I should create the arrays beforehand then multiply them since creating them does take time

def zero_float_array(n_calcs, array_dim):
    # Create the arrays beforehand then multiply them since creating them does take time
    f1s = []
    f2s = []
    for i in range(int(n_calcs)):
        f1s.append(np.zeros([array_dim[0], array_dim[1]]))
        f2s.append(np.zeros([array_dim[0], array_dim[1]]))

    # Now multiply arrays
    t0 = time.time()
    for i in range(len(f1s)):
        result = f1s[i]*f2s[i]

    t_end = time.time()
    T = t_end - t0
    return T

def random_float_array(n_calcs, array_dim):
    # Create the arrays beforehand then multiply them since creating them does take time
    f1s = []
    f2s = []
    for i in range(int(n_calcs)):
        f1s.append(np.random.rand(array_dim[0], array_dim[1]))
        f2s.append(np.random.rand(array_dim[0], array_dim[1]))

    # Now multiply arrays
    t0 = time.time()
    for i in range(len(f1s)):
        result = f1s[i] * f2s[i]

    t_end = time.time()
    T = t_end - t0
    return T

# The same functions including the time to create the floats
def zero_float_array_create(n_calcs, array_dim):
    t0 = time.time()
    for i in range(int(n_calcs)):
        f1 = np.zeros([array_dim[0], array_dim[1]])
        f2 = np.zeros([array_dim[0], array_dim[1]])
        result = f1*f2

    t_end = time.time()
    T = t_end - t0
    return T

def random_float_array_create(n_calcs, array_dim):
    t0 = time.time()
    for i in range(int(n_calcs)):
        f1 = np.random.rand(array_dim[0], array_dim[1])
        f2 = np.random.rand(array_dim[0], array_dim[1])
        result = f1*f2

    t_end = time.time()
    T = t_end - t0
    return T

zero_float_array_time = np.zeros(len(n_calcs))
random_float_array_time = np.zeros(len(n_calcs))
zero_float_array_time_create = np.zeros(len(n_calcs))
random_float_array_time_create = np.zeros(len(n_calcs))

array_dim = (3,3)

for idx,n_calc in enumerate(n_calcs):
    zero_float_array_time[idx] = zero_float_array(n_calc, array_dim)
    random_float_array_time[idx] = random_float_array(n_calc, array_dim)
    zero_float_array_time_create[idx] = zero_float_array_create(n_calc, array_dim)
    random_float_array_time_create[idx] = random_float_array_create(n_calc, array_dim)

plt.figure(2)
plt.plot(n_calcs, zero_float_array_time, label = r"Zero float array multiplication")
plt.plot(n_calcs, random_float_array_time, label = r"Random float array multiplication")
plt.plot(n_calcs, zero_float_array_time_create, label = r"Zero float array multiplication including float creation time")
plt.plot(n_calcs, random_float_array_time_create, label = r"Random float array multiplication including float creation time")
plt.xlabel(r"Number of calculations")
plt.ylabel(r"Time (S)")
plt.title(r"Time for calculations")
plt.grid()
plt.legend(loc = "best")
plt.show(block=False)