import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Patch

# DORA KUSANOVIĆ 25.5.2025.

def initialize_lattice(L, fraction=0.0):   # fraction - pojedinci s mišljenjem +1
    # rešetka s vrijednostima 0 i 1
    size = L * L
    num_one = int(size * fraction)                       # koliko osoba u početku ima mišljenje 1
    num_zero = size - num_one                            # koliko osoba u početku ima mišljenje 0
    lattice = np.array([1]*num_one + [-1]*num_zero)  # array sa svim 0 i q
    np.random.shuffle(lattice)                                # nasumično se rešetki pripisuju vrijednosti iz arraya
    return lattice.reshape((L, L))                            # pretvara 1D listu u 2D rešetku

def neighbors(i, j, L):
    # šest susjeda od jedne ćelije (i, j)
    neighbors_list = []
    # za svakog susjeda računaju se njihove koordinate s periodičnim rubnim uvjetima
    for dx, dy in [(-1, 0), (1, 0), 
                   (0, -1), (0, 1), 
                   (-1, -1), (1, 1)]:
        ni, nj = (i + dx) % L, (j + dy) % L
        neighbors_list.append((ni, nj))
    return neighbors_list

def run_sznajd(L, fraction = 0.0, max_steps = 1000000):
    lattice = initialize_lattice(L, fraction)
    
    for step in range(max_steps):
        i, j = np.random.randint(0, L, size=2)                # nasumična ćelija
        ni, nj = neighbors(i, j, L)[np.random.randint(0, 6)]  # nasumični susjed
        
        if lattice[i, j] == lattice[ni, nj]:   # ako imaju isto mišljenje utječu na susjede
            opinion = lattice[i, j]
            # promjena mišljenja susjeda od para
            for x, y in neighbors(i, j, L) + neighbors(ni, nj, L):
                lattice[x, y] = opinion
        
        # provjerava je li konsenzus postignut
        if np.all(lattice == lattice[0, 0]):
            print(f"{step} steps to consensus.")
            break
    else:
        print("Max steps reached without consensus.")

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