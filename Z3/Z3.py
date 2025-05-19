import math
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import stats



Nw = 64000
Nk = 200
x2list = [0]
klist = [0]
xw = np.zeros((Nw, Nk+1))


def hod(Nw, Nk):
    for k in range(1, Nk+1):
        klist.append(k)
        x2ave = 0
        for w in range(Nw):
            xw[w, k] = xw[w, k-1] + (6.0*np.random.rand()-3.0)
            x2ave = x2ave + xw[w, k]**2
        x2 = x2ave/Nw
        x2list.append(x2)

    with open('k_x2.txt', 'w') as f:
        for k in range(Nk):
            f.write(f"{klist[k]} {x2list[k]}\n")

    return klist, x2list, xw

hod(Nw, Nk)

#---------------------------------------------------------------------------------------------------


x_min = -100
x_max = 100

delta_x = 2.0

celija_x = int((x_max - x_min)/delta_x)+1

x = np.zeros(Nw)
Ps = np.zeros((Nk, celija_x))

for k in range(Nk):
    x = x + 6*np.random.rand(Nw)-3

    x = np.where(x > x_max, 2*x_max - x, x)
    x = np.where(x < x_min, -x, x)

    P = np.zeros(celija_x)
    for w in range(Nw):
        i = int((x[w] + 100.0 + 1)/delta_x)          # ako ne dodamo 100 i 1(polovica celije) razdioba će biti pomaknuta na -100
        if 0 <= i < celija_x:
            P[i] = P[i] + 1

    P = P/(Nw*delta_x)
    Ps[k] = P




def crtanje():
    xpos = np.linspace(x_min + delta_x/2, x_max - delta_x/2, celija_x)

    vremena = [0, 10, 50, 100, 199]
    boje = ['blue', 'red', 'green', 'purple', 'black']

    fig = plt.figure(figsize=(10, 6))
    axs = fig.add_axes([0.15, 0.15, 0.75, 0.75])

    for t, color in zip(vremena, boje):
        axs.plot(xpos, Ps[t, :], lw=2, color=color, label=f't = {t}')

    axs.set_xlabel('$x$')
    axs.set_ylabel('P$_{1D}$(x,t)')
    axs.set_title('Razdioba šetača u vremenu')
    axs.set_xlim(-100.0, 100.0)
    axs.set_ylim(0.0, 0.2)
    axs.legend()
    axs.grid()
    plt.show()

crtanje()




a, b, r, p, std_err = stats.linregress(klist, x2list)
D = a/2

# iz log filea vidimo da se dobiva D = 1.51133

print(D)



#----------------------------------------------------------------------------------------------------


ddx = 2.0
ddt = 1.0
# uvjet: dx**2 >= 2*D*dt



def rho(x):
    if x >= -ddx/2 and x <= ddx/2:
        return 1.0/ddx
    else:
        return 0.0


tlist = []
tN = 200


# poc_uvjeti= [x0, xN, t0, tN, dx, dt]


def eksplicitno(gx, poc_uvjeti, D):
    dx = poc_uvjeti[4]
    dt = poc_uvjeti[5]

    N = int((poc_uvjeti[1]-poc_uvjeti[0])/dx)
    M = int((poc_uvjeti[3]-poc_uvjeti[2])/dt)

    alpha = D*dt/(dx**2)

    prva = np.zeros(N+1) # upoc
    druga = np.zeros(N+1) # u novo

    rub_l = 0.0
    rub_d = 0.0

    for i in range(len(prva)):
        prva[i] = gx(poc_uvjeti[0] + i*dx)

    for j in range(M+1):

        for ii in range(1, N):
            druga[ii] = alpha*prva[ii+1]+(1-2*alpha)*prva[ii]+alpha*prva[ii-1]

        druga[0] = rub_l
        druga[-1] = rub_d

        prva = np.copy(druga)

    return druga



P1 = [-100, 100, 0.0, 0.0, ddx, ddt]
P2 = [-100, 100, 0.0, 10.0, ddx, ddt]
P3 = [-100, 100, 0.0, 50.0, ddx, ddt]
P4 = [-100, 100, 0.0, 100.0, ddx, ddt]
P5 = [-100, 100, 0.0, 199.0, ddx, ddt]

D1 = eksplicitno(rho, P1, D)
D2 = eksplicitno(rho, P2, D)
D3 = eksplicitno(rho, P3, D)
D4 = eksplicitno(rho, P4, D)
D5 = eksplicitno(rho, P5, D)

X = np.linspace(-100, 100+ddx, len(D1))
# X = [br for br in np.arange(-100, 100+ddx, ddx)]

fig = plt.figure()
axs = fig.add_axes([0.15, 0.15, 0.75, 0.75])

axs.grid()
axs.plot(X, D1, label='t = 0')
axs.plot(X, D2, color='red', label='t = 10')
axs.plot(X, D3, color='green', label='t = 50')
axs.plot(X, D4, color='purple', label='t = 100')
axs.plot(X, D5, color='black', label='t = 199')

axs.set_xlabel("x")
axs.set_ylabel("rho(x, t)")

axs.legend()
plt.show()



#-----------------------------------------------------------------------------

def usporedba():
    vremena = [0, 10, 50, 100, 199]
    boje = ['blue', 'red', 'green', 'purple', 'black']

    xpos = np.linspace(x_min + delta_x/2, x_max - delta_x/2, celija_x)
    X_rho = np.arange(-100, 100 + ddx, ddx)
    # X_rho = np.linspace(-100, 100+ddx, len(D1))

    plt.figure(figsize=(10, 6))
    axs = plt.gca()

    for t, color in zip(vremena, boje):
        axs.plot(xpos, Ps[t], linestyle='-', color=color, label=f'P(x, t={t})')

        poc_uvjeti = [-100, 100, 0.0, t, ddx, ddt]
        ro = eksplicitno(rho, poc_uvjeti, D)
        axs.plot(X_rho, ro, linestyle='--', color=color, label=f'rho(x, t={t})')

    axs.set_xlim(-100, 100)
    axs.set_ylim(bottom=0)
    axs.set_xlabel('x')
    axs.set_ylabel('Gustoća vjerojatnosti')
    axs.set_title('Usporedba P i rho')
    axs.legend()
    axs.grid(True)
    plt.show()




usporedba()
