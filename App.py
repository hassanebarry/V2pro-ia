import streamlit as st
import pandas as pd
from scipy.stats import poisson

# CONFIGURATION
API_KEY = "5a92166c4b4be20cef1187536c1fa610a27fbf1d985db4b8db5a1a89e43e3d10"

st.set_page_config(page_title="V2PRO PLUS IA v4.0", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00ff41;'>🟢 V2PRO PLUS IA v4.0</h1>", unsafe_allow_index=True)
st.write("---")

col1, col2 = st.columns(2)
with col1:
    home_team = st.text_input("🏠 ÉQUIPE DOMICILE", "Sénégal")
with col2:
    away_team = st.text_input("✈️ ÉQUIPE EXTÉRIEURE", "Botswana")

def calculer_prono(h_name, a_name):
    # Stats automatiques pour le test
    h_force = 2.4 if "City" in h_name or "Sénégal" in h_name else 1.2
    a_force = 0.8 if "Forest" in a_name or "Botswana" in a_name else 1.1
    
    prob_h = poisson.pmf(range(5), h_force)
    prob_a = poisson.pmf(range(5), a_force)
    
    score_h = pd.Series(prob_h).idxmax()
    score_a = pd.Series(prob_a).idxmax()
    conf = (max(prob_h) * max(prob_a)) * 100
    return score_h, score_a, conf

if st.button("🚀 START ANALYSE IA"):
    res_h, res_a, confiance = calculer_prono(home_team, away_team)
    st.markdown(f"<div style='border: 2px solid #00ff41; padding: 20px; border-radius: 10px; text-align: center; background-color: #0e1117;'><h2 style='color: #00ff41;'>SCORE PRÉDIT : {res_h} - {res_a}</h2><p style='color: white;'>CONFIANCE IA : {confiance:.1f}%</p></div>", unsafe_allow_index=True)
