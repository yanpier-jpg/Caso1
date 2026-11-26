# dfa_cli_compacto.py — versión visual idéntica al diagrama lineal
import sys, matplotlib.pyplot as plt, networkx as nx
from matplotlib.patches import FancyArrowPatch

# === Definición del DFA ===
states = {
    "Inicio de\ntrámite", "Pagar tasa\nen banco", "Tomar foto\ny huellas",
    "Verificar\ndatos", "Imprimir\nDNI", "Entregar\ncomprobante", "DNI\nEntregado"
}
alphabet = {"a", "b", "c"}
delta = {
    ("Inicio de\ntrámite", "a"): "Pagar tasa\nen banco",
    ("Pagar tasa\nen banco", "a"): "Tomar foto\ny huellas",
    ("Tomar foto\ny huellas", "a"): "Tomar foto\ny huellas",
    ("Tomar foto\ny huellas", "c"): "Verificar\ndatos",
    ("Verificar\ndatos", "a"): "Imprimir\nDNI",
    ("Verificar\ndatos", "b"): "Entregar\ncomprobante",
    ("Imprimir\nDNI", "a"): "Entregar\ncomprobante",
    ("Entregar\ncomprobante", "b"): "Verificar\ndatos",
    ("Entregar\ncomprobante", "a"): "DNI\nEntregado"
}

q0, F = "Inicio de\ntrámite", {"DNI\nEntregado"}

# === Simulación ===
def run(s):
    q, steps = q0, [q0]
    for i, ch in enumerate(s):
        if (q, ch) not in delta:
            raise ValueError(f"Sin transición desde {q.replace(chr(10), ' ')} con '{ch}' en pos {i}")
        q = delta[(q, ch)]
        steps.append(q)
    return steps, steps[-1] in F

# === Grafo y layout ===
G = nx.MultiDiGraph()
G.add_nodes_from(states)
for (q, a), p in delta.items():
    G.add_edge(q, p, key=a, label=a)

pos = {
    "Inicio de\ntrámite": (-6, 0),
    "Pagar tasa\nen banco": (-4, 0),
    "Tomar foto\ny huellas": (-2, 0),
    "Verificar\ndatos": (0, 0),
    "Imprimir\nDNI": (2, 0),
    "Entregar\ncomprobante": (4, 0),
    "DNI\nEntregado": (6, 0)
}

# === Dibujo por paso ===
def draw_step(current, idx, sym=None):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(14, 5.5)
    fig.patch.set_facecolor("#182635")
    ax = plt.gca()
    ax.set_facecolor("#182635")

    # Cuadrícula sutil de fondo
    ax.set_xticks([x * 0.5 for x in range(-15, 16)])
    ax.set_yticks([y * 0.5 for y in range(-5, 6)])
    ax.grid(True, color="#23364a", linewidth=0.8, zorder=0)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    nodes = list(G.nodes())
    # Halo exterior brillante y nodos
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=[3800 if n == current else 3200 for n in nodes], node_color="#182635", edgecolors="#26879c", linewidths=5, alpha=0.45)
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=[3300 if n == current else 2800 for n in nodes], node_color="#182635", edgecolors="#4deeea", linewidths=2.5)
    # Doble círculo para el estado final
    nx.draw_networkx_nodes(G, pos, nodelist=list(F), node_size=2100, node_color="#182635", edgecolors="#4deeea", linewidths=2)
    nx.draw_networkx_labels(G, pos, font_size=8.5, font_color="white", font_weight="bold")

    # Flecha inicial hacia 'Inicio de trámite'
    ax.annotate("", xy=(-6.62, 0), xytext=(-7.3, 0), arrowprops=dict(arrowstyle="-|>", color="#4deeea", lw=2, mutation_scale=16))

    for u, v, k, d in G.edges(keys=True, data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        if u == v:
            ax.add_patch(FancyArrowPatch((x1 - 0.25, y1 + 0.55), (x1 + 0.25, y1 + 0.55), connectionstyle="arc3,rad=-1.5", arrowstyle="-|>", color="#4deeea", lw=1.8, mutation_scale=15))
            ax.text(x1, y1 + 1.25, d["label"], fontsize=11, color="#4deeea", ha="center", fontweight="bold")
        elif abs(x2 - x1) > 2:
            rad = -0.42 if x1 < x2 else -0.42
            ax.add_patch(FancyArrowPatch((x1, y1 + (0.62 if x1 < x2 else -0.62)), (x2, y2 + (0.62 if x1 < x2 else -0.62)), connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>", color="#4deeea", lw=1.8, mutation_scale=16))
            ax.text((x1 + x2) / 2, 1.55 if x1 < x2 else -1.65, d["label"], fontsize=11, color="#4deeea", ha="center", fontweight="bold")
        else:
            ax.annotate("", xy=(x2 - 0.65, y2), xytext=(x1 + 0.65, y1), arrowprops=dict(arrowstyle="-|>", color="white", lw=1.8, mutation_scale=15))
            ax.text((x1 + x2) / 2, 0.18, d["label"], fontsize=11, color="white", ha="center", fontweight="bold")

    ax.set_xlim(-7.4, 7.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_title(f"Paso {idx}: {current.replace(chr(10), ' ')}" + (f" | '{sym}'" if sym else ""), color="white", fontsize=12, pad=10)
    plt.tight_layout()
    plt.pause(1.0)

# === core/main ===
if __name__ == '__main__':
    s = sys.argv[1] if len(sys.argv) > 1 else input("Cadena (a/b/c): ").strip()
    try:
        steps, ok = run(s)
        print("ACEPTA" if ok else "RECHAZA", f"(estado final: {steps[-1].replace(chr(10), ' ')})")
        plt.ion()
        draw_step(steps[0], 0)
        for i, ch in enumerate(s, 1):
            draw_step(steps[i], i, ch)
        plt.ioff()
        plt.show()
    except Exception as e:
        print("RECHAZA:", e)