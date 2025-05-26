import numpy as np
import random
import imageio.v2 as imageio
import matplotlib
matplotlib.use('Agg')       # pohranjuje datoteke bez prikazivanja 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# DORA KUSANOVIĆ 25.5.2025.

# LatticeFrame
def LatticeFrame(lattice, step, epsilon, m):
    fig, ax = plt.subplots(figsize=(6, 6), dpi=200)
    # prikazuje rešetku kao toplinsku kartu s trakom boja
    cax = ax.imshow(lattice, cmap='viridis', origin='lower', vmin=0, vmax=1)
    fig.colorbar(cax, ax=ax)
    ax.set_title(f"Step {step}, $\u03B5$={epsilon:.3f}, m={m}")
    canvas = FigureCanvas(fig)
    canvas.draw()
    Image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    image = Image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return image

def initialize_lattice(L):
    return np.random.rand(L, L)

def update_opinions(lattice, epsilon, m):
    L = lattice.shape[0]
    # nasumični odabir dviju ćelija
    i, j = random.randint(0, L - 1), random.randint(0, L - 1)
    k, l = random.randint(0, L - 1), random.randint(0, L - 1)
    Oi = lattice[i, j]
    Oj = lattice[k, l]
    if abs(Oi - Oj) < epsilon:   # uvjet
        delta = (m / 2) * (Oi - Oj)
        lattice[i, j] = lattice[i, j] - delta
        lattice[k, l] = lattice[k, l] + delta

# omogućava da se gif mijenja postavka pohranjuje li se gif ili ne tijekom simulacije bez prekidanja rada koda
steps_per_display_enabled = True
def enableStepsPerDisplay(enable: bool):
    global steps_per_display_enabled
    steps_per_display_enabled = enable

def simulation_gif(epsilon, m, max_steps, steps_per_display):
    L = int(np.sqrt(N))                # dimenzija rešetke
    lattice = initialize_lattice(L)    # ćelijama se pripisuje naumično mišljenje

    gif_name = f"eps{epsilon:.3f}_m{int(m*10)}.gif"
    # gif writer
    with imageio.get_writer(gif_name, mode='I', duration=0.3) as writer:
        for step in range(max_steps + 1):
            update_opinions(lattice, epsilon, m)
            if steps_per_display_enabled and (step % steps_per_display == 0):
                frame = LatticeFrame(lattice, step, epsilon, m)
                writer.append_data(frame)

    return lattice  # za histogram

# ploz svih konačnih histograma odjednom za sve parametre
def histograms(results, epsilon_values, m_values):
    fig, axes = plt.subplots(len(epsilon_values), len(m_values), figsize=(12, 8), sharex=True, sharey=True)
    for i, epsilon in enumerate(epsilon_values):
        for j, m in enumerate(m_values):
            # ako je len(epsilon_values)>1 onda je axes 2D array, tj. ima dva indeksa
            # bez te linije bude problem s duljinom epsilon_values liste
            ax = axes[i, j] if len(epsilon_values) > 1 else axes[j]
            lattice = results[(epsilon, m)]
            values = lattice.flatten()   # pretvori višedimenzionalan objekt u jednu listu
            ax.hist(values, bins=50, range=(0, 1), color='blue', alpha=0.7)
            ax.set_title(f"$\u03B5$={epsilon:.3f}, m={m}")
            if i == len(epsilon_values) - 1:
                ax.set_xlabel("Mišljenje")
            if j == 0:
                ax.set_ylabel("Broj ćelija")
            ax.grid(True)
    plt.tight_layout()
    plt.savefig("histogram_final.png")
    plt.close()

# parametri
N = 2500                                       # rešetka 50x50
epsilon_values = [10/255, 50/255, 100/255]     # parametar epsilon normiran
m_values = [0.3, 0.6] 
steps_per_display = 1000                       # svakih ovoliko koraka prikazuje se kadar u gifu
max_steps = 100000                             # ukupan broj koraka

enableStepsPerDisplay(True)                    # dopušta pohranjivanje gifa

results = {}                                   # otvaramo rječnik za pohraniti konačna stanja reštki za sve kombinacije parametara 
for epsilon in epsilon_values:
    for m in m_values:
        print(f"Run: \u03B5={epsilon:.3f}, m={m}")
        final_lattice = simulation_gif(epsilon, m, max_steps=max_steps, steps_per_display=steps_per_display)
        results[(epsilon, m)] = final_lattice  # za histogram

histograms(results, epsilon_values, m_values)