import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as S

Esustav = 20
N = 100
Edemon = 0.0
Nk = 10000
ngr = 1000

output4 = open('redak.txt', 'w')               # za ispisivanje retka
sus = np.loadtxt('sistem3p.dat', usecols=2)
dem = np.loadtxt('demon3p.dat', usecols=2)

average_ES = np.mean(sus)                     # srednja vrijednost ukupne E sustava
average_ED = np.mean(dem)                     # srednja vrijednost ukupne enerEgije demona

output4.write(f"{'N':14s} {N:>8d}\n")
output4.write(f"{'E':14s} {Esustav + Edemon:>8.0f}\n")
output4.write(f"{'<ED>':14s} {average_ED:>8.1f}\n")
output4.write(f"{'<ES>':14s} {average_ES:>8.1f}\n")
output4.write(f"{'<ES>/N':14s} {average_ES/N:>8.5f}\n")
output4.write(f"{'<ES>/(N*<ED>)':14s} {average_ES/(N*average_ED):>8.3f}\n")
output4.write(f"{'0.5N*<ED>':14s} {0.5*N*average_ED:>8.0f}\n")
output4.close()

sus = np.loadtxt('sistem3p.dat')
dem = np.loadtxt('demon3p.dat')
step, average_ES_step, average_ED_step, average_ES_cu, average_ED_cu = [], [], [], [], []

for l in range(len(sus)):
    step.append(sus[l, 0])
    average_ES_step.append(sus[l, 1])
    average_ES_cu.append(sus[l, 2])
    average_ED_step.append(dem[l, 1])
    average_ED_cu.append(dem[l, 2])

def demon():
    fig = plt.figure(figsize=(12,5), dpi=110)
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.plot(step, average_ED_step, color='lime', lw=0.9, label='Srednja energija tijekom jednog koraka')
    ax.plot(step, average_ED_cu, color='red', lw=1.0, label='Ukupna srednja energija nakon $is$ koraka')
    ax.set_xlim(ngr, Nk)
    ax.set_xlabel('$is$ / korak')
    ax.set_ylabel('E$_{demon}$')
    ax.set_title('Idealni plin: N={}, E={}'.format(N, Esustav))
    legend = ax.legend(loc='upper right')
    legend.get_texts()[0].set_color('lime')
    legend.get_texts()[1].set_color('red')
    ax.grid(True)
    plt.show()


def sustav():
    fig = plt.figure(figsize=(12,5), dpi=110)
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.plot(step, average_ES_step, color='lime', lw=0.9, label='Srednja energija tijekom jednog koraka')
    ax.plot(step, average_ES_cu, color='red', lw=1.0, label='Ukupna srednja energija nakon $is$ koraka')
    ax.set_xlim(ngr, Nk)
    ax.set_xlabel('$is$ / korak')
    ax.set_ylabel('E$_{sustav}$')
    ax.set_title('Idealni plin: N={}, E={}'.format(N, Esustav))
    legend = ax.legend(loc='upper right')
    legend.get_texts()[0].set_color('lime')
    legend.get_texts()[1].set_color('red')
    ax.grid(True)
    plt.show()


demP = np.loadtxt('P_demon.dat')
Edem, pED, ln_pED = [], [], []

for i in range(len(demP)):
    if demP[i, 1] != 0.000000:
        Edem.append(demP[i, 0])
        pED.append(demP[i, 1])
        ln_pED.append(np.log(demP[i, 1]))

a, b, r, p, std_err = S.linregress(Edem, ln_pED)
kT = -1/a

y = [a*e+b for e in Edem]

def P():
    fig = plt.figure(figsize=(12,5), dpi=110)
    ax = fig.add_axes([0.15, 0.15, 0.80, 0.70])
    ax.plot(Edem, pED, color='red', lw=1.2)
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 2.16)
    ax.set_xlabel('ED')
    ax.set_ylabel('P$_{ED}$')
    ax.set_title('Idealni plin: N={}, E={}'.format(N, Esustav))
    ax.grid(True)
    plt.show()

def lnP():
    fig = plt.figure(figsize=(12,5), dpi=110)
    ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
    ax.scatter(Edem, ln_pED, color='cyan', s=1, label='ln(P$_{ED}$)')
    ax.plot(Edem, y, color='blue', lw=1.0, label=f"{a:<5.2f}*ED+{b:<5.2f}")
    ax.set_xlim(0.0, 4.0)
    ax.set_xlabel('ED')
    ax.set_ylabel('ln(P$_{ED}$)')
    ax.set_title('Idealni plin: N={}, E={}'.format(N, Esustav))
    legend = ax.legend(loc='upper right')
    legend.get_texts()[0].set_color('cyan')
    legend.get_texts()[1].set_color('blue')
    ax.grid(True)
    plt.show()



demon()
sustav()
P()
lnP()