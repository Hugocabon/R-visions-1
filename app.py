import streamlit as st
import pandas as pd

# Ton lien export CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="Debug Eco-App", page_icon="🧪")

st.title("🧪 Diagnostic de l'App")

try:
    # 1. Tentative de lecture brute
    df = pd.read_csv(SHEET_URL)
    
    # 2. Nettoyage automatique des noms de colonnes (enlève les espaces invisibles)
    df.columns = df.columns.str.strip()
    
    st.success("✅ Données chargées avec succès !")
    
    # Affichage des colonnes trouvées pour vérification
    st.write("Colonnes détectées :", list(df.columns))
    
    # Aperçu des 3 premières lignes
    st.write("Aperçu des données :", df.head(3))

    st.markdown("---")
    
    # Le moteur du quiz simplifié
    if st.button("🎲 Tester une question"):
        q = df.sample().iloc[0]
        st.info(f"Question : {q['Question']}")
        if st.button("Voir la réponse"):
            st.success(f"Réponse : {q['Réponse']}")

except Exception as e:
    st.error("❌ Erreur de lecture")
    st.warning(f"Message d'erreur : {e}")
    st.write("Vérifie que ton lien dans le code est identique à celui de tes Notes.")
