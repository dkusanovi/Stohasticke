import random
import numpy as np
import matplotlib.pyplot as plt
import math


Nw = 5000   # broj setaca
Nk = 5000   # koraci

x_min = 0       # ogranicavamo podrucje
x_max = 100
y_min = 0 
y_max = 100

x_min_w = 40        # ogranicavamo setace
x_max_w = 60
y_min_w = 15
y_max_w = 25

deltarx = [-0.5, 0.5]       # pomak setaca
deltary = [-1.5, 1.5]

x = np.random.uniform(x_min_w, x_max_w, Nw)     # nasumicni prvi polozaj setaca u odredenim granicama
y = np.random.uniform(y_min_w, y_max_w, Nw)

putanja = np.zeros((Nk, Nw, 2))     # stvaramo polje za putanje, 2 da imamo x i y



for k in range(Nk):
    dx = np.random.uniform(deltarx[0], deltarx[1], Nw)      # nasumicni pomak setaca
    dy = np.random.uniform(deltary[0], deltary[1], Nw)
    
    x = x + dx
    y = y + dy
    
    # rubovi (np.where radi isto sto i for if, else... ali optimizira kod pa brze radi)
    x = np.where(x > x_max, 200 - x, x)       # (uvjet, sto daje, sto je to)
    x = np.where(x < x_min, - x, x)       # ne zelimo da setac izade izvan granica
    y = np.where(y > y_max, 200 - y, y)
    y = np.where(y < y_min, - y, y)

    putanja[k] = np.stack((x, y), axis = -1)



plt.figure(figsize=(6, 6))

for w in range(0, 3):       # range je broj setaca koje zelimo nacrtat
    plt.plot(putanja[:, w, 0], putanja[:, w, 1])

# plt.xlim([x_min, x_max])
# plt.ylim([y_min, y_max])
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.title("Brownovo gibanje")
plt.grid()
plt.show()

    

