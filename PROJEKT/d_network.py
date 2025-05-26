import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.cm as cm
import networkx as nx

# Number of different opinions
Q = 4  # You can change this to 4, 5, etc.

def initialize_opinions_network(N, Q):
    opinions = []
    per_opinion = N // Q
    for i in range(Q):
        opinions += [i] * per_opinion
    opinions += list(np.random.choice(Q, N - len(opinions)))  # fill remainder
    np.random.shuffle(opinions)
    return {i: opinions[i] for i in range(N)}

def run_sznajd_network(G, opinions, max_steps=100000):
    for step in range(max_steps):
        node = np.random.choice(list(G.nodes))
        neighbors = list(G.neighbors(node))
        if not neighbors:
            continue
        neighbor = np.random.choice(neighbors)

        if opinions[node] == opinions[neighbor]:
            # Get neighbors of both nodes
            combined_neighbors = list(set(list(G.neighbors(node)) + list(G.neighbors(neighbor))))
            for n in combined_neighbors:
                opinions[n] = opinions[node]

        # Check for consensus
        if all(op == opinions[0] for op in opinions.values()):
            print(f"{step} steps to consensus.")
            break
    else:
        print("Max steps reached without consensus.")
    
    return opinions

def generate_color_map(Q):
    cmap = cm.get_cmap('tab10', Q)
    return {i: cmap(i) for i in range(Q)}

def plot_multiple_networks(networks, opinions_list, fractions, N, Q):
    cols = 3
    rows = int(np.ceil(len(networks) / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
    axs = axs.flatten()

    color_map = generate_color_map(Q)
    legend_elements = [
        Patch(facecolor=color_map[i], edgecolor='k', label=f'Mišljenje {i}')
        for i in range(Q)
    ]

    for i, (G, opinions, frac) in enumerate(zip(networks, opinions_list, fractions)):
        pos = nx.spring_layout(G, seed=42)
        node_colors = [color_map[opinions[n]] for n in G.nodes]
        nx.draw(G, pos, node_color=node_colors, node_size=10, edge_color='gray', alpha=0.4, ax=axs[i])
        axs[i].set_title(f"Udio: {int(frac * 100)}%")
        axs[i].axis('off')

    fig.legend(handles=legend_elements, loc='center right', title=f'N = {N}, Q = {Q}')
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.show()

# Simulation parameters
N = 500  # Number of individuals
fractions = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]

# Run simulations
networks = []
opinions_list = []

for frac in fractions:
    G = nx.barabasi_albert_graph(N, 3)
    opinions = initialize_opinions_network(N, Q)
    final_opinions = run_sznajd_network(G, opinions)
    networks.append(G)
    opinions_list.append(final_opinions)

# Plot results
plot_multiple_networks(networks, opinions_list, fractions, N, Q)
