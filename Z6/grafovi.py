import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter

Nw = 1000
rf = np.loadtxt('rNw_300.dat', comments='#')
# print(rf.shape)
# print(rf[:5])

steps = len(rf)//Nw

fig = plt.figure(figsize=(8, 7), dpi=120)
ax = fig.add_subplot(111, projection='3d')
writer = PillowWriter(fps=10, metadata={'title': "atom vodika"})

with writer.saving(fig, "Nw_300.gif", dpi=120):
    for i in range(1, steps):
        ax.cla()  # brise osi za svaki korak

        walkers = rf[i*Nw:(i+1)*Nw]
        x, y, z = walkers[:, 1], walkers[:, 2], walkers[:, 3]

        ax.view_init(elev=6, azim=145)  # odakle gledamo na graf
        ax.set_aspect('auto')
        ax.scatter(x, y, z, c='blue', s=1)
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.set_zlim(-20, 20)
        ax.set_xlabel('x / a$_{0}$')
        ax.set_ylabel('y / a$_{0}$')
        ax.set_zlabel('z / a$_{0}$')
        ax.invert_yaxis()
        ax.invert_xaxis()
        ax.text(x=-20, y=-22, z=30, s=f"$\u03A8$(r)=|300>")
        ax.text(x=-20, y=-22, z=26, s="N$_{W}$=1000")
        ax.text(x=-22, y=25, z=26, s="t={} $\u0394$t".format(int(walkers[0, 0])))
        plt.tight_layout()

        writer.grab_frame()
        


rfr = np.loadtxt('r_300.dat', comments='#')

block, r, rb = [], [], []   # rb = prosjecni radijus po bloku
for _ in range(len(rfr)):
    val1, val2, val3 = rfr[_]
    block.append(val1)
    r.append(val3)
    rb.append(val2)

fig, ax = plt.subplots(figsize=(11, 4), dpi=110)
plt.rcParams.update({'font.size': 12})
ax.plot(block, rb, color='lime', lw=1.0, label='<r>$_{b}$')
ax.plot(block, r, color='blue', lw=1.0, label='<r>')
ax.set_xlim(0, 200)
ax.set_xlabel('t / 500 $\u0394$t')
ax.set_ylabel('<r> / a$_{0}$')
ax.text(x=3, y=13.7, s=f"N$_{'W'}$=1000, N$_{'b'}$=200, N$_{'k'}$=150")
ax.legend(loc='upper right')
plt.show()

