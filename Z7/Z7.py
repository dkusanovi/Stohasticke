import matplotlib.pyplot as plt
import numpy as np

E = np.loadtxt('E.txt')
Edev0 = np.loadtxt('E_dev.dat', comments='#')
stdev = open('st_dev_E.dat', 'w')
N = len(E)
Nkmax = 200

for Nk in range(1, Nkmax+1):
    Nb = N // Nk                 
    if Nb <= 2:                         
        continue
    Sfb = 0.0                             #suma srednjih energija po bloku
    Sf2b = 0.0                            #kvadrat suma srednjih vrijednosti po bloku
    for i in range(Nb):
        block = E[i*Nk : (i+1)*Nk, 1]
        Sfk = np.sum(block)/Nk
        Sfb = Sfb + Sfk
        Sf2b = Sf2b + (Sfk*Sfk)
    mean = Sfb / Nb
    var = (Sf2b / Nb - mean**2) / (Nb - 1)
    stdev.write(f"{Nk:<3d} {Sfb/Nb:>13.9f} {np.sqrt(var):>13.9f}\n")
        
stdev.close()

Edev = np.loadtxt('st_dev_E.dat')

b, aveE, devE, dev0 = [], [], [], []

for line in Edev:
    b.append(line[0])                   # velicina bloka
    aveE.append(line[1])                # srednje energije
    devE.append(line[2])                # devijacija energije nakon blokiranja

for line in Edev0:
    dev0.append(line[1])                # devijacija energije prije blokiranja

minlen = min(len(b), len(dev0))          # liste moraju bit iste duljine
b = b[:minlen]
aveE = aveE[:minlen]
devE = devE[:minlen]
dev0 = dev0[:minlen]

mdev = f"{np.mean(devE):<5.3f}"


def graf1():
    fig = plt.figure(figsize=(12, 5), dpi=110)
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.plot(b, np.array(dev0)*1000, label='energija')
    ax.plot(b, np.array(devE)*1000, linestyle='--', label='blokiranje')
    ax.set_xlim(0, 200)
    ax.set_xlabel('b / 2000')
    ax.set_ylabel('$10^{3}$ $σ_{E}$ / mK')
    ax.grid(True)
    ax.text(10, 60, s='$σ_{}$={} mK'.format('E', mdev))
    ax.set_title('Standardna devijacija $σ_{E}$ energije $E$ klastera\n$^{4}$He$_{20}$ za vremenski korak $Δ τ=10^{-7}$ mK$^{-1}$')
    ax.legend(loc='upper right')
    plt.show()

def graf2():
    fig = plt.figure(figsize=(12, 5), dpi=110)
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.errorbar(b, aveE, yerr=devE, fmt='o-', capsize=3, label='energija', ecolor='purple', elinewidth=0.3, ms=5, mew=1)
    ax.set_xlim(0, 200)
    ax.set_xlabel('b / 2000')
    ax.set_ylabel('<E> / mK')
    ax.grid(True)
    ax.set_title('Srednja vrijednost energije $E$ klastera $^{4}$He$_{20}$ za\nvremenski korak $Δ τ=10^{-7}$ mK$^{-1}$ dobivena dodatnim blokiranjem')
    ax.legend(loc='upper right')
    plt.show()

graf1()
graf2()