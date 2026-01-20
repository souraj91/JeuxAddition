import streamlit as st
import random
import time

# Configuration de la page
st.set_page_config(page_title="Mission Addition", page_icon="🚀")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .big-font { font-size:50px !important; font-weight: bold; color: #FF4B4B; }
    .score-text { font-size:25px !important; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(1, 5)
    st.session_state.n2 = random.randint(1, 5)
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

def nouvelle_question():
    st.session_state.n1 = random.randint(1, 5) # Chiffres simples pour le CP
    st.session_state.n2 = random.randint(1, 5)

# --- INTERFACE PRINCIPALE ---
st.title("🚀 Mission : Champion des Additions")

# Barre de progression
progres = st.session_state.score / 10
st.progress(min(progres, 1.0))
st.write(f"Ton objectif : 10 points. Points actuels : **{st.session_state.score}**")

if st.session_state.score >= 10:
    st.balloons()
    st.success("🏆 FÉLICITATIONS ! Tu es un champion !")
    if st.button("Recommencer une partie"):
        st.session_state.score = 0
        nouvelle_question()
        st.rerun()
else:
    # Affichage de l'addition en gros
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.markdown(f"<p class='big-font'>{st.session_state.n1}</p>", unsafe_allow_html=True)
    with col2: st.markdown("<p class='big-font'>+</p>", unsafe_allow_html=True)
    with col3: st.markdown(f"<p class='big-font'>{st.session_state.n2}</p>", unsafe_allow_html=True)
    with col4: st.markdown("<p class='big-font'>=</p>", unsafe_allow_html=True)
    with col5: reponse = st.number_input("", min_value=0, max_value=20, step=1, key="rep", label_visibility="collapsed")

    # Aide visuelle (les petites étoiles pour compter)
    st.write("---")
    st.write("💡 Aide-toi des étoiles :")
    st.write(f"{'⭐ ' * st.session_state.n1}  |  {'🌟 ' * st.session_state.n2}")
    st.write("---")

    if st.button("VÉRIFIER MA RÉPONSE 🎯", use_container_width=True):
        if reponse == st.session_state.n1 + st.session_state.n2:
            st.session_state.score += 1
            st.snow() # Petit effet de fête
            st.toast("Super ! +1 point", icon="✅")
            nouvelle_question()
            time.sleep(1) # Laisser le temps de voir la neige
            st.rerun()
        else:
            st.error("Oups ! Réessaie encore, tu vas y arriver ! 🌈")

# --- MENU LATÉRAL ---
with st.sidebar:
    st.header("Paramètres")
    difficulte = st.selectbox("Niveau", ["Débutant (1-5)", "Expert (1-10)"])
    if st.button("Réinitialiser le jeu"):
        st.session_state.score = 0
        nouvelle_question()
        st.rerun()
