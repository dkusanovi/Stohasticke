import random
import numpy as np
import matplotlib.pyplot as plt
import math


x = []
y = []
N = []
rj = []


for j in range(100):
    x.append(random.random())

for i in range(100-6):
    i = i + 1
    N.append(i)
    suma = x[i]*x[i+5]
    c = suma/100
    rj.append(abs(math.sqrt(100)*(c-0.25)))


fig, ax = plt.subplots()
ax.grid()
ax.set_title("susjedi")
ax.set(xlabel='N', ylabel='c')
ax.plot(N, rj, markersize=1)

plt.show()

print(x)