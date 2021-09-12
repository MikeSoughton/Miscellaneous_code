import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')


fig = plt.figure()
ax = plt.axes(xlim=(0, 200), ylim=(0, 200))
lineA, = ax.plot([], [], lw=300, marker='o', color='red')
lineB, = ax.plot([], [], lw=300, marker='o', color='green')

xA_0 = 0
yA_0 = 0
vA_x = 1
vA_y = 1

B_inits = [0,0]
B_params = [1,2]


def init():
    lineA.set_data([], [])
    lineB.set_data([], [])
    return lineA, lineB,

def animate(t_i):
    xA = xA_0 + vA_x * t_i
    yA = yA_0 + vA_y * t_i
    xB = B_inits[0] + B_params[0] * t_i
    yB = B_inits[1] + B_params[1] * t_i
    print(xA,yA,xB,yB)
    lineA.set_data(xA, yA)
    lineB.set_data(xB, yB)
    return lineA, lineB,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# Save animation as gif
#anim.save('interactive_particle.gif', writer='imagemagick')

plt.show()
