import streamlit as st
import random
import requests
from streamlit_lottie import st_lottie

# 1. INITIALISATION (À mettre tout en haut)
# On vérifie si 'boss_hp' existe. Si non, on crée tout le nécessaire.
if 'boss_hp' not in st.session_state:
    st.session_state.boss_hp = 50
    st.session_state.xp = 0
    st.session_state.n1 = random.randint(1, 10)
    st.session_state.n2 = random.randint(1, 5)
