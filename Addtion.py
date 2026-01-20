import streamlit as st
import random

st.set_page_config(page_title="Mon Super Jeu d'Additions", page_icon="🧮")

st.title("🔢 Apprends à additionner !")

# Initialisation du score et des nombres dans la "session_state"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(1, 10)
    st.session_state.n2 = random.randint(1, 10)

# Affichage de l'exercice
st.header(f"Combien font {st.session_state.n1} + {st.session_state.n2} ?")

# Zone de réponse
reponse = st.number_input("Ta réponse :", min_value=0, step=1, value=None, placeholder="Écris le nombre ici...")

if st.button("Vérifier ✅"):
    if reponse == st.session_state.n1 + st.session_state.n2:
        st.success("Bravo ! C'est la bonne réponse ! 🎉")
        st.session_state.score += 1
        # On change les nombres pour la prochaine question
        st.session_state.n1 = random.randint(1, 10)
        st.session_state.n2 = random.randint(1, 10)
        st.rerun()
    else:
        st.error("Essaie encore, tu peux y arriver ! 💪")

st.sidebar.metric("Ton Score", st.session_state.score)
