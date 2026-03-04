import streamlit as st
import pandas as pd

# Ton lien magique (celui qui finit par export?format=csv)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-JEZTqNXVx6whsY5XOpcsDk1ujSvLN2p-KRzng3fBeKo/export?format=csv"

st.set_page_config(page_title="Eco-Gestion L2 Prep", page_icon="🎓")

@st.cache_data(ttl=60)
def load_data():
    # 'sep=None' détecte automatiquement si c'est une virgule (,) ou un point-virgule (;)
    # 'engine=python' est nécessaire pour cette détection automatique
    df = pd.read_csv(SHEET_URL, sep=None, engine='python')
    # Nettoyage des espaces dans les noms de colonnes
    df.columns = [c.strip() for c in df.columns]
    return df

st.title("🎓 Objectif L2 Éco-Gestion")
st.markdown("---")

try:
    df = load_data()
    
    # On identifie les colonnes pour que l'app ne crash pas si les noms changent
    col_theme = 'Thème' if 'Thème' in df.columns else df.columns[1]
    col_question = 'Question' if 'Question' in df.columns else df.columns[2]
    col_reponse = 'Réponse' if 'Réponse' in df.columns else df.columns[3]

    with st.sidebar:
        st.header("Paramètres")
        themes = ["Tous"] + list(df[col_theme].unique())
        selected_theme = st.selectbox("Matière", themes)

    # Filtrage
    filtered_df = df if selected_theme == "Tous" else df[df[col_theme] == selected_theme]

    if st.button("🎲 Tirer une question au sort"):
        st.session_state.current_q = filtered_df.sample().iloc[0]
        st.session_state.reveal = False

    if 'current_q' in st.session_state:
        q = st.session_state.current_q
        st.info(f"Domaine : {q[col_theme]}")
        st.subheader(q[col_question])
        
        if st.button("💡 Voir la solution"):
            st.session_state.reveal = True
            
        if st.session_state.get('reveal'):
            st.success(f"**Réponse :** {q[col_reponse]}")

except Exception as e:
    st.error("⚠️ Problème de lecture du Google Sheet.")
    st.write("Vérifie bien que ton Sheets est en accès 'Tous les utilisateurs disposant du lien'.")
    st.write(f"Erreur technique : {e}")
