import random
import numpy as np
import matplotlib.pyplot as plt
import math

x2ave = [0]
n = 100
m = 3
x = [0] # polozaj setaca
norm = []
ilist = []
xave = []

for j in range(1, m):
    for i in range(1, n):
        ilist.append(i)
        r = random.random()

        if r < 0.5:
            x.append(x[-1] + 1)
        else:
            x.append(x[-1] - 1)

        x2ave.append(x2ave[-1] + x[i]**2)

        xave.append(x[i]/m)
        norm.append(x2ave[i]/m)

fig, ax = plt.subplots()
ax.grid()
ax.set_title("")
ax.set(xlabel='i', ylabel='x')
ax.plot(ilist, norm, markersize=1)

plt.show()

    
    

