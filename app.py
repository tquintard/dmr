import streamlit as st
from modules import plot_graph

# Titre principal
st.title("Data Maturity Review")

# Introduction
st.write("Veuillez choisir une RAG status pour chacun des critères ci-dessous. Vous pouvez également ajouter de nouveaux critères.")

# Variables pour stocker les critères et les réponses
if "labels" not in st.session_state:
    st.session_state.labels = [
        "Data model\ncompliance",
        "Completeness",
        "Maturity\nManagement",
        "Data Roles\nappointment",
        "Delivery\nProcess",
        "Tools/UX\nperformances",
        "Support\ncommissioning",
        "SZC\ncompliance"
    ]
if "responses" not in st.session_state:
    st.session_state.responses = {label: "N/A" for label in st.session_state.labels}
if "new_criteria_trigger" not in st.session_state:
    st.session_state.new_criteria_trigger = False  # État pour forcer la mise à jour

# Champ pour ajouter un nouveau critère
new_criteria = st.text_input("Ajouter un nouveau critère", key="new_criteria")

# Bouton pour ajouter un critère
if st.button("Ajouter le critère", key="add_button"):
    if new_criteria and new_criteria not in st.session_state.labels:
        st.session_state.labels.append(new_criteria)
        st.session_state.responses[new_criteria] = "N/A"
        st.session_state.new_criteria_trigger = not st.session_state.new_criteria_trigger  # Changer l'état pour forcer un rechargement
    elif not new_criteria:
        st.error("Le champ de texte est vide. Veuillez entrer un nom de critère.")
    elif new_criteria in st.session_state.labels:
        st.error("Ce critère existe déjà.")

# Affichage des critères et des boutons radio dans trois colonnes
num_columns = 3
columns = st.columns(num_columns)

for idx, label in enumerate(st.session_state.labels):
    col = columns[idx % num_columns]  # Répartition des critères dans les colonnes
    with col:
        st.session_state.responses[label] = st.radio(
            label,
            options=["Green", "Amber", "Red", "N/A"],
            key=f"{label}_{st.session_state.new_criteria_trigger}"  # Clé unique pour recharger dynamiquement
        )

# Bouton pour générer le graphique
if st.button("Lancer le graphique", key="generate_button"):
    # Traduire les réponses en scores pour le graphique
    response_to_score = {
        "Red": 1,
        "Amber": 2,
        "Green": 3
    }
    criteria, scores = [], []
    for label in st.session_state.labels:
        if st.session_state.responses[label] != "N/A":
            criteria.append(label)
            scores.append(response_to_score[st.session_state.responses[label]])

    # Appeler la fonction `generate_graph` pour créer le graphique
    fig = plot_graph.generate_graph(criteria, scores)

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)
