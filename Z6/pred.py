# rho(X, t+1) - rh(X, t) = - suma po X' rho (X,t)T(X->X') + suma po X' rho (X', t)T(X'->X)
# zahtijevamo: rho(X,t)T(X->X') = rho(X',t)T(X'->X) za svaki X', X detaljna ravnoteza
# p(xi)T(Xi->Xj) = p(xj)T(Xj->Xi)
# T(Xi->Xj) = min[1, p(xi)/p(xj)]
# pp: p(xi) > p(xj) => p(xi)/p(xj) > 1
# T(Xi->Xj) = 1
# T(Xj->Xi) = min[1, p(xi)/p(xj)] = p(xi)/p(xj)


import numpy as np
import random
import matplotlib.pyplot as plt

delta = 1
n = 100  # broj setaca
k = 1000 # broj koraka
x0 = 0 # pocetna vrijednost x
x = x0
prihvaceno = [x] # prihvacena promjena
func = []  # rjesenja integrala

def p_proba(x):
    return np.exp(-x**2/2)

def f(x):
    return x**2

Im = []
ImN = []


for i in range(1,n):
    for j in range(1,k):
        delta_i = np.random.uniform(-delta, delta)
        x_proba = x + delta_i

        w = p_proba(x_proba) / p_proba(x)

        if w >= 1:
            x = x_proba
        else:
            r = random.random()
            if r <= w:
                x = x_proba

        prihvaceno.append(x)
        func.append(f(x))
        Im.append(x**2/i)
        ImN.append(x**2/(i*j))

klist = []
for nn in range(1,n):
    for kk in range(1,k):
        klist.append(kk)

integral = np.average(func)
print(integral)

plt.figure(figsize=(10, 6))
# plt.ylim(-1.2, 1.2)
plt.plot(klist, Im, label='')
plt.plot(klist, ImN, label='')
plt.xlabel('')
plt.ylabel('')
plt.title('')
plt.grid(True)
plt.legend()
plt.show()





























# plt.hist(prihvaceno, bins=50, density=True, alpha=0.6, label="prihvaceno")
# xevi = np.linspace(-8, 8, 1000)
# plt.plot(xevi, p_proba(xevi)/np.trapz(p_proba(xevi), xevi), 'r-', label="???")
# plt.title("Histogram")
# plt.xlabel("x")
# plt.ylabel("gustoća vjerojatnosti")
# plt.legend()
# plt.show()

