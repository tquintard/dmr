import matplotlib.pyplot as plt
import numpy as np

RAG = {1: "red", 2: "orange", 3: "green", 1.5: "gray", 2.5: "gray"}

def xlabel_position(angle):
    if 0 < angle < np.pi:
        v_align = "bottom"
    elif np.pi < angle < 2 * np.pi:
        v_align = "top"
    else:
        v_align = "center"

    if 0 <= angle < np.pi / 2 or 3 * np.pi / 2 < angle <= 2 * np.pi:
        h_align = "left"
    elif np.pi / 2 < angle < 3 * np.pi / 2:
        h_align = "right"
    else:
        h_align = "center"

    return v_align, h_align

def generate_graph(criteria, scores):
    nb_crit = len(criteria)
    values = scores + [scores[0]]
    angles = np.linspace(0, 2 * np.pi, nb_crit, endpoint=False).tolist()
    angles.append(angles[0])

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for val, rag in RAG.items():
        lw = 1.5 if int(val) == val else 0.5
        ax.plot(
            np.linspace(0, 2 * np.pi, nb_crit + 1),
            [val] * (nb_crit + 1),
            color=rag,
            lw=lw,
            linestyle=":"
        )

    #ax.fill(angles, values, color="black", alpha=0.15)
    ax.plot(angles, values, color="black", linewidth=3, alpha=0.7)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([""] * nb_crit)
    ax.set_yticklabels([], visible=False)

    for angle, label, score in zip(angles[:-1], criteria, scores):
        va, ha = xlabel_position(angle)
        ax.text(angle, 3, label, fontsize=12, color=RAG[score], fontweight="bold", ha=ha, va=va)
        ax.plot([angle, angle], [0, 3], color="gray", lw=0.5, linestyle=":")

    ax.spines["polar"].set_visible(False)
    ax.grid(visible = False)
    return fig
