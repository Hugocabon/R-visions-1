import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lien de ton Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="R-Vision 1", page_icon="🎓", layout="centered")

# --- FONCTIONS DE CHARGEMENT ---
@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

# --- SECTION 1 : QUIZ ---
def section_quiz():
    st.title("🎲 Quiz de Révision")
    try:
        df = load_data()
        themes_a_exclure = ['Orientation', 'Job', 'Méthode']
        df = df[~df['Thème'].isin(themes_a_exclure)]

        with st.sidebar:
            st.header("🎯 Filtres Quiz")
            matieres = st.multiselect("Matières", options=df['Thème'].unique(), default=list(df['Thème'].unique()))

        filtered_df = df[df['Thème'].isin(matieres)]

        if st.button("🎲 Nouvelle question", use_container_width=True):
            st.session_state.current_q = filtered_df.sample().iloc[0]
            st.session_state.answered = False

        if 'current_q' in st.session_state:
            q = st.session_state.current_q
            st.info(f"**{q['Niveau']}** | **{q['Thème']}**")
            st.markdown(f"### {q['Question']}")

            options_labels = [f"A) {q['A']}", f"B) {q['B']}", f"C) {q['C']}", f"D) {q['D']}"]
            choice = st.radio("Sélectionnez votre réponse :", options_labels, index=None)

            if st.button("Valider ✅") and choice:
                st.session_state.answered = True
                st.session_state.user_choice = choice[0]

            if st.session_state.get('answered'):
                bonne_rep = str(q['Réponse']).strip()
                if st.session_state.user_choice == bonne_rep:
                    st.success(f"Bravo ! La bonne réponse était la {bonne_rep}.")
                else:
                    st.error(f"Faux. La réponse était la {bonne_rep}.")
                with st.expander("🔎 Explication technique"):
                    st.write(q['Explication'])
    except Exception as e:
        st.error(f"Erreur de configuration : {e}")

# --- SECTION 2 : SIMULATEUR IS-LM ---
def section_simulateur():
    st.title("📈 Simulateur IS-LM")
    st.markdown("Visualise l'impact des chocs économiques en temps réel.")
    
    # Paramètres de simulation
    g = st.slider("Dépenses Publiques (G)", 10.0, 50.0, 20.0, help="Impacte la courbe IS")
    ms = st.slider("Offre de Monnaie (M)", 10.0, 50.0, 25.0, help="Impacte la courbe LM")
    
    y = np.linspace(0, 100, 100)
    # Modélisation simplifiée IS-LM
    is_curve = (80 + g - y) / 2 
    lm_curve = (0.5 * y - ms + 20)
    
    fig, ax = plt.subplots()
    ax.plot(y, is_curve, label='Courbe IS (Marché des biens)', color='#1f77b4', lw=2)
    ax.plot(y, lm_curve, label='Courbe LM (Marché monétaire)', color='#d62728', lw=2)
    
    ax.set_ylim(0, 50)
    ax.set_xlabel('Revenu National (Y)')
    ax.set_ylabel('Taux d’intérêt (r)')
    ax.legend()
    ax.grid(alpha=0.3)
    
    st.pyplot(fig)
    st.info("💡 **Analyse :** Une hausse de $G$ déplace **IS** vers la droite (Relance). Une hausse de $M$ déplace **LM** vers la droite (Expansion monétaire).")

# --- SECTION 3 : CALCULATEUR MATHS ---
def section_calculateur():
    st.title("🧮 Calculateur Matriciel")
    st.markdown("Calcule instantanément le déterminant d'une matrice $2 \\times 2$.")
    
    st.write("Matrice $A = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$")
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a", value=1.0)
        c = st.number_input("c", value=0.0)
    with col2:
        b = st.number_input("b", value=0.0)
        d = st.number_input("d", value=1.0)
        
    det = (a * d) - (b * c)
    st.latex(f"\\det(A) = ({a} \\times {d}) - ({b} \\times {c}) = {det}")
    
    if det == 0:
        st.error("⚠️ Cette matrice n'est pas inversible.")
    else:
        st.success("✅ Cette matrice est inversible !")

# --- NAVIGATION ---
with st.sidebar:
    st.title("🎮 Menu")
    nav = st.radio("Aller vers :", ["📖 Quiz", "📈 Simulateur IS-LM", "🧮 Calculateur Maths"])

if nav == "📖 Quiz":
    section_quiz()
elif nav == "📈 Simulateur IS-LM":
    section_simulateur()
elif nav == "🧮 Calculateur Maths":
    section_calculateur()
