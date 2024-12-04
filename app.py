import streamlit as st
from plot_graph import generate_graph

# Activer le mode large
st.set_page_config(layout="wide")

# Dictionnaire des catégories et critères initiaux
dict_labels = {
    "Quality": ["Data model\ncompliance", "Completeness", "Maturity\nManagement"],
    "Process & Roles": ["Data Roles\nappointment", "Delivery\nProcess", "Tools/UX\nperformances"],
    "Usage & Benefits": ["Support\ncommissioning", "SZC\ncompliance"],
}

# Initialisation des états de l'application
if "categories" not in st.session_state:
    st.session_state.categories = dict_labels
if "responses" not in st.session_state:
    st.session_state.responses = {cat: {} for cat in dict_labels.keys()}

# Titre principal
st.title("Data Maturity Review")

# Introduction
st.write("Veuillez choisir une RAG status pour chacun des critères ci-dessous. Vous pouvez également ajouter de nouveaux critères.")

# Champ pour ajouter un nouveau critère
new_criteria = st.text_input("Ajouter un nouveau critère", key="new_criteria")

# Choisir la catégorie
new_crit_cat = st.selectbox("Choisir la catégorie associée au critère à ajouter", st.session_state.categories.keys())

# Bouton pour ajouter un critère
if st.button("Ajouter le critère"):
    if new_criteria:
        # Ajouter le critère à la catégorie sélectionnée
        if new_criteria not in st.session_state.categories[new_crit_cat]:
            st.session_state.categories[new_crit_cat].append(new_criteria)
            st.session_state.responses[new_crit_cat][new_criteria] = "N/A"
        else:
            st.error("Ce critère existe déjà.")
    else:
        st.error("Le champ de texte est vide. Veuillez entrer un nom de critère.")

# Organisation en 3 colonnes principales (une par catégorie)
main_columns = st.columns(len(st.session_state.categories))
for main_col, (cat, labels) in zip(main_columns, st.session_state.categories.items()):
    with main_col:
        st.subheader(cat, divider= "rainbow")
        # Diviser chaque catégorie en 3 sous-colonnes
        sub_columns = st.columns(3)
        for idx, label in enumerate(labels):
            sub_col = sub_columns[idx % 3]  # Répartir les critères entre les 3 sous-colonnes
            with sub_col:
                st.session_state.responses[cat][label] = st.radio(
                    label,
                    options=["Green", "Amber", "Red", "N/A"],
                    key=f"{cat}_{label}"
                )

# Bouton pour générer le graphique
if st.button("Générer Radar Plot"):
    response_to_score = {"Red": 1, "Amber": 2, "Green": 3}
    scores = list()
    criteria = list()
    for cat, labels in st.session_state.categories.items():
        for label in labels:
            response = st.session_state.responses[cat][label]
            if response != "N/A":
                criteria.append(label)
                scores.append(response_to_score[response])

    # Générer et afficher le graphique
    fig = generate_graph(criteria, scores)
    st.pyplot(fig, use_container_width=False)
