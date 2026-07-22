import streamlit as st
import json
import os
import requests
from datetime import datetime, date

st.set_page_config(
    page_title="BYPASS",
    layout="centered",
    initial_sidebar_state="expanded"
)

BIN_ID = "6a6062a5f5f4af5e29af85cd"
API_KEY = "$2a$10$HG2ozmdWbzNBc5DhTzel5.aNV0Z3UckB1adx8MbSDki6hUZxRFnIi"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #212121 !important;
        color: #E0E0E0 !important;
    }
    
    .stApp {
        background-color: #212121 !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #212121 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.02) !important;
        box-shadow: 10px 0px 30px #151515;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    h4 {
        color: #B32428 !important; /* Accento Rosso Carminio */
        text-transform: uppercase;
        font-size: 0.9rem !important;
        letter-spacing: 2px;
    }

    /* Form e Card Neumorfiche */
    div[data-testid="stForm"], .neumorphic-card {
        background-color: #212121 !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        box-shadow: 8px 8px 16px #151515, -8px -8px 16px #2d2d2d !important;
        padding: 24px;
        margin-bottom: 24px;
    }

    /* Pulsanti - Effetto Sollevato */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #212121 !important;
        color: #B32428 !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        box-shadow: 6px 6px 12px #151515, -6px -6px 12px #2d2d2d !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.2s ease-in-out;
    }
    
    /* Pulsanti - Hover Effetto Premuto/Scavato */
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        color: #FFFFFF !important;
        background-color: #B32428 !important;
        border-color: #B32428 !important;
        box-shadow: inset 4px 4px 8px rgba(0, 0, 0, 0.2), inset -4px -4px 8px rgba(255, 255, 255, 0.1) !important;
    }
    
    div.stButton > button:active {
        box-shadow: inset 6px 6px 12px #151515, inset -6px -6px 12px #2d2d2d !important;
        color: #888888 !important;
    }
    
    /* Pulsante Add Minimal */
    .btn-minimal > div > button {
        padding: 0.4rem 1rem !important;
        font-size: 0.9rem !important;
        border-radius: 12px !important;
    }

    /* Metriche (Cruscotto) */
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #888888 !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="metric-container"] {
        background-color: #212121;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        box-shadow: inset 4px 4px 8px #151515, inset -4px -4px 8px #2d2d2d;
        padding: 16px;
        text-align: center;
    }

    /* Campi di Input - Effetto Scavato */
    .stTextInput input, .stSelectbox div div, .stNumberInput input {
        background-color: #212121 !important;
        color: #E0E0E0 !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.02) !important;
        box-shadow: inset 6px 6px 12px #151515, inset -6px -6px 12px #2d2d2d !important;
        padding: 12px 16px !important;
        font-weight: 500;
    }
    
    .stTextInput input:focus {
        border-color: #B32428 !important;
        box-shadow: inset 6px 6px 12px #151515, inset -6px -6px 12px #2d2d2d, 0 0 10px rgba(179, 36, 40, 0.2) !important;
    }

    /* Barre di Progresso */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #B32428 !important;
        border-radius: 10px;
    }

    /* Badge Trofei - Sbloccati */
    .badge-unlocked {
        padding: 18px 24px;
        background-color: #212121;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-left: 6px solid #B32428;
        box-shadow: 8px 8px 16px #151515, -8px -8px 16px #2d2d2d;
        margin-bottom: 16px;
    }
    /* Badge Trofei - Bloccati (Scavati) */
    .badge-locked {
        padding: 18px 24px;
        background-color: #212121;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.02);
        box-shadow: inset 6px 6px 12px #151515, inset -6px -6px 12px #2d2d2d;
        margin-bottom: 16px;
        opacity: 0.5;
    }
    
    /* Checkbox */
    .stCheckbox > label {
        padding: 8px 0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

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

def applica_decadimento(data):
    today = date.today()
    regole = {
        "disciplina": {"giorni": 3, "tasso": 0.05},
        "focus": {"giorni": 4, "tasso": 0.04},
        "skill": {"giorni": 5, "tasso": 0.03}
    }
    modificato = False
    for stat_name, regola in regole.items():
        if stat_name not in data["stats"]: continue
        last_active_str = data["stats"][stat_name].get("last_active", str(today))
        try:
            last_active_date = datetime.strptime(last_active_str, "%Y-%m-%d").date()
            days_passed = (today - last_active_date).days
            if days_passed > regola["giorni"]:
                giorni_penalita = days_passed - regola["giorni"]
                perdita = int(data["stats"][stat_name]["xp"] * (regola["tasso"] * giorni_penalita))
                if perdita > 0:
                    data["stats"][stat_name]["xp"] = max(0, data["stats"][stat_name]["xp"] - perdita)
                    data["stats"][stat_name]["last_active"] = str(today)
                    modificato = True
        except Exception:
            data["stats"][stat_name]["last_active"] = str(today)
            modificato = True
            
    if modificato:
        save_data(data)

applica_decadimento(data)

def aggiungi_xp(stat, quantita):
    if stat == "fisico": stat = "disciplina"
    if stat == "mente": stat = "focus"
    
    if stat not in data["stats"]:
        data["stats"][stat] = {"xp": 0, "level": 1, "last_active": str(date.today())}
    
    data["stats"][stat]["xp"] += quantita
    data["stats"][stat]["last_active"] = str(date.today())
    
    xp_necessari = 100 * data["stats"][stat]["level"]
    if data["stats"][stat]["xp"] >= xp_necessari:
        data["stats"][stat]["level"] += 1
        data["stats"][stat]["xp"] -= xp_necessari
        st.toast(f"Level UP: {stat.upper()} sale al Livello {data['stats'][stat]['level']}")
        
    livelli = [
        data["stats"].get("disciplina", {}).get("level", 1),
        data["stats"].get("focus", {}).get("level", 1),
        data["stats"].get("skill", {}).get("level", 1)
    ]
    media_livelli = sum(livelli) // 3
    data["stats"]["rep"]["level"] = max(1, media_livelli)
    
    save_data(data)

if "show_mission_form" not in st.session_state:
    st.session_state.show_mission_form = False

st.sidebar.title("BYPASS")
st.sidebar.caption("SISTEMA DI CONTROLLO OPERATIVO")
st.sidebar.write("---")

scelta_menu = st.sidebar.radio(
    "Navigazione",
    ["BACHECA MISSIONI", "PROFILO & STATS", "GARAGE & RISPARMI"],
    label_visibility="collapsed"
)

st.sidebar.write("---")
st.sidebar.markdown(f"### REP GLOBALE: Livello {data['stats']['rep']['level']}")
st.sidebar.progress(min(1.0, (data['stats']['rep'].get('xp', 0)) / (100 * max(1, data['stats']['rep']['level']))))

if scelta_menu == "BACHECA MISSIONI":
    
    col_title, col_btn = st.columns([8, 2])
    with col_title:
        st.title("BYPASS")
        st.markdown("#### RADAR OPERATIVO")
    with col_btn:
        st.write("")
        st.write("")
        st.markdown('<div class="btn-minimal">', unsafe_allow_html=True)
        if st.button("ADD TASK", use_container_width=True):
            st.session_state.show_mission_form = not st.session_state.show_mission_form
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("---")

    if st.session_state.show_mission_form:
        with st.form("new_mission_form", clear_on_submit=True):
            titolo = st.text_input("Descrizione Task")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                tipo = st.selectbox("Urgenza / Carico", [
                    "Scadenza URGENTE (+40 XP)", 
                    "Progetto / Priorità (+30 XP)", 
                    "Routine / Manutenzione (+15 XP)"
                ])
            with col_f2:
                stat = st.selectbox("Area di afferenza", [
                    "disciplina (Scadenze / Burocrazia)", 
                    "focus (Lavoro / Progetti)", 
                    "skill (Fai-da-te / Casa)"
                ])
                stat_clean = stat.split(" ")[0]
            
            scadenza = None
            if "URGENTE" in tipo:
                scadenza = st.date_input("Scadenza inderogabile:", min_value=date.today())
                
            submit = st.form_submit_button("INSERISCI A SISTEMA")
            
            if submit and titolo:
                nuova_missione = {
                    "id": len(data.get("tasks", [])) + 1,
                    "titolo": titolo,
                    "tipo": tipo,
                    "stat": stat_clean,
                    "scadenza": str(scadenza) if scadenza else None,
                    "completato": False
                }
                data["tasks"].append(nuova_missione)
                save_data(data)
                st.session_state.show_mission_form = False
                st.toast(f"Task registrato: {titolo}")
                st.rerun()

    all_tasks = data.get("tasks", [])
    attive = [t for t in all_tasks if not t.get("completato", False)]

    if not attive:
        st.info("Nessun task in sospeso. Sistema allineato.")
    else:
        scadenze = [t for t in attive if "URGENTE" in t.get("tipo", "")]
        scadenze.sort(key=lambda x: x.get("scadenza") if x.get("scadenza") else "9999-12-31")
        grossi = [t for t in attive if "Priorità" in t.get("tipo", "")]
        lavoretti = [t for t in attive if "Routine" in t.get("tipo", "")]
        lista_ordinata = scadenze + grossi + lavoretti

        for task in lista_ordinata:
            t_tipo = task.get("tipo", "Routine / Manutenzione (+15 XP)")
            t_titolo = task.get("titolo", "Task")
            t_scadenza = task.get("scadenza")
            t_id = task.get("id", 0)
            t_stat = task.get("stat", "disciplina")
            
            if "URGENTE" in t_tipo and t_scadenza:
                try:
                    scad_date = datetime.strptime(t_scadenza, "%Y-%m-%d").date()
                    giorni_rimasti = (scad_date - date.today()).days
                    if giorni_rimasti <= 0:
                        label = f"[SCADUTA] — {t_titolo}"
                    elif giorni_rimasti == 1:
                        label = f"[SCADE DOMANI] — {t_titolo}"
                    else:
                        label = f"[{giorni_rimasti} GG RIMASTI] — {t_titolo}"
                except:
                    label = f"[URGENTE] — {t_titolo}"
                xp_reward = 40
                categoria_stat = "urgenti"
            elif "Priorità" in t_tipo:
                label = f"[PRIORITÀ] — {t_titolo}"
                xp_reward = 30
                categoria_stat = "grossi"
            else:
                label = f"[ROUTINE] — {t_titolo}"
                xp_reward = 15
                categoria_stat = "lavoretti"
                
            if st.checkbox(label, key=f"task_{t_id}"):
                for t in data["tasks"]:
                    if t.get("id") == t_id:
                        t["completato"] = True
                
                data["mission_stats"]["totale"] = data["mission_stats"].get("totale", 0) + 1
                data["mission_stats"][categoria_stat] = data["mission_stats"].get(categoria_stat, 0) + 1
                
                save_data(data)
                aggiungi_xp(t_stat, xp_reward)
                st.toast(f"Task completato (+{xp_reward} XP in {t_stat.upper()})")
                st.rerun()

elif scelta_menu == "PROFILO & STATS":
    st.title("STATO OPERATIVO")
    st.markdown(f"#### LIVELLO REP: {data['stats']['rep']['level']}")
    st.write("---")
    
    st.markdown("### CRUSCOTTO ANALITICO")
    m_stats = data.get("mission_stats", {"totale": 0, "urgenti": 0, "grossi": 0, "lavoretti": 0})
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Task Totali", m_stats.get("totale", 0))
    col_m2.metric("Scadenze", m_stats.get("urgenti", 0))
    col_m3.metric("Progetti", m_stats.get("grossi", 0))
    col_m4.metric("Routine", m_stats.get("lavoretti", 0))
    st.write("---")
    
    st.markdown("### PARAMETRI VITALI")
    for stat in ["disciplina", "focus", "skill"]:
        info = data["stats"].get(stat, {"xp": 0, "level": 1, "last_active": str(date.today())})
        livello_attuale = info.get("level", 1)
        xp_attuali = info.get("xp", 0)
        prossimo_livello = 100 * livello_attuale
        
        st.markdown(f"**{stat.upper()}** — Livello {livello_attuale}")
        st.progress(min(1.0, xp_attuali / prossimo_livello))
        st.caption(f"Esperienza: {xp_attuali}/{prossimo_livello} XP")
        st.write("")

    st.write("---")
    st.markdown("### TRAGUARDI")
    streak = data.get("bar_streak", 0)
    badge_list = [
        {"nome": "Efficienza Fiscale", "desc": "Risolvi 3 scadenze urgenti.", "sbloccato": m_stats.get("urgenti", 0) >= 3},
        {"nome": "Inarrestabile", "desc": "Porta a termine 10 task totali.", "sbloccato": m_stats.get("totale", 0) >= 10},
        {"nome": "Fondo Solido", "desc": "5 giorni consecutivi senza spese accessorie.", "sbloccato": streak >= 5},
        {"nome": "Ascetismo Finanziario", "desc": "14 giorni consecutivi senza micro-spese.", "sbloccato": streak >= 14},
    ]
    
    for b in badge_list:
        if b["sbloccato"]:
            st.markdown(f"<div class='badge-unlocked'><b>{b['nome']}</b><br><span style='color:#888;'>{b['desc']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='badge-locked'><b>{b['nome']}</b><br><span style='color:#666;'>{b['desc']}</span></div>", unsafe_allow_html=True)

elif scelta_menu == "GARAGE & RISPARMI":
    st.title("GESTIONE FONDI")
    st.write("---")
    
    st.markdown("### CONTROLLO SPESE (DAILY CHECK)")
    today_str = str(date.today())
    last_check = data.get("last_bar_check", "")
    
    if last_check != today_str:
        st.info("Hai evitato spese superflue (es. bar) oggi?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("NESSUNA SPESA"):
                data["bar_streak"] += 1
                data["last_bar_check"] = today_str
                save_data(data)
                aggiungi_xp("disciplina", 15)
                st.rerun()
        with col2:
            if st.button("SPESA EFFETTUATA"):
                data["bar_streak"] = 0
                data["last_bar_check"] = today_str
                save_data(data)
                st.rerun()
    else:
        st.markdown(f"**Scia virtuosa attuale:** `{data['bar_streak']} giorni consecutivi`")
        
    st.write("---")
    st.markdown("### OBIETTIVI FINANZIARI")
    
    if "show_garage_form" not in st.session_state:
        st.session_state.show_garage_form = False
        
    col_g_title, col_g_btn = st.columns([8, 2])
    with col_g_btn:
        st.markdown('<div class="btn-minimal">', unsafe_allow_html=True)
        if st.button("ADD TARGET", key="toggle_garage", use_container_width=True):
            st.session_state.show_garage_form = not st.session_state.show_garage_form
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.show_garage_form:
        with st.form("new_garage_item"):
            col_g1, col_g2 = st.columns([2, 1])
            with col_g1:
                oggetto = st.text_input("Descrizione Obiettivo:")
            with col_g2:
                costo = st.number_input("Target Budget (€):", min_value=1)
            submit_item = st.form_submit_button("AGGIUNGI OBIETTIVO")
            if submit_item and oggetto and costo:
                data["garage"].append({
                    "oggetto": oggetto, "costo": costo, "risparmiati": 0
                })
                save_data(data)
                st.session_state.show_garage_form = False
                st.rerun()
                
    if not data["garage"]:
        st.info("Nessun obiettivo di risparmio impostato.")
    else:
        for idx, item in enumerate(data["garage"]):
            costo_tot = item["costo"]
            risp = item["risparmiati"]
            percentuale = min(1.0, risp / costo_tot)
            
            st.markdown(f"##### {item['oggetto']} — {risp}€ / {costo_tot}€")
            st.progress(percentuale)
            
            col_dep1, col_dep2 = st.columns([2, 1])
            with col_dep1:
                deposito = st.number_input("Importo da allocare (€):", min_value=1, key=f"dep_val_{idx}")
            with col_dep2:
                st.write("") 
                if st.button("ALLOCA FONDI", key=f"dep_btn_{idx}"):
                    item["risparmiati"] += deposito
                    save_data(data)
                    if item["risparmiati"] >= item["costo"]:
                        aggiungi_xp("skill", 100)
                    else:
                        aggiungi_xp("skill", 10)
                    st.rerun()
            st.write("---")
