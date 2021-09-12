import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

xmax = 200
ymax = 200
zmax = 5

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xlim=(0, xmax), ylim=(0, ymax), zlim=(0,zmax))


lineA, = ax.plot([], [], [], lw=300, marker='o', color='red')
lineB, = ax.plot([], [], [], lw=300, marker='o', color='green')

xA_0 = 0
yA_0 = 0
vA_x = 1
vA_y = 1

B_inits = [0,0]
B_params = [1,2]


def init():
    lineA.set_data(np.array([]), np.array([]))
    lineB.set_data(np.array([]), np.array([]))
    lineA.set_3d_properties([])
    lineB.set_3d_properties([])
    return lineA, lineB,

def animate(t_i): # t_i is an index, here referring to the ith time index (we assume each frame is a second here)
    xA = xA_0 + vA_x * t_i
    yA = yA_0 + vA_y * t_i
    xB = B_inits[0] + B_params[0] * t_i
    yB = B_inits[1] + B_params[1] * t_i
    zA = 0
    zB = 0
    print(t_i,xA,yA,xB,yB)

    # Check if particle beyond allowed (max) range and cap it if necessary
    def max_cap(coord, coord_max):
        if coord > coord_max:
            coord = coord_max
        return coord
    xA = max_cap(xA, xmax)
    yA = max_cap(yA, ymax)
    xB = max_cap(xB, xmax)
    yB = max_cap(yB, ymax)


    lineA.set_data(np.array(xA), np.array(yA))
    lineB.set_data(np.array(xB), np.array(yB))
    lineA.set_3d_properties(np.array(zA))
    lineB.set_3d_properties(np.array(zB))
    return lineA, lineB,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# Save animation as gif
#anim.save('interactive_particle.gif', writer='imagemagick')

plt.show()
