import matplotlib.pyplot as plt
import numpy as np

RAG = {1: "red", 2: "orange", 3: "green", 1.5: "gray", 2.5: "gray"}

def xlabel_position(angle):

    #vertical alignment
    if 0 < angle < np.pi:
        v_align = "bottom"
    elif np.pi < angle < 2*np.pi:
        v_align = "top"
    else:
        v_align = "center"

    #horizontal alignment
    if 0 <= angle < np.pi/2 or 3*np.pi/2 < angle <= 2*np.pi:
        h_align = "left"
    elif np.pi/2 < angle < 3*np.pi/2:
        h_align = "right"
    else:
        h_align = "center"

    return v_align, h_align

# Données des critères et leurs scores
criteria = [
    "Data model\ncompliance",
    "Completeness",
    "Maturity\nManagement",
    "Data Roles\nappointment",
    "Delivery\nProcess",
    "Tools/UX\nperformances",
    "Support\ncommissioning",
    "SZC\ncompliance"]#,
#    "Other\nopportunities"
#]
nb_crit = len(criteria)
scores = [3,3,1,3,3,2,2,3]

# Préparation des données pour le graphique radar
values = scores
values.append(values[0])  # Boucler le graphique (fermer le polygone)

# Calcul des angles
angles = np.linspace(0, 2 * np.pi, nb_crit, endpoint=False).tolist()
angles.append(angles[0])

# Création du graphique radar
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Couleurs pour les cercles concentriques
circle_colors = ['red', 'orange', 'green']

#Ajouter des cercles colorés en pointillés pour les yticks
for val, rag in RAG.items():  # Commence à 1 pour les scores
    lw = 1.5 if int(val) == val else 0.5
    ax.plot(
        np.linspace(0, 2 * np.pi, nb_crit + 1),
        [val] * (nb_crit + 1),
        color=rag,
        lw=lw,
        linestyle=':'
    )

# Ajout des données
ax.fill(angles, values, color="black", alpha=0.15)
ax.plot(angles, values, color='black', linewidth=3, alpha=0.7) 

# Suppression des étiquettes x existantes
ax.set_xticks([])

# Configuration des ticks
ax.set_yticklabels(labels="", visible=False)
ax.set_xticks(angles[:-1])  # Critères
ax.set_xticklabels(['']*len(criteria))

# Suppression de la grille intérieure (lignes grises)
ax.grid(visible = False)

# Ajout manuel des étiquettes à l’extérieur du cercle externe
for angle, label, score in zip(angles[:-1], criteria, scores):
    va, ha = xlabel_position(angle)
    ax.text(
        angle, 3,  # Angle et rayon pour placer les étiquettes
        label,
        fontsize=12,
        color= RAG[score],
        fontweight = "bold",
        ha=ha,
        va=va,
        #backgroundcolor='white',
        #rotation=np.degrees(angle),  # Aligner avec l'angle
        rotation_mode="anchor"
    )
    ax.plot([angle,angle], [0,3], color='gray', lw=0.5,linestyle=':')

# Suppression de l'anneau extérieur pour concentricité et cohérence
ax.spines['polar'].set_visible(False)


# Affichage
plt.show()




    