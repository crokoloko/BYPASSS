import streamlit as st
import json
import os
import requests
from datetime import datetime, date

st.set_page_config(
    page_title="BYPASS.EXE",
    page_icon="🐱",
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Permanent+Marker&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #1a1a1a;
        background-image: radial-gradient(#2b2b2b 2px, transparent 2px);
        background-size: 30px 30px;
        color: #e0e0e0;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #111 !important;
        border-right: 4px solid #d92525;
    }
    
    h1, h2, h3 {
        font-family: 'Permanent Marker', cursive !important;
        color: #f4f4f4 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 0px #000;
    }
    h4, h5 {
        font-family: 'Permanent Marker', cursive !important;
        color: #d92525 !important;
        letter-spacing: 1px;
    }

    div[data-testid="stForm"] {
        background: #222 !important;
        border: 2px solid #555 !important;
        border-radius: 4px !important;
        box-shadow: 6px 6px 0px rgba(0, 0, 0, 0.8) !important;
        padding: 15px;
        margin-bottom: 20px;
    }

    div.stButton > button, div.stFormSubmitButton > button {
        background: #d92525;
        color: #fff;
        border: 2px solid #000;
        border-radius: 4px;
        padding: 0.6rem 1.2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        width: 100%;
        box-shadow: 4px 4px 0px #000;
        transition: all 0.1s ease-in-out;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: #ff3333;
        color: #fff;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000;
    }
    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 0px 0px 0px #000;
    }
    
    .btn-minimal > div > button {
        padding: 0.2rem 0.5rem !important;
        font-size: 1.2rem !important;
        background: #333;
        color: #fff;
    }

    div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-family: 'Permanent Marker', cursive !important;
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #999 !important;
        font-weight: 800 !important;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] {
        background: #222;
        border: 2px solid #444;
        border-left: 6px solid #d92525;
        padding: 12px;
    }

    .stTextInput input, .stSelectbox div div, .stNumberInput input {
        background-color: #111 !important;
        color: #fff !important;
        border: 2px solid #444 !important;
        border-radius: 4px !important;
        font-weight: 600;
    }
    .stTextInput input:focus {
        border-color: #d92525 !important;
    }

    div[data-testid="stProgress"] > div > div > div > div {
        background: #d92525 !important;
        border-radius: 2px;
    }

    .badge-unlocked {
        padding: 14px 18px;
        background: #222;
        border: 2px solid #000;
        border-left: 8px solid #d92525;
        margin-bottom: 12px;
        box-shadow: 4px 4px 0px #000;
    }
    .badge-locked {
        padding: 14px 18px;
        background: #1a1a1a;
        border: 2px dashed #444;
        margin-bottom: 12px;
        opacity: 0.5;
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
        st.toast(f"⚡ LEVEL UP: {stat.upper()} sale al Livello {data['stats'][stat]['level']}! 😸", icon="🆙")
        
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

st.sidebar.title("⚡ BYPASS")
st.sidebar.caption("SISTEMA DI CONTROLLO 🐾")
st.sidebar.write("---")

scelta_menu = st.sidebar.radio(
    "NAVIGAZIONE SYSTEM:",
    ["📋 BACHECA MISSIONI 🐱", "👤 PROFILO & STATS 🐈", "🚘 GARAGE & RISPARMI 🐈‍⬛"],
    label_visibility="collapsed"
)

st.sidebar.write("---")
st.sidebar.markdown(f"### 👑 REP GLOBALE: `Lvl. {data['stats']['rep']['level']}`")
st.sidebar.progress(min(1.0, (data['stats']['rep'].get('xp', 0)) / (100 * max(1, data['stats']['rep']['level']))))
st.sidebar.markdown("<center>😸 Meow!</center>", unsafe_allow_html=True)

if scelta_menu == "📋 BACHECA MISSIONI 🐱":
    
    col_title, col_btn = st.columns([8, 2])
    with col_title:
        st.title("⚡ BYPASS")
        st.markdown("#### `IL TUO RADAR OPERATIVO.` 🐾")
    with col_btn:
        st.write("")
        st.write("")
        st.markdown('<div class="btn-minimal">', unsafe_allow_html=True)
        if st.button("➕ ADD", use_container_width=True):
            st.session_state.show_mission_form = not st.session_state.show_mission_form
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("---")

    if st.session_state.show_mission_form:
        with st.form("new_mission_form", clear_on_submit=True):
            titolo = st.text_input("Cosa devi fare? (es. Bolletta luce, Pulire lettiera 🐈)")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                tipo = st.selectbox("Gravosità / Urgenza", [
                    "Scadenza URGENTE (+40 XP)", 
                    "I Grossi / Priorità (+30 XP)", 
                    "Lavoretti / Routine (+15 XP)"
                ])
            with col_f2:
                stat = st.selectbox("Area di potenziamento", [
                    "disciplina (Scadenze / Burocrazia)", 
                    "focus (Lavoro / Progetti seri)", 
                    "skill (Fai-da-te / Manutenzione / Casa)"
                ])
                stat_clean = stat.split(" ")[0]
            
            scadenza = None
            if "URGENTE" in tipo:
                scadenza = st.date_input("Data limite inderogabile:", min_value=date.today())
                
            submit = st.form_submit_button("🔥 INSERISCI A SISTEMA")
            
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
                st.toast(f"Faccenda '{titolo}' appuntata! 🐾", icon="🚀")
                st.rerun()

    all_tasks = data.get("tasks", [])
    attive = [t for t in all_tasks if not t.get("completato", False)]

    if not attive:
        st.info("⚡ Nessuna faccenda in sospeso. Il radar è pulito! Tempo per le coccole 🐱")
    else:
        scadenze = [t for t in attive if "URGENTE" in t.get("tipo", "")]
        scadenze.sort(key=lambda x: x.get("scadenza") if x.get("scadenza") else "9999-12-31")
        grossi = [t for t in attive if "Priorità" in t.get("tipo", "")]
        lavoretti = [t for t in attive if "Routine" in t.get("tipo", "")]
        lista_ordinata = scadenze + grossi + lavoretti

        for task in lista_ordinata:
            t_tipo = task.get("tipo", "Lavoretti / Routine (+15 XP)")
            t_titolo = task.get("titolo", "Senza Nome")
            t_scadenza = task.get("scadenza")
            t_id = task.get("id", 0)
            t_stat = task.get("stat", "disciplina")
            
            if "URGENTE" in t_tipo and t_scadenza:
                try:
                    scad_date = datetime.strptime(t_scadenza, "%Y-%m-%d").date()
                    giorni_rimasti = (scad_date - date.today()).days
                    if giorni_rimasti <= 0:
                        label = f"🚨 [SCADUTA / SCADE OGGI] — {t_titolo}"
                    elif giorni_rimasti == 1:
                        label = f"⚠️ [SCADE DOMANI] — {t_titolo}"
                    else:
                        label = f"⏳ [TRA {giorni_rimasti} GG] — {t_titolo}"
                except:
                    label = f"⏳ [SCADENZA] — {t_titolo}"
                xp_reward = 40
                categoria_stat = "urgenti"
            elif "Priorità" in t_tipo:
                label = f"🔴 [PRIORITÀ] — {t_titolo}"
                xp_reward = 30
                categoria_stat = "grossi"
            else:
                label = f"⚪ [ROUTINE] — {t_titolo}"
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
                st.toast(f"Fatto! +{xp_reward} XP in {t_stat.upper()} 😸", icon="⚡")
                st.rerun()

elif scelta_menu == "👤 PROFILO & STATS 🐈":
    st.title("👤 STATO OPERATIVO 🐈")
    st.markdown(f"#### LIVELLO REP: `{data['stats']['rep']['level']}`")
    st.write("---")
    
    st.markdown("### 📈 CRUSCOTTO FACCENDE")
    m_stats = data.get("mission_stats", {"totale": 0, "urgenti": 0, "grossi": 0, "lavoretti": 0})
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("🔥 Svolte", m_stats.get("totale", 0))
    col_m2.metric("⚠️ Scadenze", m_stats.get("urgenti", 0))
    col_m3.metric("🔴 I Grossi", m_stats.get("grossi", 0))
    col_m4.metric("⚪ Routine", m_stats.get("lavoretti", 0))
    st.write("---")
    
    st.markdown("### 📊 PARAMETRI")
    for stat in ["disciplina", "focus", "skill"]:
        info = data["stats"].get(stat, {"xp": 0, "level": 1, "last_active": str(date.today())})
        livello_attuale = info.get("level", 1)
        xp_attuali = info.get("xp", 0)
        prossimo_livello = 100 * livello_attuale
        
        st.markdown(f"**{stat.upper()}** — `Lvl {livello_attuale}`")
        st.progress(min(1.0, xp_attuali / prossimo_livello))
        st.caption(f"Esperienza: {xp_attuali}/{prossimo_livello} XP")
        st.write("")

    st.write("---")
    st.markdown("### 🏆 BACHECA TROFEI 🐾")
    streak = data.get("bar_streak", 0)
    badge_list = [
        {"nome": "Conti Puliti 🐈", "desc": "Risolvi 3 scadenze urgenti.", "sbloccato": m_stats.get("urgenti", 0) >= 3},
        {"nome": "Macchina da Guerra 🐯", "desc": "Porta a termine 10 faccende totali.", "sbloccato": m_stats.get("totale", 0) >= 10},
        {"nome": "Sotto i Radar 😼", "desc": "5 giorni di fila niente bar.", "sbloccato": streak >= 5},
        {"nome": "Infiltrato Invisibile 🐾", "desc": "14 giorni di fila senza micro-spese.", "sbloccato": streak >= 14},
    ]
    
    for b in badge_list:
        if b["sbloccato"]:
            st.markdown(f"<div class='badge-unlocked'>👑 <b>{b['nome']}</b><br><small>{b['desc']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='badge-locked'>🔒 <b>{b['nome']}</b><br><small>{b['desc']}</small></div>", unsafe_allow_html=True)

elif scelta_menu == "🚘 GARAGE & RISPARMI 🐈‍⬛":
    st.title("🚘 IL GARAGE 🐈‍⬛")
    st.write("---")
    
    st.markdown("### 🚭 Sfida del Bar")
    today_str = str(date.today())
    last_check = data.get("last_bar_check", "")
    
    if last_check != today_str:
        st.info("⚡ Hai speso soldi al bar oggi?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("SONO RIMASTO PULITO 💸 😸"):
                data["bar_streak"] += 1
                data["last_bar_check"] = today_str
                save_data(data)
                aggiungi_xp("disciplina", 15)
                st.rerun()
        with col2:
            if st.button("SÌ, HO SPESO. 😿"):
                data["bar_streak"] = 0
                data["last_bar_check"] = today_str
                save_data(data)
                st.rerun()
    else:
        st.markdown(f"🔥 **Scia senza bar:** `{data['bar_streak']} giorni` 🐾")
        
    st.write("---")
    st.markdown("### 📦 OBIETTIVI")
    
    if "show_garage_form" not in st.session_state:
        st.session_state.show_garage_form = False
        
    col_g_title, col_g_btn = st.columns([8, 2])
    with col_g_btn:
        st.markdown('<div class="btn-minimal">', unsafe_allow_html=True)
        if st.button("➕ ADD", key="toggle_garage", use_container_width=True):
            st.session_state.show_garage_form = not st.session_state.show_garage_form
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.show_garage_form:
        with st.form("new_garage_item"):
            col_g1, col_g2 = st.columns([2, 1])
            with col_g1:
                oggetto = st.text_input("Oggetto (es. Cibo per gatti 🐟):")
            with col_g2:
                costo = st.number_input("Costo (€):", min_value=1)
            submit_item = st.form_submit_button("🔥 METTI IN CODA")
            if submit_item and oggetto and costo:
                data["garage"].append({
                    "oggetto": oggetto, "costo": costo, "risparmiati": 0
                })
                save_data(data)
                st.session_state.show_garage_form = False
                st.rerun()
                
    if not data["garage"]:
        st.info("Nessun obiettivo nel garage. 🐱")
    else:
        for idx, item in enumerate(data["garage"]):
            costo_tot = item["costo"]
            risp = item["risparmiati"]
            percentuale = min(1.0, risp / costo_tot)
            
            st.markdown(f"##### 📦 {item['oggetto']} — `{risp}€` su `{costo_tot}€`")
            st.progress(percentuale)
            
            col_dep1, col_dep2 = st.columns([2, 1])
            with col_dep1:
                deposito = st.number_input("Quota (€):", min_value=1, key=f"dep_val_{idx}")
            with col_dep2:
                st.write("") 
                if st.button("DEPOSITA 🐾", key=f"dep_btn_{idx}"):
                    item["risparmiati"] += deposito
                    save_data(data)
                    if item["risparmiati"] >= item["costo"]:
                        aggiungi_xp("skill", 100)
                    else:
                        aggiungi_xp("skill", 10)
                    st.rerun()
            st.write("---")
