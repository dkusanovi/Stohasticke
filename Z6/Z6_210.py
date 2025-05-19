import numpy as np
import random

NbSkip = 50             # broj preskocenih blokova
Nb = 200               # = broj blokova (number of blocks)
Nk = 150
Nw = 1000
Nacc = 300             # broj koraka za provjeru prihvacanja (total steps)
a0 = 0.529*10**(-10)

def Psi(r, z):  
    return z*np.exp(-r/2.0) # 210

# ik = 0                                                # indeks koraka, trenutni korak (index of step)
# ib = 1                                                # indeks bloka, trenutni blok (index of block)
x = np.random.uniform(-7.0, 7.0, (3, Nw))             # polozaji [x, y, z] setaca
# xp = np.zeros(4)                         # koordinate probnog polozaja setaca (trial position)
dX = np.array([1.5, 1.5, 1.5])             # maksimalna duljina koraka (maximum change of coordinate)
f = np.zeros(Nw)                           # f: Stores radii r for each walker.
P = np.zeros(Nw)                           # P: Probability densities |Ψ|² for each walker.

r2 = np.sum(x**2, axis=0)
r = np.sqrt(r2)
P = Psi(r, x[2])**2                       
f = r.copy()

ff = open("r_210.dat", "w")                   # prosjecni radijus <r>
frNw = open("rNw_210.dat", "w")               # polozaj svakog setaca

# for iw in range(1, Nw + 1):                 # postavlja svakog setaca u prostor, računa svakom radijus i gustocu vjerojatnosti
#     rp2 = 0.0
#     for k in range(1, 4):
#         x[k][iw] = 14.0 * (np.random.rand() - 0.5)         # pretpostavljam da je ovo d
#         rp2 += x[k][iw] * x[k][iw]                         # ovo je valjda delta x
#     frNw.write("%7d  %13.8e  %13.8e  %13.8e\n" % ((ib - 1) * Nk + ik, x[1][iw], x[2][iw], x[3][iw]))
#     rp = np.sqrt(rp2)
#     tmp = Psi(rp, x[3][iw])
#     P[iw] = tmp * tmp
#     f[iw] = rp
# frNw.write("\n\n")

for iw in range(Nw): #spremanje pocetnih vrijednosti
    frNw.write(f"{0:<7d} {x[0, iw]:>12.6f} {x[1, iw]:>12.6f} {x[2, iw]:>12.6f}\n")
# frNw.write("\n")

acc = 0.0                                # ukupno prihvaceno
Sbf = 0.0                                # zbroj srednjih vrijednosti po blokovima
Sbf2 = 0.0                               # suma za varijancu od r

for ib in range(1 - NbSkip, Nb + 1):
    Skf = 0.0                        # zbroj srednjih vrijednosti po koracima
    if ib == 1:
        acc = 0.0

    for ik in range(1, Nk + 1):
        Swf = 0.0

        for iw in range(Nw):
            rp2 = 0.0
            dx = (np.random.rand(3) - 0.5) * dX
            xp = x[:, iw] + dx
            rp2 += xp * xp

            rp = np.linalg.norm(xp)                      # r probnog polozaja
            tmp = Psi(rp, xp[2])
            Pp = tmp * tmp                        # vjerojatnost nalazenja u probnom polozaju (probability density at xp)
            T = Pp / P[iw]                       # vjerojatnost prijelaza
            if T >= 1 or np.random.rand() <= T:   # ako se prihvati, onda se pohranjuje novi polozaj, vjerojatnost i radijus
                x[:, iw] = xp
                acc += 1
                P[iw] = Pp                    # vjerojatnost nalazenja u probnom polozaju
                f[iw] = rp                    # r probnog polozaja

            Swf += f[iw]

        if (ib - 1 + NbSkip) * Nk + ik % Nacc == 0 and ib < 1:   # računa stopu prihvacanja tijekom stabilizacije
            accP = acc / (Nacc * Nw)
            # 1) PRILAGODITE MAX KOORDINATNE POMAKE (ADJUST MAX COORDINATE CHANGES)
            accP = acc/(Nacc*Nw)
            scale = (1+0.05) if accP > 0.5 else (1-0.05)
            dX *= scale
            
            # duljinu koraka podesavamo za prihvacanje = 50%
            if ib % 10:
                print("ib = %d, accP = %3.1lf\n" % (ib, accP * 100.0))
            acc = 0.0

        if ib > 0:           # nakon stabilizacije
            Skf += Swf / Nw
    if ib > 0:
        Sbf += Skf / Nk
        Sbf2 += Skf * Skf / (Nk * Nk)
        accP = acc / (ib * Nw * Nk)          # udio prihvacenih koraka
        # 2) PRILAGODITE MAX KOORDINATNE POMAKE (ADJUST MAX COORDINATE CHANGES)
        scale = (1+0.05) if accP > 0.5 else (1-0.05)
        dX *= scale
        
        
        if ib % (Nb // 10) == 0:          # printa progres svakih 10% ukupnih blokova
            print("ib = %d, accP = %3.1lf\n" % (ib, accP * 100.0))
        # 3) POHRANITE SVE POLOZAJE U frNw (STORE ALL POSITIONS IN frNw)
        for iw in range(Nw):
            frNw.write(f"{(ib-1)*Nk+ik:<7d} {x[0, iw]:>12.6f} {x[1, iw]:>12.6f} {x[2, iw]:>12.6f}\n")

        # frNw.write("\n")
        ff.write("%7d  %13.8e  %13.8e\n" % (ib, Skf / Nk, Sbf / ib))

# 4) IZRACUNAJTE PROSJEK, DEVIJACIJU I PRIHVACENOST: ave_f, sig_f, accP
ave_f = Sbf / Nb
sig_f = np.sqrt(Sbf2 / Nb - ave_f**2)


print("\n accP = %4.1lf\n" % (accP * 100.0))
print("\n max dx = %6.4lf, %6.4lf, %6.4lf\n" % tuple(dX))
print("\n <r> = %8.5lf +- %8.6lf \n" % (ave_f, sig_f))