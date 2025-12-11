import numpy as np
import random

max_dim = 8      # dimenzija resetke max X max
kT0 = 1.0        # pocetna temperatura
dkT = 0.2        # temperaturni korak
nT = 15          # broj razlicitih temperatura
Jv = 1.0         # konstanta izmjene energije

NbSkip = 200
Nk = 1000
Nb = 1000

#  Odredite kako se ponaša susceptibilnost po spinu, za beskonačan sustav modeliran korištenjem 
# različitih periodičnih rešetki (4x4 ili 8x8), u ovisnosti o temperaturi. Promotrite temperaturni raspon od 
# 1 do 4 K s koracima od 0.2 K. Završna konfiguraciju rešetke na prethodnoj temperaturi neka bude 
# trenutna početna.  
# Priložite kod i graf na kojem su prikazani zajedno rezultati svih simulacija 𝑋(𝑇). Na grafu napišite kolika 
# je temperatura faznog prijelaza. Priložite neki dodatni graf koji potvrđuje ravnotežno uzorkovanje.  

Swrite = 1  # pohrana mape spinova (0=NE, 1=DA)

random.seed(20)

def energija(s):
	sum_energija = 0.0
	for i in range(1, max_dim + 1):
		for j in range(1, max_dim + 1):
			desno = 1 if i == max_dim else i + 1
			gore = 1 if j == max_dim else j + 1
			sum_energija -= Jv * s[i,j] * (s[i][gore] + s[desno][j]) + mH * s[i][j]
	return sum_energija

def magnetizacija(s):
	sum_magnetizacija = 0.0
	for i in range(1, max_dim + 1):
		for j in range(1, max_dim + 1):
			sum_magnetizacija += s[i][j]
	return sum_magnetizacija

mH = 0.0


s = np.ones((max_dim + 2, max_dim + 2), dtype=int)

fm = open("f_m8.dat", "w")
fE = open("f_E8.dat", "w")
fT = open("f_T8.dat", "w")
fsG = open("f_spinG8.dat", "w")
fsD = open("f_spinD8.dat", "w")

# fm = open("f_m.dat", "w")
# fE = open("f_E.dat", "w")
# fT = open("f_T.dat", "w")
# fsG = open("f_spinG.dat", "w")
# fsD = open("f_spinD.dat", "w")

# fm = open("f_m32.dat", "w")
# fE = open("f_E32.dat", "w")
# fT = open("f_T32.dat", "w")
# fsG = open("f_spinG32.dat", "w")
# fsD = open("f_spinD32.dat", "w")

fm.write("#b, Mb, M, sigM\n")
fE.write("#b, Eb, E, sigE\n")
fT.write("#T, c, x\n")

# Pocetna konfiguracija
for i in range(1, max_dim + 1):
	for j in range(1, max_dim + 1):
		s[i][j] = 1
		print(f"{i}\t{j}\t{s[i][j]}")

for it in range(nT + 1):
	kT = kT0 + it * dkT
	SbM, SbE, SbE2, SbM2 = 0.0, 0.0, 0.0, 0.0
	reject = 0.0
	# pocetna energija i magnetizacija
	E = energija(s)
	# ZAD1: doraditi funkciju da racuna pocetnu magnetizaciju
	M = magnetizacija(s)
	print("\nT = %6.4lf K\n - pocetak:\n   E = %6.4lf\n   M = %6.4lf\n" % (kT, E, M))
	for ib in range(1, Nb + 1): # petlja po blokovima
		SkE, SkE2, SkM, SkM2 = 0.0, 0.0, 0.0, 0.0  ##############
			
		for ik in range(1, Nk + 1): # petlja po koracima
			# izaberi element od 1 do max
			i = int(1 + random.random() * max_dim)
			j = int(1 + random.random() * max_dim)
			s[i][j] *= -1 # promjena spina
			# periodicni rubni uvjeti, mijenjaju se samo kada zatrebaju
			s[i-1][j] = s[max_dim][j] if i == 1 else s[i-1][j]
			s[i+1][j] = s[1][j] if i == max_dim else s[i+1][j]
			s[i][j-1] = s[i][max_dim] if j == 1 else s[i][j-1]
			s[i][j+1] = s[i][1] if j == max_dim else s[i][j+1]
			# ZAD2: definirati promjenu magnetizacije i pravilno je odbaciti
			# dE = -2.0 * Jv * s[i,j] * (s[i + 1,j] + s[i - 1,j] + s[i,j + 1] + s[i,j - 1])
			dE = -2.0 * Jv* s[i][j] * (s[i+1][j]+s[i-1][j]+s[i][j+1] + s[i][j-1]) - 2.0 * s[i][j] * mH
			dM = 2.0 * s[i][j]

			if (dE > 0) and (np.exp(-dE / kT) <= np.random.rand()):
				s[i][j] *= -1              # odbaci promjenu
				reject += 1.0 / Nk / Nb    # postotak odbacenih koraka
				dE = 0.0
				dM = 0.0
				
			E += dE
			M += dM

			# ZAD3: izracunati magnetizaciju na osnovu prihvacene/neprihvacene promjene
			if ib > NbSkip:
				SkE += E
				SkE2 += E*E
				SkM += M
				SkM2 += M*M
			
			# ZAD4: sakupljati i uporosjeciti magnetizaciju
			#       (resetirati i dodati velicine gdje god je potrebno u kodu)
				
				
		if ib > NbSkip:
			SbE += SkE / Nk
			SbE2 += SkE2 / Nk
			SbM += SkM / Nk
			SbM2 += SkM2 / Nk
            
            
            # pohrama mape spinova u odvojenim datotekama
			if Swrite == 1:
				for i in range(1, max_dim + 1):
					for j in range(1, max_dim + 1):
						if s[i][j] == 1:
							fsG.write(f"{i}  {j}\n")
						if s[i][j] == -1:
							fsD.write(f"{i}  {j}\n")
				fsG.write("\n\n")
				fsD.write("\n\n")
			NbEff = ib - NbSkip
			aE = SbE / NbEff
			aE2 = SbE2 / NbEff
			sigmaE = np.sqrt(aE2 - aE * aE) / np.sqrt(NbEff)
			fE.write(f"{ib}  {SkE / Nk}  {aE}  {sigmaE}\n")
	# ZAD5: dodatno pohraniti kT, magnetizaciju i susceptibilnost
			aM = SbM / NbEff
			aM2 = SbM2 / NbEff
			sigmaM = np.sqrt(aM2 - aM * aM)  / np.sqrt(NbEff)
			fm.write(f"{ib}  {SkM / Nk}  {aM}  {sigmaM}\n")    # po bloku

	
	C = (aE2 - aE * aE) / (kT * kT)
	sus = (aM2 - aM * aM) / kT
	fT.write(f"{kT}  {C / (max_dim * max_dim)}  {sus / (max_dim * max_dim)} {aE / max_dim**2} {aM / max_dim**2}\n")    # nakon blokiranja
	fE.write("\n\n")
	print(f" - kraj:\n   <E> = {aE}\n")
	print(f" - prihvacenost {100 - reject * 100:.2f} % = \n")
	if Swrite == 1:
		print(" - konacni raspored spinova: f_spinG.dat i f_spinD.dat\n")

