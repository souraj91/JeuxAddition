import streamlit as st
import random
import time
import requests
from streamlit_lottie import st_lottie

# Configuration style "Jeux Vidéo"
st.set_page_config(page_title="Maths Monster Hunter", layout="centered")

# --- CHARGEMENT DES ANIMATIONS (Lottie) ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# On charge un monstre rigolo et une explosion
lottie_monster = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_T69m9N.json") # Un monstre qui flotte
lottie_success = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_pqnfmone.json") # Explosion de confettis

# --- STYLE CSS POUR L'ASPECT CARTOON ---
st.markdown("""
    <style>
    .math-bubble {
        background-color: #FF4B4B;
        color: white;
        padding: 20px;
        border-radius: 50px;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        border: 8px solid #FFD700;
        margin: 20px 0;
    }
    .hp-text { font-size: 20px; font-weight: bold; color: #E74C3C; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'boss_hp' not in st.session_state:
    st.session_state.boss_hp = 50
    st.session_state.n1 = random.randint(1, 10)
    st.session_state.n2 = random.randint(1, 5)
    st.session_state.shake = False

# --- INTERFACE ---
st.title("👾 Gobelin Glouton Challenge")

# Affichage du Monstre Animé
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.boss_hp > 0:
        # L'animation du monstre
        st_lottie(lottie_monster, speed=1, height=250, key="monster")
    else:
        st_lottie(lottie_success, speed=1, height=250, key="win")
        st.balloons()
        st.success("TU AS GAGNÉ !")
        if st.button("Rejouer ?"):
            st.session_state.boss_hp = 50
            st.rerun()

# Barre de vie du Boss animée
st.markdown(f"<p class='hp-text'>POINTS DE VIE DU MONSTRE : {st.session_state.boss_hp}/50</p>", unsafe_allow_html=True)
st.progress(max(0, st.session_state.boss_hp / 50))

# Bulle de calcul Cartoon
st.markdown(f"<div class='math-bubble'>{st.session_state.n1} + {st.session_state.n2} = ?</div>", unsafe_allow_html=True)

# Entrée joueur
reponse = st.number_input("Ta réponse :", min_value=0, step=1, value=None, key="ans")

if st.button("ATTAQUER ! ⚔️"):
    if reponse == st.session_state.n1 + st.session_state.n2:
        st.session_state.boss_hp -= 10
        st.toast("BAM ! -10 dégâts !", icon="💥")
        # Nouvelles valeurs
        st.session_state.n1 = random.randint(1, 10)
        st.session_state.n2 = random.randint(1, 10)
        time.sleep(0.5)
        st.rerun()
    else:
        st.error("Raté ! Le monstre rigole... 👅")
        # On peut ajouter un petit tremblement de terre visuel ici
