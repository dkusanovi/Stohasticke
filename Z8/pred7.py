# deltaE < 0
# Es = Es + deltaE
# Ed = Ed - deltaE

# deltaE > 0 i deltaE < Ed
# Es = Es + deltaE
# Ed = Ed - deltaE

import math
import random
import numpy as np

m = 1
N = 100
E1 = 25
E2 = 50


def demon(N, Euk):
    Ed = 0.0
    vlist = []  
    for vv in range(N):
        vlist.append(0.0)

    vi = math.sqrt(2*Euk/(N))
    vlist = [vi for _ in range(N)]

    Euk = 0.0

    for _ in range(N):
        i = random.randint(0, N - 1)
        deltav = (random.random() - 0.5)
        v_old = vlist[i]
        v_new = v_old + deltav

        E_old = m*v_old**2 /2
        E_new = m*v_new**2 /2
        deltaE = E_new - E_old

        if deltaE <= 0:
            vlist[i] = v_new
            Ed = Ed - deltaE
        elif Ed >= deltaE:
            vlist[i] = v_new
            Ed = Ed - deltaE

        Euk = Euk + Ed

    avg_particle_energy = sum(m*v**2 /2 for v in vlist) / N
    avg_demon_energy = Euk / N

    return avg_particle_energy, avg_demon_energy


# Pokretanje za E = 25 i E = 50
N = 100
for E in [25, 50]:
    avg_Es, avg_Ed = demon(N, E)
    print(f"E = {E}")
    print(f"  Srednja energija po čestici: {avg_Es:.5f}")
    print(f"  Srednja energija demona:     {avg_Ed:.5f}")

