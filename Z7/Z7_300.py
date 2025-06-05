import numpy as np
import matplotlib.pyplot as plt

Nw = 1000 
Nkmax = 200
r = np.loadtxt('r_300.dat', comments='#', usecols=(1))
stdev = open('st_dev_300.dat', 'w')

N = len(r)

for Nk in range(1, Nkmax+1):
    Nb = N // Nk 
    if Nb <= 2: 
        continue
    Sfb = 0.0                             #suma srednjih energija po bloku
    Sf2b = 0.0                            #kvadrat suma srednjih vrijednosti po bloku
    for i in range(Nb):
        block = r[i*Nk : (i+1)*Nk]
        Sfk = np.sum(block)/Nk
        Sfb = Sfb + Sfk
        Sf2b = Sf2b + (Sfk*Sfk)
    mean = Sfb / Nb
    var = (Sf2b / Nb - mean**2) / (Nb - 1)
    stdev.write(f"{Nk:<3d} {mean:>13.9f} {np.sqrt(var):>13.9f}\n")

stdev.close()

rdev = np.loadtxt('st_dev_300.dat')

b, aver, devr = [], [], []

for line in rdev:
    b.append(line[0])               # velicina bloka
    aver.append(line[1])            # srednje energije
    devr.append(line[2])            # devijacija energije nakon blokiranja

mdev = f"{np.mean(devr):<5.3f}"


def graf1():
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.plot(b, np.array(devr)*1000)
    ax.set_xlim(0, 67)
    ax.set_xlabel('b')
    ax.set_ylabel('$10^{3} σ_{r}$ / $\u212B$')
    ax.grid(True)
    ax.set_title('Standardna devijacija $σ_{r}$ radijalne udaljenosti <r> elektrona u |3,0,0> stanju vodikova atoma')
    ax.text(4, 7, s='$σ_{}$={} $\u212B$'.format('r', mdev))
    plt.show()

def graf2():
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.errorbar(b, aver, yerr=devr, fmt='o-', capsize=2, label='radijalna udaljenost', ecolor='purple', elinewidth=0.3, ms=3, mew=1)
    ax.set_xlim(0, 67)
    ax.set_xlabel('b')
    ax.set_ylabel('<r> / a$_{0}$')
    ax.grid(True)
    ax.set_title('Vrijednosti srednje radijalne udaljenosti <r> elektrona u |3,0,0> stanju vodikova atoma dobivene dodatnim blokiranjem')
    ax.legend(loc='upper right')
    plt.show()

graf1()
graf2()