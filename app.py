import streamlit as st
import json
import os
import requests
from datetime import datetime, date

# --- CONFIGURAZIONE PAGINA BYPASS ---
st.set_page_config(
    page_title="BYPASS.EXE",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CREDENZIALI CLOUD DATABASE (JSONBin.io) ---
BIN_ID = "6a6062a5f5f4af5e29af85cd"
API_KEY = "$2a$10$HG2ozmdWbzNBc5DhTzel5.aNV0Z3UckB1adx8MbSDki6hUZxRFnIi"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

# --- STILE CSS FLUIDO & MORBIDO (SMOOTH NEON STREET) ---
# (QUI LASCIA ESATTAMENTE TUTTO IL BLOCCO st.markdown CHE HAI GIA')

# --- DATABASE LOGIC SUL CLOUD ---
def load_data():
    default_data = {
        "stats": {
            "disciplina": {"xp": 0, "level": 1, "last_active": str(date.today())},
            "focus": {"xp": 0, "level": 1, "last_active": str(date.today())},
            "skill": {"xp": 0, "level": 1, "last_active": str(date.today())},
            "rep": {"xp": 0, "level": 1}
        },
        "mission_stats": {"totale": 0, "urgenti": 0, "grossi": 0, "lavoretti": 0},
        "tasks": [],
        "garage": [],
        "bar_streak": 0,
        "last_bar_check": str(date.today())
    }
    
    try:
        req = requests.get(URL, headers=HEADERS)
        if req.status_code == 200:
            db = req.json()["record"]
            if "garage" not in db: db["garage"] = []
            if "bar_streak" not in db: db["bar_streak"] = 0
            if "last_bar_check" not in db: db["last_bar_check"] = str(date.today())
            if "mission_stats" not in db: db["mission_stats"] = {"totale": 0, "urgenti": 0, "grossi": 0, "lavoretti": 0}
            if "stats" not in db: db["stats"] = default_data["stats"]
            return db
        else:
            return default_data
    except Exception:
        return default_data

def save_data(data):
    try:
        requests.put(URL, json=data, headers=HEADERS)
    except Exception as e:
        pass

data = load_data()

# --- DA QUI IN POI LASCIA TUTTO INTATTO (applica_decadimento, ecc.) ---
