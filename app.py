import streamlit as st
import json
import os
from datetime import datetime, date

# --- CONFIGURAZIONE PAGINA BYPASS ---
st.set_page_config(
    page_title="BYPASS.EXE",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STILI CSS NEON / STREET ---
st.markdown("""
<style>
    .stApp {
        background-color: #08090a;
        color: #c5c6c7;
    }
    h1, h2, h3 {
        color: #ff0055 !important; /* Rosa Neon */
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #ff0055;
    }
    .stDateInput div div input {
        background-color: #121212 !important;
        color: #66fcf1 !important;
    }
    div.stButton > button {
        background-color: #121212;
        color: #66fcf1;
        border: 2px solid #66fcf1;
        border-radius: 4px;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #66fcf1;
        color: #08090a;
        box-shadow: 0 0 10px #66fcf1;
    }
</style>
""", unsafe_allow_html=True)

DB_FILE = "bypass_db.json"

# --- DATABASE LOGIC ---
def load_data():
    if not os.path.exists(DB_FILE):
        return {
            "stats": {
                "fisico": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "mente": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "skill": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "rep": {"xp": 0, "level": 1}
            },
            "tasks": []
        }
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def aggiungi_xp(stat, quantita):
    data["stats"][stat]["xp"] += quantita
    data["stats"][stat]["last_active"] = str(date.today())
    xp_necessari = 100 * data["stats"][stat]["level"]
    if data["stats"][stat]["xp"] >= xp_necessari:
        data["stats"][stat]["level"] += 1
        data["stats"][stat]["xp"] -= xp_necessari
        st.success(f"⚡ SKILL UP: {stat.upper()} sale al Livello {data['stats'][stat]['level']}!")
    save_data(data)

# --- HEADER BYPASS ---
st.title("⚡ BYPASS")
st.write("`SOVRASCRIVI LA ROUTINE. PRENDI IL CONTROLLO.`")
st.write("---")

# --- 1. AGGIUNGI MISSIONE ---
with st.expander("➕ APRI TERMINALE: AGGIUNGI MISSIONE", expanded=False):
    with st.form("new_mission_form", clear_on_submit=True):
        titolo = st.text_input("Nome della Missione (es. Pagare multa, Allenamento gambe)")
        tipo = st.selectbox("Tipologia", ["Scadenza URGENTE", "I Grossi (Priorità)", "Lavoretti (Secondari)"])
        stat = st.selectbox("Statistica che potenzia", ["fisico", "mente", "skill"])
        
        # Mostra selezione data solo se è una Scadenza URGENTE
        scadenza = None
        if tipo == "Scadenza URGENTE":
            scadenza = st.date_input("Scade il:", min_value=date.today())
            
        submit = st.form_submit_button("REGISTRA NEI SISTEMI")
        
        if submit and titolo:
            nuova_missione = {
                "id": len(data["tasks"]) + 1,
                "titolo": titolo,
                "tipo": tipo,
                "stat": stat,
                "scadenza": str(scadenza) if scadenza else None,
                "completata": False
            }
            data["tasks"].append(nuova_missione)
            save_data(data)
            st.success(f"Missione '{titolo}' caricata!")
            st.rerun()

# --- 2. LISTA DELLE MISSIONI ORDINATE ---
st.write("### 📋 LE TUE MISSIONI ATTIVE")

attive = [t for t in data["tasks"] if not t["completato"]]

if not attive:
    st.info("Nessuna missione attiva al momento. Sei libero o è il momento di pianificare?")
else:
    # Ordiniamo le missioni:
    # 1. Prima le Scadenze Urgenti (ordinate per data di scadenza più vicina)
    # 2. Poi I Grossi (Priorità)
    # 3. Infine i Lavoretti
    
    scadenze = [t for t in attive if t["tipo"] == "Scadenza URGENTE"]
    # Ordina le scadenze per data
    scadenze.sort(key=lambda x: x["scadenza"] if x["scadenza"] else "9999-12-31")
    
    grossi = [t for t in attive if t["tipo"] == "I Grossi (Priorità)"]
    lavoretti = [t for t in attive if t["tipo"] == "Lavoretti (Secondari)"]
    
    lista_ordinata = scadenze + grossi + lavoretti

    for task in lista_ordinata:
        # Crea un'etichetta visiva per la priorità/scadenza
        if task["tipo"] == "Scadenza URGENTE":
            scad_date = datetime.strptime(task["scadenza"], "%Y-%m-%d").date()
            giorni_rimasti = (scad_date - date.today()).days
            if giorni_rimasti <= 1:
                label = f"⚠️ [SCADE DOMANI/OGGI] - {task['titolo']}"
            else:
                label = f"⏳ [SCADE TRA {giorni_rimasti} GG] - {task['titolo']}"
            xp_reward = 40
        elif task["tipo"] == "I Grossi (Priorità)":
            label = f"🔴 [PRIORITÀ] - {task['titolo']}"
            xp_reward = 30
        else:
            label = f"⚪ [LAVORETTO] - {task['titolo']}"
            xp_reward = 15
            
        # Checkbox per completare la missione
        if st.checkbox(label, key=f"task_{task['id']}"):
            # Segna come completata
            for t in data["tasks"]:
                if t["id"] == task["id"]:
                    t["completato"] = True
            save_data(data)
            # Aggiungi XP
            aggiungi_xp(task["stat"], xp_reward)
            st.toast(f"Missione Completata! +{xp_reward} XP in {task['stat'].upper()}", icon="⚡")
            st.rerun()

