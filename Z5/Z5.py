import numpy as np

n1 = 5*10**6
n2 = 4*10**5


x1 = np.random.random(n1)

A = np.exp(1)/(np.exp(1)-1)
r2 = np.random.random(n2)
x2 = -np.log(1-r2/A)

Fn1 = np.exp(-x1**2) / 1
px2 = (A * np.exp(-x2))
Fn2 = np.exp(-x2**2) / px2

procjena_Fn1 = np.average(Fn1)
procjena_Fn2 = np.average(Fn2)

# def varijanca(F, ave):
#     suma = 0.0
#     for x in F:
#         suma = suma + (x - ave)**2
#     return suma / len(F)

# sigma1 = varijanca(Fn1, procjena_Fn1)
# sigma2 = varijanca(Fn2, procjena_Fn2)

sigma1 = np.sqrt(np.var(Fn1))
sigma2 = np.sqrt(np.var(Fn2))

greska_n1 = sigma1/np.sqrt(n1)
greska_n2 = sigma2/np.sqrt(n2)


with open('Z5.txt', 'w', encoding='utf-8') as f:
    f.write(f"{'n (uzoraka)':<12} {n1:10d} {n2:10d}\n")
    f.write(f"{'F':<12} {procjena_Fn1:10.5f} {procjena_Fn2:10.5f}\n")
    f.write(f"{'σ':<12} {sigma1:10.4f} {sigma2:10.4f}\n")
    f.write(f"{'σ/sqrt(n)':<12} {greska_n1:10.6f} {greska_n2:10.6f}\n")

