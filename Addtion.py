import streamlit as st
import random
import time

# Configuration de la page
st.set_page_config(page_title="Maths Aventure : Contre les Monstres !", page_icon="👹", layout="centered")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; font-size: 20px; background-color: #FF4B4B; color: white; margin-top: 10px; }
    .math-card { background-color: white; padding: 30px; border-radius: 15px; border: 5px solid #FF4B4B; text-align: center; font-size: 60px; font-weight: bold; margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.2); }
    .boss-hp-bar .stProgress > div > div { background-color: #e00 !important; } /* Rouge pour la vie du boss */
    .player-xp-bar .stProgress > div > div { background-color: #0c0 !important; } /* Vert pour l'XP du joueur */
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES VARIABLES DE SESSION ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'boss_hp' not in st.session_state:
    st.session_state.boss_hp = 50 # Le boss commence avec 50 HP
if 'current_boss_name' not in st.session_state:
    st.session_state.current_boss_name = "Le Gobelin Glouton"
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(1, 6)
    st.session_state.n2 = random.randint(1, 4)
if 'badges' not in st.session_state:
    st.session_state.badges = []

BOSS_NAMES = ["Le Gobelin Glouton", "Le Spectre Sanguinaire", "Le Dragon des Chiffres", "Le Kraken des Calculs"]
XP_PER_LEVEL = 20 # XP nécessaire pour monter de niveau
DAMAGE_PER_CORRECT_ANSWER = 10 # Dégâts infligés au boss par bonne réponse

def nouvelle_question():
    # Difficulté augmente avec le niveau du joueur
    max_num = 5 + (st.session_state.level * 2)
    st.session_state.n1 = random.randint(1, max_num)
    st.session_state.n2 = random.randint(1, max_num // 2 + 1) # Pour garder des additions gérables
    # S'assurer que les nombres ne sont pas trop petits si le niveau est élevé
    if st.session_state.n1 < 3 and max_num > 5: st.session_state.n1 = random.randint(3, max_num)
    if st.session_state.n2 < 2 and max_num > 5: st.session_state.n2 = random.randint(2, max_num // 2 + 1)


def next_boss():
    st.balloons()
    st.success(f"VICTOIRE ! Tu as battu {st.session_state.current_boss_name} !")
    st.session_state.xp += 50 # Bonus XP pour avoir battu un boss
    
    # Choisir un nouveau boss
    current_boss_index = BOSS_NAMES.index(st.session_state.current_boss_name)
    if current_boss_index + 1 < len(BOSS_NAMES):
        st.session_state.current_boss_name = BOSS_NAMES[current_boss_index + 1]
    else:
        st.session_state.current_boss_name = "Le Grand Maître des Mathématiques" # Dernier boss, ou on boucle
    
    st.session_state.boss_hp = 50 + (st.session_state.level * 10) # Plus de vie pour le nouveau boss
    nouvelle_question()
    st.rerun()

# --- SIDEBAR (PROFIL DU JOUEUR) ---
with st.sidebar:
    st.header("👤 Ton Aventure")
    
    # Niveau et XP du joueur
    st.subheader(f"Level : {st.session_state.level} ⭐")
    st.write(f"XP : **{st.session_state.xp}**")
    st.markdown(f"<div class='player-xp-bar'>", unsafe_allow_html=True)
    st.progress(min((st.session_state.xp % XP_PER_LEVEL) / XP_PER_LEVEL, 1.0))
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("Boss actuel :")
    st.warning(f"👹 {st.session_state.current_boss_name}")
    st.write(f"HP : **{st.session_state.boss_hp}**")
    st.markdown(f"<div class='boss-hp-bar'>", unsafe_allow_html=True)
    st.progress(max(0.0, st.session_state.boss_hp / (50 + (st.session_state.level * 10)))) # Affichage de la vie
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    if st.button("Recommencer l'aventure ♻️"):
        st.session_state.xp = 0
        st.session_state.level = 1
        st.session_state.boss_hp = 50
        st.session_state.current_boss_name = BOSS_NAMES[0]
        st.session_state.badges = []
        nouvelle_question()
        st.rerun()

# --- ZONE DE JEU PRINCIPALE ---
st.title("Maths Aventure : Affronte les Monstres ! ⚔️")

# Augmenter le niveau du joueur
old_level = st.session_state.level
st.session_state.level = (st.session_state.xp // XP_PER_LEVEL) + 1
if st.session_state.level > old_level:
    st.success(f"FÉLICITATIONS ! Tu as atteint le Niveau {st.session_state.level} ! 🎉")
    st.snow() # Petite animation de fête

# Affichage de l'énigme
st.markdown(f"""
    <div class='math-card'>
        {st.session_state.n1} + {st.session_state.n2} = ?
    </div>
    """, unsafe_allow_html=True)

# Aide visuelle par icônes
col_a, col_b = st.columns(2)
with col_a:
    st.write(f"Force 1 : {'⚡' * st.session_state.n1}")
with col_b:
    st.write(f"Force 2 : {'💥' * st.session_state.n2}")

# Entrée de la réponse
reponse = st.number_input("Ta réponse, jeune héros :", min_value=0, step=1, value=None, key="input_res")

if st.button("ATTAQUER LE MONSTRE ! 🗡️"):
    if reponse == st.session_state.n1 + st.session_state.n2:
        # Réponse correcte
        st.session_state.xp += 5 # XP pour la réponse
        st.session_state.boss_hp -= DAMAGE_PER_CORRECT_ANSWER # Le boss prend des dégâts
        st.toast(f"Boom ! {DAMAGE_PER_CORRECT_ANSWER} dégâts au monstre !", icon="💥")
        
        # Vérifier si le boss est battu
        if st.session_state.boss_hp <= 0:
            next_boss() # Passer au boss suivant
        else:
            nouvelle_question() # Nouvelle addition
            st.rerun() # Rafraîchir l'interface
    else:
        # Mauvaise réponse
        st.error(f"Zut ! Ton attaque a raté. Le monstre te regarde de travers ! 😈 (La bonne réponse était {st.session_state.n1 + st.session_state.n2})")
        st.session_state.xp = max(0, st.session_state.xp - 2) # Petite pénalité XP
        nouvelle_question()
        time.sleep(1) # Laisser le temps de lire le message
        st.rerun()

# --- Message d'encouragement ---
if st.session_state.xp < 10 and st.session_state.boss_hp > 40:
    st.info("Concentration ! Chaque bonne réponse affaiblit le monstre !")
