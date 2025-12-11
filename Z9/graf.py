import numpy as np
import matplotlib.pyplot as plt

# toplinski kapacitet i susceptibilnost za L = 4, 8, 32
f4t = np.loadtxt('f_T.dat', comments='#', usecols = (0,1,2,3,4))
f8t = np.loadtxt('f_T8.dat', comments='#', usecols = (0,1,2,3,4))
f32t = np.loadtxt('f_T32.dat', comments='#', usecols = (0,1,2,3,4))

# fm. ("#b, Mb, M, sigM")
# fE. ("#b, Eb, E, sigE")
# fT. ("#T, c, x\n")

x4, x8, x32,  C4, C8, C32 = [], [], [], [], [], []

kT4 = f4t[:, 0]
kT8 = f8t[:, 0]
kT32 = f32t[:, 0]

min_len = min(len(f4t), len(f8t), len(f32t))
for i in range(min_len):
    C4.append(f4t[i, 1])
    x4.append(f4t[i, 2])
    C8.append(f8t[i, 1])
    x8.append(f8t[i, 2])
    C32.append(f32t[i, 1])
    x32.append(f32t[i, 2])

def C():
    fig, ax = plt.subplots(figsize=(10,6), dpi=110)
    ax.scatter(kT4, C4, color='red', s=10, label=r'L=4, T$_{C}\approx2.4$ K')
    ax.scatter(kT8, C8, color='purple', s=10, label=r'L=8, T$_{C}\approx2.4$ K')
    ax.scatter(kT32, C32, color='green', s=10, label=r'L=32, T$_{C}\approx2.4$ K')
    ax.plot(kT4, C4, color='red', lw=0.5)
    ax.plot(kT8, C8, color='purple', lw=0.5)
    ax.plot(kT32, C32, color='green', lw=0.5)
    ax.set_xlabel('T / K')
    ax.set_ylabel('C$_{V}$ / k$_{B}$')
    ax.grid(lw=0.2)
    ax.legend(loc='upper right')
    ax.set_title('2D Isingov model: toplinski kapacitet po čestici')
    plt.show()


def sus():
    fig, ax = plt.subplots(figsize=(10,6), dpi=110)
    ax.scatter(kT4, x4, color='red', s=10, label=r'L=4, T$_{C}\approx1.6$ K')
    ax.scatter(kT8, x8, color='purple', s=10, label=r'L=8, T$_{C}\approx2.0$ K')
    ax.scatter(kT32, x32, color='green', s=10, label=r'L=32, T$_{C}\approx2.4$ K')
    ax.plot(kT4, x4, color='red', lw=0.5)
    ax.plot(kT8, x8, color='purple', lw=0.5)
    ax.plot(kT32, x32, color='green', lw=0.5)
    ax.set_xlabel('T / K')
    ax.set_ylabel('$\u03C7$')
    ax.grid(lw=0.2)
    ax.legend(loc='upper right')
    ax.set_title('2D Isingov model: susceptibilnost po čestici')
    plt.show()


# energija i magnetizacija za L = 4, 8, 32

E4, E8, E32, M4, M8, M32 = [], [], [], [], [], []

for i in range(min_len):
    E4.append(f4t[i, 3])
    M4.append(f4t[i, 4])
    E8.append(f8t[i, 3])
    M8.append(f8t[i, 4])
    E32.append(f32t[i, 3])
    M32.append(f32t[i, 4])
    

def E():   
    fig, ax = plt.subplots(figsize=(10,6), dpi=110)
    ax.scatter(kT4, E4, color='red', s=10, label=r'L=4, T$_{C}\approx2.4$ K')
    ax.scatter(kT8, E8, color='purple', s=10, label=r'L=8, T$_{C}\approx2.4$ K')
    ax.scatter(kT32, E32, color='green', s=10, label=r'L=32, T$_{C}\approx2.4$ K')
    ax.plot(kT4, E4, color='red', lw=0.5)
    ax.plot(kT8, E8, color='purple', lw=0.5)
    ax.plot(kT32, E32, color='green', lw=0.5)
    ax.set_xlabel('T / K')
    ax.set_ylabel(r'$\dfrac{<E>}{N}$')
    ax.grid(lw=0.2)
    ax.legend(loc='upper left')
    ax.set_title('2D Isingov model: srednja energija po čestici')
    plt.show()

def M():
    fig, ax = plt.subplots(figsize=(10,6), dpi=110)
    ax.scatter(kT4, M4, color='red', s=10, label=r'L=4, T$_{C}\approx2.4$ K')
    ax.scatter(kT8, M8, color='purple', s=10, label=r'L=8, T$_{C}\approx2.4$ K')
    ax.scatter(kT32, M32, color='green', s=10, label=r'L=32, T$_{C}\approx1.4$ K')
    ax.plot(kT4, M4, color='red', lw=0.5)
    ax.plot(kT8, M8, color='purple', lw=0.5)
    ax.plot(kT32, M32, color='green', lw=0.5)
    ax.set_xlabel('T / K')
    ax.set_ylabel(r'$\dfrac{<M>}{N}$')
    ax.grid(lw=0.2)
    ax.legend(loc='upper right')
    ax.set_title('2D Isingov model: srednja magnetizacija po čestici')
    plt.show()


f8m = np.loadtxt('f_m8.dat', comments='#', usecols = (0,1,2,3))
f8E = np.loadtxt('f_E8.dat', comments='#', usecols = (0,1,2,3))


b, Eb, Eu, Mb, Mu = [], [], [], [], []

for k in range(800):
    b.append(f8E[k, 0])
    Eb.append(f8E[k, 1])
    Eu.append(f8E[k, 2])
    Mb.append(f8m[k, 1])
    Mu.append(f8m[k, 2])


def ravnotezno1():
    fig, ax = plt.subplots(figsize=(12,5), dpi=110)
    ax.plot(b, Eb, color='lime', lw=1.0, label='<E$_{b}$>')
    ax.plot(b, Eu, color='red', lw=1.2, label='<E$_{u}$>')
    ax.set_xlabel('block')
    ax.set_ylabel('<E>')
    ax.grid(lw=0.2)
    ax.legend(loc='upper right')
    ax.set_title('2D Isingov model: energija sustava za L=8 i T=1 K')
    ax.text(x = 215.0, y = -123, s=r"$N_b^{\mathrm{skip}} = 200$, $N_b = 1000$, $N_k = 1000$")
    plt.show()

def ravnotezno2():
    fig, ax = plt.subplots(figsize=(12,5), dpi=110)
    ax.plot(b, Mb, color='lime', lw=1.0, label='<M$_{b}$>')
    ax.plot(b, Mu, color='red', lw=1.2, label='<M$_{u}$>')
    ax.set_xlabel('block')
    ax.set_ylabel('<M>')
    ax.grid(lw=0.2)
    ax.legend(loc='lower right')
    ax.set_title('2D Isingov model: magnetizacija sustava za L=8 i T=1 K')
    ax.text(x = 215.0, y = 62.8, s=r"$N_b^{\mathrm{skip}} = 200$, $N_b = 1000$, $N_k = 1000$")
    plt.show()

C()
sus()
E()
M()
ravnotezno1()
ravnotezno2()