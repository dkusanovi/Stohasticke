import numpy as np

# kod pisan po primjeru koda prof. Vranjes Markic


Esustav = 20.0        # energija sustava
N = 100               # broj cestica
delta = 1.4           # maksimalna promjena brzine
ngr = 1000            # odbaceni koraci
Nk = 10000            # ukupni broj koraka
Nw = 50               # broj setaca
Edemon_max = 4.0
NED = 500             # broj intervala za energiju demona
dED = Edemon_max / NED
p_demon = np.zeros(NED + 1)

v = np.zeros((N, Nw))
v[:, :] = np.sqrt(2 * Esustav / N) 

accept = 0
output1 = open('sistem3p.dat', 'w')         # count, E sustava / count, E sustava
output2 = open('demon3p.dat', 'w')          # count, E demona / count, E demona
output3 = open('P_demon.dat', 'w')          # E demona, razdioba

Ezbroj_sustav = 0
Ezbroj_demon = 0
count = 0
demon_E = np.zeros(Nw)


for i in range(1, Nk + 1):
    Eakum_demon = 0.0
    Eakum_sustav = 0.0

    for j in range(Nw):
        ipd = np.random.randint(N)
        dvel = (2*np.random.rand()-1.0)*delta
        probnav = v[ipd, j]+dvel
        dE = 0.5* (probnav * probnav - v[ipd, j]*v[ipd, j])

        if dE < 0.0 or demon_E[j] >= dE:
            v[ipd, j] = probnav
            demon_E[j] = demon_E[j] - dE
            accept = accept + 1

        Eakum_sustav = Eakum_sustav + np.sum(0.5*(v[:, j]*v[:, j]))
        Eakum_demon = Eakum_demon + demon_E[j]
        id = int(demon_E[j] / dED)

        if id <= NED:
            p_demon[id] = p_demon[id] + 1

    if i >= ngr and i % 10 == 0: # srednje vrijednosti
        Eakum_sustav2 = Eakum_sustav / Nw
        Eakum_demon2 = Eakum_demon / Nw
        Ezbroj_sustav = Ezbroj_sustav + Eakum_sustav2
        Ezbroj_demon = Ezbroj_demon + Eakum_demon2
        count = count + 1
        output1.write(f"{i:>6d} {Eakum_sustav2:>15.11f} {Ezbroj_sustav/count:>15.11f}\n")
        output2.write(f"{i:>6d} {Eakum_demon2:>15.11f} {Ezbroj_demon/count:>15.11f}\n")

for i in range(NED+1):
    p_demon[i] /= dED * Nw * Nk
    output3.write(f"{i*dED:>8.5f} {p_demon[i]:>10.7f}\n")
    
print("\naccept = {}\n".format(accept/(Nk*Nw)))

output1.close()
output2.close()
output3.close()