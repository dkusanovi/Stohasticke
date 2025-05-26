import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# DORA KUSANOVIĆ 25.5.2025.

# vjerojatnost postizanja konsenzusa i broj koraka u ovisnosti o početnoj gustoći

# parametri
L = 10                                 # veličina stranice
N = L * L                              # ukupni broj ćelija
number_of_runs = 20                    # broj runova po početnoj gustoći
densities = np.linspace(0.1, 1.0, 50)  # različiti udjeli početne gustoće +1 rho_0  (ako je npr 0.3 onda 30% celija ima +1, a 70% ima -1)

probability_plus_consensus = []        # vjerojatnost da konsenzus bude +1
average_time_to_consensus = []         # prosječni broj koraka da se konsenzus postigne

def initialize_lattice(density):
    # stvara se rešetka s vrjednostima -1 ili +1, dimenzije rešetke, vjerojatnost
    return np.random.choice([-1, 1], size=(L, L), p = [1 - density, density])

def neighbors(i, j):
    return [
        ((i - 1) % L, j),             # gore
        ((i + 1) % L, j),             # dolje
        (i, (j - 1) % L),             # lijevo
        (i, (j + 1) % L)              # desno
    ]

def voting(grid):                                              # radi jednu promjenu po koraku
    i, j = random.randint(0, L - 1), random.randint(0, L - 1)  # nasumično biramo ćeliju (glasač)
    ni, nj = random.choice(neighbors(i, j))                    # nasumično biramu susjeda
    grid[i, j] = grid[ni, nj]                                  # glasač poprima mišljenje susjeda

def simulation(initial_density):
    # simulacija traje dok se konsenzus ne postigne
    grid = initialize_lattice(initial_density)
    steps = 0
    while not np.all(grid == grid[0, 0]):    # dok nisu sve iste vrijednosti
        voting(grid)
        steps = steps + 1
    return grid[0, 0], steps                 # konačna vrijednost i broj koraka

# simulacija za svaku početnu gustoću
for rho0 in densities:
    plus_count = 0        # koliko runova završi u +1 konsenzusu
    steps_list = []       # broj koraka za svaki run
    for _ in range(number_of_runs):
        final_value, steps = simulation(rho0)
        if final_value == 1:
            plus_count = plus_count + 1
        # if final_value == -1:
        #     minus_count = minus_count + 1        # ako želimo -1 konsenzus
        steps_list.append(steps)
    probability_plus = plus_count / number_of_runs
    average_steps = np.mean(steps_list)

    probability_plus_consensus.append(probability_plus)
    average_time_to_consensus.append(average_steps)

# graf: vjerojatnost da se postigne +1 konsenzus vs rno_0
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(densities, probability_plus_consensus, linestyle='None', marker='o', color="#4D8D5D")
plt.title('Vjerojatnost konsenzusa na +1 (L = 10)')
plt.xlabel('Početna gustoća +1 ćelija ($\u03C1_0$)')
plt.ylabel('Vjerojatnost konsenzusa +1')
plt.grid(True)

# graf: prosječno vrijeme do konsenzusa vs rho_0
plt.subplot(1, 2, 2)
plt.plot(densities, average_time_to_consensus, linestyle='None', marker='o', color="#614A8A")
plt.title('Prosječno vrijeme do konsenzusa (L = 10)')
plt.xlabel('Početna gustoća +1 ćelija ($\u03C1_0$)')
plt.ylabel('Broj koraka')
plt.grid(True)


# fitanje podataka
def logistic(x, k, x0):
    return 1 / (1 + np.exp(-k*(x - x0)))

def gaussian(x, A, mu, sigma):
    return A * np.exp(-((x - mu)**2) / (2*sigma**2))


# curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, check_finite=None, bounds=(-inf, inf), method=None, jac=None, *, full_output=False, nan_policy=None, **kwargs)

# returns:             # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
# popt:array Optimal values for the parameters so that the sum of the squared residuals of f(xdata, *popt) - ydata is minimized.
# The covariance matrix of those parameters (a measure of the uncertainty in the fit). - ovo nije potrebno u ovom slučaju
fit1_popt, _ = curve_fit(logistic, densities, probability_plus_consensus, p0=[10, 0.5])
fit2_popt, _ = curve_fit(gaussian, densities, average_time_to_consensus, p0=[max(average_time_to_consensus), 0.5, 0.1])

x_fit = np.linspace(0, 1.0, 200)

plt.subplot(1, 2, 1)
label1 = r"$f(\rho_0) = \frac{1}{1 + e^{-%.2f(\rho_0 - %.2f)}}$" % (fit1_popt[0], fit1_popt[1])
plt.plot(x_fit, logistic(x_fit, *fit1_popt), color="black", linestyle="-", label=label1)
plt.legend(fontsize=11)

plt.subplot(1, 2, 2)
A, mu, sigma = fit2_popt
label2 = r"$f(\rho_0) = %.1f \exp\left(-\frac{(\rho_0 - %.2f)^2}{2 \cdot %.2f^2}\right)$" % (A, mu, sigma)
plt.plot(x_fit, gaussian(x_fit, *fit2_popt), color="black", linestyle="-", label=label2)
plt.legend(fontsize=11)

plt.show()
