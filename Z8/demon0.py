import random
import math

max_steps = 30000  # broj koraka
m = 10  # broj setaca
np = 40

idum = -1  # seed for random number generator

def ran1(idum):
    return random.random()

output = open("sistem3p.dat", "w")
output1 = open("demon3p.dat", "w")

Esustav = 40.0
delta = 1.6
accept = 0.0
v0 = math.sqrt(2.0 * Esustav / np)
print("v0=", v0)

Edemon = 0.0
ngr = 5000
Ezbroj_sustav = 0.0
Ezbroj_demon = 0.0
Ezbroj2_sustav = 0.0
Ezbroj2_demon = 0.0

v = [[0.0] * (m + 1) for _ in range(np + 2)]

for j in range(1, m + 1):
    for ip in range(1, np + 1):
        v[ip][j] = v0

for i in range(1, max_steps + 1):
    Eakum_demon = 0.0
    Eakum_sustav = 0.0

    for j in range(1, m + 1):
        for ip in range(1, np + 1):
            ind = round(ran1(idum) * np)
            dvel = delta * (2.0 * ran1(idum) - 1.0)
            probnav = v[ind][j] + dvel
            dE = 0.5 * (probnav * probnav - v[ind][j] * v[ind][j])

            if dE <= Edemon:
                v[ind][j] = probnav
                accept += 1.0
                Esustav += dE
                Edemon -= dE

            if i > ngr:
                Eakum_demon += Edemon
                Eakum_sustav += Esustav

    Ezbroj_sustav += Eakum_sustav / (m * np)
    Ezbroj2_sustav += Eakum_sustav * Eakum_sustav / (m * np * m * np)
    Ezbroj2_demon += Eakum_demon * Eakum_demon / (m * np * m * np)
    Ezbroj_demon += Eakum_demon / (m * np)

    if i > ngr and i % 10 == 0:  # save afer 10,20,30 ...
        n = i - ngr
        ko = i - ngr
        del_val = Ezbroj2_sustav / ko - (Ezbroj_sustav / ko) * (Ezbroj_sustav / ko)
        sigma = math.sqrt(del_val / ko)
        deld = Ezbroj2_demon / ko - (Ezbroj_demon / ko) * (Ezbroj_demon / ko)
        sigmad = math.sqrt(deld / ko)
        output.write(f"{i}\t{Ezbroj_sustav / (i - ngr)}\t{sigma}\n")
        output1.write(f"{i}\t{Ezbroj_demon / (i - ngr)}\t{sigmad}\n")

accept /= m * max_steps * np
print("accept=", accept)

output1.close()
output.close()


