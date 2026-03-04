import streamlit as st
import pandas as pd
import random

# Ton lien export CSV vérifié
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-JEZTqNXVx6whsY5XOpcsDk1ujSvLN2p-KRzng3fBeKo/export?format=csv"

st.set_page_config(page_title="Eco-Gestion L2 Prep", page_icon="🎓")

@st.cache_data(ttl=60)
def load_data():
    # On lit le CSV depuis Google Sheets
    return pd.read_csv(SHEET_URL)

st.title("🎓 Objectif L2 Éco-Gestion")
st.markdown("---")

try:
    df = load_data()
    
    # On s'assure que les colonnes sont bien nommées
    df.columns = [c.strip() for c in df.columns]

    # Filtres dans la barre latérale
    with st.sidebar:
        st.header("Paramètres")
        themes = ["Tous"] + list(df['Thème'].unique())
        selected_theme = st.selectbox("Matière", themes)

    # Filtrage
    filtered_df = df if selected_theme == "Tous" else df[df['Thème'] == selected_theme]

    if st.button("🎲 Question au hasard"):
        st.session_state.current_q = filtered_df.sample().iloc[0]
        st.session_state.reveal = False

    if 'current_q' in st.session_state:
        q = st.session_state.current_q
        st.info(f"Domaine : {q['Thème']} | Niveau : {q['Niveau']}")
        st.subheader(q['Question'])
        
        if st.button("💡 Voir la réponse"):
            st.session_state.reveal = True
            
        if st.session_state.get('reveal'):
            st.success(f"**Réponse :** {q['Réponse']}")

except Exception as e:
    st.error("⚠️ L'application n'arrive pas à lire ton Google Sheet.")
    st.write("Vérifie l'étape 2 ci-dessous pour 'connecter' ton fichier.")
