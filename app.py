import streamlit as st
import pandas as pd

# Ton lien de publication qui fonctionne enfin !
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="Eco-Master L2", page_icon="🎓", layout="centered")

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

st.title("🎓 Eco-Master : Objectif L2")
st.markdown("---")

try:
    df = load_data()
    
    # Sidebar pour filtrer les révisions
    with st.sidebar:
        st.header("🎯 Vos Objectifs")
        niveaux = st.multiselect("Choisir les niveaux", options=df['Niveau'].unique(), default=list(df['Niveau'].unique()))
        matieres = st.multiselect("Choisir les matières", options=df['Thème'].unique(), default=list(df['Thème'].unique()))

    # Filtrage des données
    mask = df['Niveau'].isin(niveaux) & df['Thème'].isin(matieres)
    filtered_df = df[mask]

    if filtered_df.empty:
        st.warning("Aucune question ne correspond à vos filtres dans le Sheets.")
    else:
        # Initialisation de la question dans la session
        if st.button("🎲 Nouvelle question au hasard", use_container_width=True):
            st.session_state.current_q = filtered_df.sample().iloc[0]
            st.session_state.reveal = False

        # Affichage de la question
        if 'current_q' in st.session_state:
            q = st.session_state.current_q
            
            st.info(f"**{q['Niveau']}** | **Matière :** {q['Thème']}")
            st.subheader(q['Question'])
            
            if st.button("💡 Voir la réponse"):
                st.session_state.reveal = True
            
            if st.session_state.get('reveal'):
                st.success(f"**Réponse :** {q['Réponse']}")

except Exception as e:
    st.error(f"Erreur de flux : {e}")
