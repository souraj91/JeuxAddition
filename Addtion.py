import streamlit as st
import requests
from streamlit_lottie import st_lottie
import random

# --- FONCTION DE CHARGEMENT SÉCURISÉE ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Utilisation de nouvelles URLs testées
# Monstre : https://lottie.host/804043b2-608d-4952-9441-267954930114/A60L51A6nS.json
# Explosion : https://lottie.host/846a48f3-80f4-4113-91b3-469614457493/S9v19T2v3f.json

lottie_monster = load_lottieurl("https://lottie.host/804043b2-608d-4952-9441-267954930114/A60L51A6nS.json")
lottie_success = load_lottieurl("https://lottie.host/846a48f3-80f4-4113-91b3-469614457493/S9v19T2v3f.json")

# --- DANS TA ZONE D'AFFICHAGE ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.boss_hp > 0:
        if lottie_monster:
            st_lottie(lottie_monster, speed=1, height=250, key="monster")
        else:
            st.title("👾") # Emoji de secours si l'anim ne charge pas
    else:
        if lottie_success:
            st_lottie(lottie_success, speed=1, height=250, key="win")
        else:
            st.balloons()
