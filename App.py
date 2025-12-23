import streamlit as st
import pandas as pd
from scipy.stats import poisson

# CONFIGURATION
API_KEY = "5a92166c4b4be20cef1187536c1fa610a27fbf1d985db4b8db5a1a89e43e3d10"

st.set_page_config(page_title="V2PRO PLUS IA v4.0", layout="centered")

# Correction de l'erreur TypeError
st.title("🟢 V2PRO PLUS IA v4.0")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    home_team = st.text_input("🏠 ÉQUIPE DOMICILE", "Manchester City")
with col2:
    away_team = st.text_input("✈️ ÉQUIPE EXTÉRIEURE", "Nottingham Forest")

def calculer_prono(h_name, a_name):
    # Logique IA simplifiée
    h_force = 2.8 if "City" in h_name else 1.2
    a_force = 0.9 if "Forest" in a_name else 1.1
    prob_h = poisson.pmf(range(5), h_force)
    prob_a = poisson.pmf(range(5), a_force)
    score_h = pd.Series(prob_h).idxmax()
    score_a = pd.Series(prob_a).idxmax()
    conf = (max(prob_h) * max(prob_a)) * 100
    return score_h, score_a, conf

if st.button("🚀 START ANALYSE IA"):
    res_h, res_a, confiance = calculer_prono(home_team, away_team)
    st.success(f"SCORE PRÉDIT : {res_h} - {res_a}")
    st.info(f"CONFIANCE : {confiance:.1f}%")
