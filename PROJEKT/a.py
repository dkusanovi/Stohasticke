import numpy as np
import random
import matplotlib.pyplot as plt

# DORA KUSANOVIĆ 25.5.2025.

# parametri
number_of_runs = 20  # broj runova
sizes_1d = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
sizes_2d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # N = LxL
sizes_3d = [1, 2, 3, 4, 5]  # N = LxLxL
initial_density = 0.3


def initialize_lattice(shape, density):
    return np.random.choice([-1, 1], size=shape, p=[1 - density, density])


def neighbors_1d(i, L):
    return [(i - 1) % L, (i + 1) % L]

def neighbors_2d(i, j, L):
    return [((i - 1) % L, j), 
            ((i + 1) % L, j), 
            (i, (j - 1) % L), 
            (i, (j + 1) % L)]

def neighbors_3d(i, j, k, L):
    return [
        ((i - 1) % L, j, k), 
        ((i + 1) % L, j, k),
        (i, (j - 1) % L, k), 
        (i, (j + 1) % L, k),
        (i, j, (k - 1) % L), 
        (i, j, (k + 1) % L)
    ]


def vote_1d(lattice):
    L = len(lattice)
    i = random.randint(0, L - 1)            # nasumičan odabir glasača
    ni = random.choice(neighbors_1d(i, L))  # nasumičan odabir susjeda
    lattice[i] = lattice[ni]                # glasač poprima mišljenje susjeda
    return lattice

def vote_2d(lattice):
    L = lattice.shape[0]
    i, j = random.randint(0, L - 1), random.randint(0, L - 1)
    ni, nj = random.choice(neighbors_2d(i, j, L))
    lattice[i, j] = lattice[ni, nj]
    return lattice

def vote_3d(lattice):
    L = lattice.shape[0]
    i, j, k = random.randint(0, L - 1), random.randint(0, L - 1), random.randint(0, L - 1)
    ni, nj, nk = random.choice(neighbors_3d(i, j, k, L))
    lattice[i, j, k] = lattice[ni, nj, nk]
    return lattice

def simulation(dimension, size, density):
    # proces se ponavlja do konsenzusa
    if dimension == 1:
        lattice = initialize_lattice((size,), density)
        vote_fn = vote_1d
    elif dimension == 2:
        lattice = initialize_lattice((size, size), density)
        vote_fn = vote_2d
    elif dimension == 3:
        lattice = initialize_lattice((size, size, size), density)
        vote_fn = vote_3d

    steps = 0
    # dok sve ćelije nemaju isto mišljenje
    while not np.all(lattice == lattice.flat[0]):
        lattice = vote_fn(lattice)
        steps = steps + 1
    return steps

def run_dimensions():
    results_time = {'1D': [], '2D': [], '3D': []}
    sizes = {'1D': sizes_1d, '2D': sizes_2d, '3D': sizes_3d}  # duljine L
    Ns = {'1D': [], '2D': [], '3D': []}                       # ukupan broj ćelija u rešetci za n-dim

    for dim in ['1D', '2D', '3D']:
        for size in sizes[dim]:
            print(f"{dim}, size = {size}")
            total_steps = 0
            for _ in range(number_of_runs):
                if dim == '1D':
                    N = size                                      # ukupan broj ćelija u 1D                           
                    steps = simulation(1, size, initial_density)
                elif dim == '2D':
                    N = size**2                                   # ukupan broj ćelija u 2D
                    steps = simulation(2, size, initial_density)
                elif dim == '3D':
                    N = size**3                                   # ukupan broj ćelija u 3D
                    steps = simulation(3, size, initial_density)
                total_steps = total_steps + steps
            average_time = total_steps / number_of_runs
            results_time[dim].append(average_time)
            Ns[dim].append(N)
    return Ns, results_time

Ns, results_time = run_dimensions()

plt.figure(figsize=(10, 6))

Ns_1d = np.array(Ns['1D'])
res_1d = np.array(results_time['1D'])
Ns_2d = np.array(Ns['2D'])
res_2d = np.array(results_time['2D'])
Ns_3d = np.array(Ns['3D'])
res_3d = np.array(results_time['3D'])

N_line_1d = np.linspace(1, max(Ns_1d) * 1.5, 500)
N_line_2d = np.linspace(2, max(Ns_2d) * 1.5, 500)  # krecemo od 2 umjesto 1 da ne računa ln(1)=0 jer neće crtati funkciju
N_line_3d = np.linspace(1, max(Ns_3d) * 1.5, 500)

# koeficijent smjera za 1D
# formula se dobija kao t = koeficijent x funkcija po kojoj se skalira (gdje je t vrijeme do konsenzusa)
coefficient_1d = np.mean(res_1d[-6:] / Ns_1d[-6:]**2)                                             # ne koristimo prvih nekoliko članova liste za izračun koeficijenta zbog manjeg broja podataka u takvim rešetkama
# parametar skaliranja za 2D                                                                      # tada izračun koeficijenta bude lošiji i fit ne prati najbolje
coefficient_2d = np.mean(res_2d[-3:] / (Ns_2d[-3:]*np.log(Ns_2d[-3:])))
#parametar skaliranja 3D
coefficient_3d = np.mean(res_3d[-3:] / Ns_3d[-3:])

plt.plot(Ns_1d, res_1d, 'bo', label='1D podaci')
plt.plot(Ns_2d, res_2d, 'ro', label='2D podaci')
plt.plot(Ns_3d, res_3d, 'go', label='3D podaci')

plt.plot(N_line_1d, coefficient_1d * N_line_1d**2, 'b-', label='fit 1D: $N^2$')
plt.plot(N_line_2d, coefficient_2d * N_line_2d*np.log(N_line_2d), 'r-', label='fit 2D: $N \\ln N$')
plt.plot(N_line_3d, coefficient_3d * N_line_3d, 'g-', label='fit 3D: $N$')

plt.xlabel('Broj ćelija (N)')
plt.ylabel('Prosječno vrijeme do konsenzusa')
plt.title('Vrijeme konsenzusa u 1D, 2D, 3D za model glasača')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.xlim(0, 130)
plt.show()