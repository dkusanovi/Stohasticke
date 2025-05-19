import random
import numpy as np
import matplotlib.pyplot as plt
import math


x = []
N = []
rj = []
N_max = 10000000
k = 5
suma = 0


for j in range(N_max):
    x.append(random.random())


for i in range(N_max-k):
    suma = suma + x[i]*x[i+5]
    c = suma/(i+1)
    if (i+1)%1000 == 0:
        N.append(i+1)
        rj.append((math.sqrt(i+1)*(c-0.25)))


fig, ax = plt.subplots()
ax.grid()
ax.set_title("susjedi")
ax.set(xlabel='N', ylabel='$\sqrt{N} \cdot (C(5) - 0.25)$')
ax.plot(N, rj, markersize=1)

plt.savefig("Z1_graf.png", dpi=300, bbox_inches='tight')

plt.show()