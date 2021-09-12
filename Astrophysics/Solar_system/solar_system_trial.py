#!/usr/bin/python

"""
    My solar system
"""

# ============================ Import modules ==================================
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

import argparse

# ========================= Take and or define parameters ======================
parser = argparse.ArgumentParser(description='These are the arguments that will be passed to the script.')

parser.add_argument("--sun_init_coords",
                    type=float,
                    default=[0,0,0],
                    help="float: The initial xyz coordinates of the Sun.")

parser.add_argument("--sun_init_vel",
                    type=float,
                    default=[0,0,0],
                    help="float: The initial xyz velocity of the Sun.")

parser.add_argument("--earth_init_coords",
                    type=float,
                    default=[1,0,0],
                    help="float: The initial xyz coordinates of the Sun.")

parser.add_argument("--earth_init_vel",
                    type=float,
                    default=[0,1,0],
                    help="float: The initial xyz velocity of the Sun.")

args = parser.parse_args()
print("Starting parameters:")
print("Sun xyz initial coordinates:",args.sun_init_coords)
print("Sun xyz initial coordinates:",args.sun_init_vel)
print("Earth xyz initial coordinates:",args.earth_init_coords)
print("Earth xyz initial coordinates:",args.earth_init_vel)


xlims = [-5,5]
ylims = [-5,5]
zlims = [0,5]

# Setup figure for animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xlim=(xlims[0], xlims[1]), ylim=(ylims[0], ylims[1]), zlim=(zlims[0], zlims[1]))

line_sun, = ax.plot([], [], lw=3, marker='o', color='red')
line_earth, = ax.plot([], [], lw=3, marker='o', color='green')


# ============================ Define functions ================================
def init():
    line_sun.set_data(np.array([]), np.array([]))
    line_sun.set_3d_properties([])

    line_earth.set_data(np.array([]), np.array([]))
    line_earth.set_3d_properties([])
    return line_sun, line_earth,

def animate(t_i, previous_earth_vel=0, a_i_minus_1=0):
    x_sun = args.sun_init_coords[0] + args.sun_init_vel[0] * t_i
    y_sun = args.sun_init_coords[1] + args.sun_init_vel[1] * t_i
    z_sun = args.sun_init_coords[2] + args.sun_init_vel[2] * t_i

    #previous_earth_vel = ...
    if t_i == 0:
        previous_earth_vel = args.earth_init_vel
    else:
        previous_earth_vel = previous_earth_vel + a_i_minus_1 * (t_i - 1) # need a way to make this dynamic

    #x_earth = args.earth_init_coords[0] + args.earth_init_vel[0] * t_i # + 0.5 * a * t_i ** 2   also earth_init_vel should only apply to start with - need to update previous velocity dynamically
    #y_earth = args.earth_init_coords[1] + args.earth_init_vel[1] * t_i
    #z_earth = args.earth_init_coords[2] + args.earth_init_vel[2] * t_i

    x_earth = args.earth_init_coords[0] + args.earth_init_vel[0] * t_i # + 0.5 * a * t_i ** 2   also earth_init_vel should only apply to start with - need to update previous velocity dynamically
    y_earth = args.earth_init_coords[1] + args.earth_init_vel[1] * t_i
    z_earth = args.earth_init_coords[2] + args.earth_init_vel[2] * t_i

    print(x_sun, y_sun, z_sun, x_earth, y_earth, z_earth, previous_earth_vel) # also need to make previous earth coords dynamic

    line_sun.set_data(np.array(x_sun), np.array(y_sun))
    line_sun.set_3d_properties(np.array(z_sun))

    line_earth.set_data(np.array(x_earth), np.array(y_earth))
    line_earth.set_3d_properties(np.array(z_earth))

    return line_sun, line_earth,

def euclidean_distance(coordsA, coordsB):
    delta_x = abs(coordsA[0] - coordsB[0])
    delta_y = abs(coordsA[1] - coordsB[1])
    delta_z = abs(coordsA[2] - coordsB[2])
    delta_r = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
    return delta_r

def newtonian_force(mA, coordsA, mB, coordsB):
    # Magnitude
    delta_r = euclidean_distance(coordsA, coordsB)
    F = (G * mA * mB) / (delta_r ** 2)
    return F

    # Need to get vector infomation of acceleration - aA = newtonian_force(mA,coordsA,mB,coordsB)/mA always in direction of B. Also find aB = newtonian_force(mA,coordsA,mB,coordsB)/mB always in direction of A



# ============================ Run script ======================================
def run_solar_system():

    #lineB, = ax.plot([], [], lw=300, marker='o', color='green')
    print("Running")

    previous_earth_vel = 0
    a_i_minus_1 =0
    anim = FuncAnimation(fig, animate, init_func=init, fargs=(previous_earth_vel, a_i_minus_1),
                                   frames=20, interval=200, blit=True)


    plt.show()

if __name__ == "__main__":
    run_solar_system()
