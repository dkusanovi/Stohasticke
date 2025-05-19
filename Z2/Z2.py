import random
import numpy as np
import matplotlib.pyplot as plt
import math as m


Nw = 200000   # broj setaca
Nk = 2000   # koraci

# t = 6
# deltat = 5

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

delta_x = 2
delta_y = 2

x = np.random.uniform(x_min_w, x_max_w, Nw)     # nasumicni prvi polozaj setaca u odredenim granicama
y = np.random.uniform(y_min_w, y_max_w, Nw)

putanja = np.zeros((Nk, Nw, 2))     # stvaramo polje za putanje, 2 da imamo x i y

celija_x = int((x_max - x_min)/delta_x)
celija_y = int((y_max - y_min)/delta_y)

P = np.zeros((celija_x, celija_y))

S = 0
Slista = [0]



for k in range(Nk):
    dx = np.random.uniform(deltarx[0], deltarx[1], Nw)      # nasumicni pomak setaca
    dy = np.random.uniform(deltary[0], deltary[1], Nw)

    x = x + dx
    y = y + dy

    # rubovi (np.where radi isto sto i for if, else... ali optimizira kod pa brze radi)
    x = np.where(x > x_max, 200 - x, x)       # (uvjet, sto daje, sto je to)
    x = np.where(x < x_min, - x, x)          # ne zelimo da setac izade izvan granica
    y = np.where(y > y_max, 200 - y, y)
    y = np.where(y < y_min, - y, y)

    putanja[k] = np.stack((x, y), axis=-1)

    P = np.zeros((celija_x, celija_y))

    for w in range(Nw):
        i = int(x[w]/delta_x)
        j = int(y[w]/delta_y)
        P[i, j] = P[i, j] + 1


    # for i in range(celija_x):
    #         for j in range(celija_y):
    #             if P[i, j] > 0:
    #                 S = S - P[i, j]*m.log(P[i, j])
    # Slista.append(S)  # popravit entropiju

    P = P/Nw

    if k % 1000 == 0:
        with open('Pij.txt', 'w') as f:
            for i in range(celija_x):
                for j in range(celija_y):
                    X = (i + 0.5)*delta_x
                    Y = (j + 0.5)*delta_y
                    Z = P[i, j]/(delta_x*delta_y)
                    f.write(f"{X} {Y} {Z}\n")
                f.write("\n")
            f.write("\n")

# with open('S.txt', 'w') as fi:
#     for k in range(Nk):
#         fi.write(f"{k} {Slista[k]}\n")


