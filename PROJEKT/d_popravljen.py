import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Patch

# DORA KUSANOVIĆ 5.6.2025.

def initialize_lattice(L, Q):       # Q je broj mišljenja
    size = L * L
    lattice = np.random.randint(Q, size=size)
    return lattice.reshape((L, L))  

# za razliku prošloga problema, ovdje nije zadan udio osoba s nekim mišljenjem
# Q mišljenja je uniformno raspoređen unutar 0 do Q-1 intervala (gdje me mišljenje cijeli broj)

def neighbors(i, j, L):
    return [((i - 1) % L, j),
            ((i + 1) % L, j),
            (i, (j - 1) % L),
            (i, (j + 1) % L)]

def run_sznajd(L, fraction=0.0, max_steps=1000000):
    lattice = initialize_lattice(L, fraction)
    
    for step in range(max_steps):
        i, j = np.random.randint(0, L, size=2)              # nasumična ćelija
        nbs_ij = neighbors(i, j, L)
        ni, nj = nbs_ij[np.random.randint(0, len(nbs_ij))]  # nasumični susjed

        if lattice[i, j] == lattice[ni, nj]:
            opinion = lattice[i, j]

            # svi susjedi - 6
            six_neighbors = neighbors(i, j, L) + neighbors(ni, nj, L)
            
            # uklanjamo glavnu ćeliju i odabranog susjeda
            six_neighbors = set(six_neighbors) - {(i, j), (ni, nj)}

            for x, y in six_neighbors:
                lattice[x, y] = opinion

        if np.all(lattice == lattice[0, 0]):
            return lattice, f'{step} koraka do konsenzusa.'
    return lattice, 'Milijun koraka bez konsenzusa.'


L = 80

def plot(lattices, Q, L):
    num = len(lattices)
    cols = 3
    rows = int(np.ceil(num / cols))

    colors_list = plt.cm.tab10.colors  # tab10 ima do 10 boja što znači da ovo funkcionira do 10 mišljenja
    cmap = colors.ListedColormap(colors_list[:Q])

    fig, axs = plt.subplots(rows, cols, figsize=(12, 8))
    axs = axs.flatten()

    for i in range(num):
        lattice, consensus = results[i]
        axs[i].imshow(lattice, cmap=cmap, vmin=0, vmax=Q-1)
        axs[i].set_title(f"Pokušaj {i+1}\n{consensus}")
        axs[i].grid(color='gray', linestyle='-', linewidth=0.1)

    legend_elements = [
        Patch(facecolor=colors_list[i], edgecolor='k', label=f'Mišljenje {i}') for i in range(Q)
    ]

    fig.tight_layout(rect=[0, 0, 0.9, 1])
    fig.legend(handles=legend_elements, loc='center right', bbox_to_anchor=(1.0, 0.5), title=f'L = {L}')
    plt.show()

Q = 4
results = [run_sznajd(L, Q) for _ in range(6)]  # nekoliko (6) pokušaja do konsenzusa
plot(results, Q, L)