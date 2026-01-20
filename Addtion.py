import streamlit as st
import random
import time
import pandas as pd

# Configuration
st.set_page_config(page_title="Maths Cup CP", page_icon="🏆")

# --- INITIALISATION ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
    st.session_state.boss_hp = 50
    st.session_state.start_time = time.time() # Début du chrono
    st.session_state.leaderboard = [] # Liste des records
    st.session_state.game_finished = False

# --- LOGIQUE DU CHRONO ---
def get_time():
    return round(time.time() - st.session_state.start_time, 1)

# --- STYLE CSS ---
st.markdown("""
    <style>
    .chrono { font-size: 30px; font-weight: bold; color: #FF4B4B; text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 10px; }
    .math-card { font-size: 70px; text-align: center; padding: 20px; background: white; border-radius: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ET CHRONO ---
st.title("🏆 Le Défi des Champions")
col_stats1, col_stats2 = st.columns(2)

with col_stats1:
    st.metric("Points d'Expérience", f"{st.session_state.xp} XP")
with col_stats2:
    if not st.session_state.game_finished:
        st.markdown(f"<div class='chrono'>⏱️ {get_time()}s</div>", unsafe_allow_html=True)

# --- ZONE DU BOSS ---
st.write(f"### 👹 Boss : Le Dragon du Temps")
st.progress(max(0.0, st.session_state.boss_hp / 50))
st.write(f"Vie du Boss : {st.session_state.boss_hp} / 50")

# --- L'ADDITION ---
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(1, 10)
    st.session_state.n2 = random.randint(1, 5)

st.markdown(f"<div class='math-card'>{st.session_state.n1} + {st.session_state.n2}</div>", unsafe_allow_html=True)

# --- RÉPONSE ---
nom_eleve = st.sidebar.text_input("Ton prénom :", "Anonyme")
reponse = st.number_input("Ta réponse :", min_value=0, step=1, value=None)

if st.button("ATTAQUER ! ⚡"):
    if reponse == st.session_state.n1 + st.session_state.n2:
        st.session_state.boss_hp -= 10
        st.session_state.xp += 10
        st.session_state.n1 = random.randint(1, 10)
        st.session_state.n2 = random.randint(1, 5)
        
        if st.session_state.boss_hp <= 0:
            temps_final = get_time()
            st.balloons()
            st.session_state.game_finished = True
            # Ajouter au tableau des scores
            st.session_state.leaderboard.append({"Élève": nom_eleve, "Temps (s)": temps_final})
            st.success(f"VICTOIRE ! Tu as battu le boss en {temps_final} secondes !")
        else:
            st.toast("Touche réussie ! -10 HP", icon="💥")
            st.rerun()
    else:
        st.error("Oups ! Réessaie vite, le chrono tourne !")

# --- TABLEAU DES SCORES (LEADERBOARD) ---
st.write("---")
st.subheader("📊 Tableau des Champions")
if st.session_state.leaderboard:
    # On trie pour avoir les temps les plus courts en premier
    df = pd.DataFrame(st.session_state.leaderboard).sort_values(by="Temps (s)")
    st.table(df)
else:
    st.info("Aucun record pour le moment. Sois le premier !")

# Bouton Reset
if st.sidebar.button("Nouveau Match 🔄"):
    st.session_state.boss_hp = 50
    st.session_state.start_time = time.time()
    st.session_state.game_finished = False
    st.rerun()
