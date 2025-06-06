import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Patch

# DORA KUSANOVIĆ 5.6.2025.

def initialize_lattice(L, fraction=0.0):   # fraction - pojedinci s mišljenjem +1
    # rešetka s vrijednostima 0 i 1
    size = L * L
    num_one = int(size * fraction)                            # koliko osoba u početku ima mišljenje 1
    num_zero = size - num_one                                 # koliko osoba u početku ima mišljenje 0
    lattice = np.array([1]*num_one + [0]*num_zero)           # array sa svim 0 i 1
    np.random.shuffle(lattice)                                # nasumično se rešetki pripisuju vrijednosti iz arraya
    return lattice.reshape((L, L))                            # pretvara 1D listu u 2D rešetku


def neighbors(i, j, L):
    return [((i - 1) % L, j),
            ((i + 1) % L, j),
            (i, (j - 1) % L),
            (i, (j + 1) % L)]



def run_sznajd(L, fraction=0.0, max_steps=1000000):
    lattice = initialize_lattice(L, fraction)
    
    for step in range(max_steps):
        i, j = np.random.randint(0, L, size=2)           # nasumična ćelija
        nbs_ij = neighbors(i, j, L)
        ni, nj = nbs_ij[np.random.randint(0, len(nbs_ij))]  # nasumični susjed

        if lattice[i, j] == lattice[ni, nj]:
            opinion = lattice[i, j]

            # Union of neighbors of both (i,j) and (ni,nj)
            six_neighbors = neighbors(i, j, L) + neighbors(ni, nj, L)
            
            # Optional: exclude (i,j) and (ni,nj) themselves
            six_neighbors = set(six_neighbors) - {(i, j), (ni, nj)}

            for x, y in six_neighbors:
                lattice[x, y] = opinion

        if np.all(lattice == lattice[0, 0]):
            print(f"{step} koraka do konsenzusa.")
            break
    else:
        print("Maksimalan broj koraka bez konsenzusa.")

    return lattice


L = 100

def plot(lattices, fractions, L):       # crta sva konačna stanja za različite udjele +1, tj. za različite majorities
    num = len(lattices)
    cols = 3                            # u 3 stupca
    rows = int(np.ceil(num / cols))     # koliko je potrebno redaka - najmanji int geq num/cols

    cmap = colors.ListedColormap(['magenta', 'blue'])   # dvije boje za grafički prikaz dvaju mišljenja

    fig, axs = plt.subplots(rows, cols, figsize=(12, 8))
    axs = axs.flatten()

    for i in range(num):
        axs[i].imshow(lattices[i], cmap=cmap, vmin=0, vmax=1)
        axs[i].set_title(f"Udio: {int(fractions[i]*100)}%")
        axs[i].grid(color='gray', linestyle='-', linewidth=0.1)

    legend_elements = [
        Patch(facecolor='magenta', edgecolor='k', label='Mišljenje 0'),
        Patch(facecolor='blue', edgecolor='k', label='Mišljenje 1')
    ]

    fig.tight_layout(rect=[0, 0, 0.9, 1])
    fig.legend(handles=legend_elements, loc='center right', bbox_to_anchor=(1.0, 0.5), title=f'L = {L}')
    plt.show()

fractions = [0.01, 0.05, 0.10, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
lattices = [run_sznajd(L, f) for f in fractions]
plot(lattices, fractions, L)