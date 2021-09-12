import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import animation

def f(x,y):
    return x+y

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xlim=(0, 20), ylim=(0, 20), zlim=(0,20))
X = np.arange(0, 10, 1)
Y = np.arange(0, 10, 1)
Z = X+Y

X1, Y1 = np.meshgrid(X, Y)
Z1 = f(X1, Y1)
#ax.plot_surface(X1, Y1, Z1, color='red', alpha=0.5)

line, = ax.plot([], [], [], lw=2)

def init():
    line.set_data(np.array([]), np.array([]))
    line.set_3d_properties([])
    return line,

def animate(i, line, X, Y, Z):
    line.set_data(X[:i], Y[:i]) # For safety: line.set_data(np.array(X[:i]), np.array(Y[:i]))
    line.set_3d_properties(Z[:i])
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=(line, X, Y, Z),
                           frames=10, interval=200,
                           repeat_delay=5, blit=True)

try:
    __IPYTHON__
except NameError:
    ipython = False
else:
    ipython = True

print(ipython)
if ipython == True:
    plt.ion()

plt.show()
