import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv
from scipy.stats import poisson
from datetime import date

# ================= CONFIG =================
st.set_page_config(page_title="BOT PRO FOOTBALL", layout="centered")
st.title("⚽ BOT PRO – ANALYSE AVANT MATCH (RÉEL)")

# ================= API ====================
load_dotenv()
API_TOKEN = os.getenv("ZzMVJCWYvSS9xnMuyUh5eoPrYu8Xf1ewIYm0H36Uqls0HTJmaFK4kDdxI3Nj")

if not API_TOKEN:
    st.error("❌ Clé API introuvable. Vérifie le fichier .env")
    st.stop()

BASE_URL = "https://api.sportmonks.com/v3/football"

# ================= DATA ===================
def get_fixtures(match_date):
    url = f"{BASE_URL}/fixtures/date/{match_date}"
    params = {
        "api_token": API_TOKEN,
        "include": "participants"
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return []
    return r.json().get("data", [])

# ================= ANALYSE =================
def predict_score(avg_home, avg_away):
    home_goals = round(poisson.mean(avg_home))
    away_goals = round(poisson.mean(avg_away))
    return home_goals, away_goals

def confidence(avg_home, avg_away):
    diff = abs(avg_home - avg_away)
    return min(75, int(50 + diff * 12))

# ================= UI ======================
selected_date = st.date_input("📅 Date d’analyse", date.today())

if st.button("🔍 LANCER ANALYSE"):
    st.info("⏳ Analyse en cours… récupération des données")
    time.sleep(2)

    matches = get_fixtures(selected_date)

    if not matches:
        st.error("Aucun match trouvé ou problème API")
        st.stop()

    for m in matches:
        teams = m.get("participants", [])
        if len(teams) < 2:
            continue

        home = teams[0]["name"]
        away = teams[1]["name"]

        # Moyennes par défaut (améliorables)
        avg_home = 1.5
        avg_away = 1.2

        score_home, score_away = predict_score(avg_home, avg_away)
        conf = confidence(avg_home, avg_away)

        st.subheader(f"{home} vs {away}")
        st.write(f"🔮 Score probable : **{score_home} – {score_away}**")
        st.write("📈 BTTS :", "OUI" if score_home > 0 and score_away > 0 else "NON")
        st.write("⚖️ Over 1.5 :", "OUI" if score_home + score_away >= 2 else "NON")
        st.write(f"✅ Confiance : **{conf}%**")
        st.divider()
