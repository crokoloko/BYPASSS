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
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        # Se il file è corrotto o vuoto, ricomincia da zero
        return {
            "stats": {
                "fisico": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "mente": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "skill": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "rep": {"xp": 0, "level": 1}
            },
            "tasks": []
        }

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def aggiungi_xp(stat, quantita):
    # Usiamo .get per evitare crash se la stat non esiste nel vecchio db
    if stat not in data["stats"]:
        data["stats"][stat] = {"xp": 0, "level": 1, "last_active": str(date.today())}
    
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
        
        scadenza = None
        if tipo == "Scadenza URGENTE":
            scadenza = st.date_input("Scade il:", min_value=date.today())
            
        submit = st.form_submit_button("REGISTRA NEI SISTEMI")
        
        if submit and titolo:
            nuova_missione = {
                "id": len(data.get("tasks", [])),
                "titolo": titolo,
                "tipo": tipo,
                "stat": stat,
                "scadenza": str(scadenza) if scadenza else None,
                "completata": False
            }
            if "tasks" not in data:
                data["tasks"] = []
            data["tasks"].append(nuova_missione)
            save_data(data)
            st.success(f"Missione '{titolo}' caricata!")
            st.rerun()

# --- 2. LISTA DELLE MISSIONI ORDINATE ---
st.write("### 📋 LE TUE MISSIONI ATTIVE")

all_tasks = data.get("tasks", [])
attive = [t for t in all_tasks if not t.get("completato", False)]

if not attive:
    st.info("Nessuna missione attiva al momento. Sei libero o è il momento di pianificare?")
else:
    # Filtriamo in modo sicuro usando .get() per evitare KeyError
    scadenze = [t for t in attive if t.get("tipo") == "Scadenza URGENTE"]
    scadenze.sort(key=lambda x: x.get("scadenza") if x.get("scadenza") else "9999-12-31")
    
    grossi = [t for t in attive if t.get("tipo") == "I Grossi (Priorità)"]
    lavoretti = [t for t in attive if t.get("tipo") == "Lavoretti (Secondari)"]
    
    lista_ordinata = scadenze + grossi + lavoretti

    for task in lista_ordinata:
        t_tipo = task.get("tipo", "Lavoretti (Secondari)")
        t_titolo = task.get("titolo", "Missione Senza Nome")
        t_scadenza = task.get("scadenza")
        t_id = task.get("id", 0)
        t_stat = task.get("stat", "mente")
        
        if t_tipo == "Scadenza URGENTE" and t_scadenza:
            try:
                scad_date = datetime.strptime(t_scadenza, "%Y-%m-%d").date()
                giorni_rimasti = (scad_date - date.today()).days
                if giorni_rimasti <= 1:
                    label = f"⚠️ [SCADE DOMANI/OGGI] - {t_titolo}"
                else:
                    label = f"⏳ [SCADE TRA {giorni_rimasti} GG] - {t_titolo}"
            except Exception:
                label = f"⏳ [SCADENZA] - {t_titolo}"
            xp_reward = 40
        elif t_tipo == "I Grossi (Priorità)":
            label = f"🔴 [PRIORITÀ] - {t_titolo}"
            xp_reward = 30
        else:
            label = f"⚪ [LAVORETTO] - {t_titolo}"
            xp_reward = 15
            
        if st.checkbox(label, key=f"task_{t_id}"):
            for t in data["tasks"]:
                if t.get("id") == t_id:
                    t["completato"] = True
            save_data(data)
            aggiungi_xp(t_stat, xp_reward)
            st.toast(f"Missione Completata! +{xp_reward} XP", icon="⚡")
            st.rerun()
