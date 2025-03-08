import random
import numpy as np
import matplotlib.pyplot as plt

M = 256
I = [3]
a = 57
c = 1
x = []
y = []

while len(x) < 500:
    for i in range(1000):
        I[i] = (a*I[i-1] + c)%M
        I.append(I[i])

        if i % 2 == 0:
            x.append(I[i])
        else:
            y.append(I[i])

    

fig, ax = plt.subplots()
ax.grid()
ax.set_title("random")
ax.set(xlabel='x', ylabel='y')
ax.plot(x, y, 'mo', markersize=1)

plt.show()

print(x)
print(y)

