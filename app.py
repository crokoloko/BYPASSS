import streamlit as st
import json
import os
import requests
from datetime import datetime, date

st.set_page_config(
    page_title="BYPASS",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAZIONE CREDENZIALI ---
try:
    BIN_ID = st.secrets["jsonbin"]["bin_id"]
    API_KEY = st.secrets["jsonbin"]["api_key"]
except Exception:
    BIN_ID = None
    API_KEY = None

if not BIN_ID or not API_KEY:
    st.error(
        "Credenziali JSONBin non configurate. Aggiungi bin_id e api_key in "
        "`.streamlit/secrets.toml` (vedi sezione [jsonbin])."
    )
    st.stop()

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #F5F5FA !important;
    }

    /* --- SFONDO ANIMATO A STRATI --- */
    .stApp {
        background: linear-gradient(-45deg, #0B0B1A, #1A0B2E, #0B1120, #16092B);
        background-size: 400% 400%;
        animation: gradientFlow 22s ease infinite;
        background-attachment: fixed !important;
        padding-bottom: 110px !important;
        position: relative;
        overflow-x: hidden;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Bagliori fluttuanti (glow orbs) sopra il gradiente */
    .stApp::before, .stApp::after {
        content: "";
        position: fixed;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.35;
        z-index: 0;
        pointer-events: none;
    }

    .stApp::before {
        width: 420px;
        height: 420px;
        top: -120px;
        left: -100px;
        background: radial-gradient(circle, #FF3366 0%, transparent 70%);
        animation: floatOrb1 16s ease-in-out infinite;
    }

    .stApp::after {
        width: 480px;
        height: 480px;
        bottom: -140px;
        right: -120px;
        background: radial-gradient(circle, #00FFFF 0%, transparent 70%);
        animation: floatOrb2 20s ease-in-out infinite;
    }

    @keyframes floatOrb1 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(60px, 80px) scale(1.15); }
    }

    @keyframes floatOrb2 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-50px, -60px) scale(1.1); }
    }

    /* Contenuto principale sopra i layer di sfondo */
    .main .block-container {
        position: relative;
        z-index: 1;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    h1 {
        background: linear-gradient(90deg, #FF3366, #FF9933, #00FFFF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmerTitle 6s linear infinite;
        font-weight: 800 !important;
    }

    @keyframes shimmerTitle {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    h4 {
        color: #FF6B93 !important;
        text-transform: uppercase;
        font-size: 0.85rem !important;
        letter-spacing: 2.5px;
        opacity: 0.9;
    }

    /* --- CARD PIU' LEGGERE (glass morbido, meno bordi netti) --- */
    div[data-testid="stForm"], .neumorphic-card {
        background: rgba(255, 255, 255, 0.035) !important;
        backdrop-filter: blur(16px) saturate(140%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(140%) !important;
        border-radius: 22px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25) !important;
        padding: 24px;
        margin-bottom: 24px;
        animation: fadeSlideIn 0.5s ease-out;
    }

    .task-card {
        background: rgba(255, 255, 255, 0.025);
        backdrop-filter: blur(14px) saturate(130%);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.22);
        display: flex;
        flex-direction: column;
        gap: 8px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeSlideIn 0.45s ease-out;
    }

    .task-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .task-card-urgent {
        border-left: 4px solid #FF3366;
        background: rgba(255, 51, 102, 0.035);
        animation: fadeSlideIn 0.45s ease-out, pulseUrgent 3s ease-in-out infinite;
    }

    @keyframes pulseUrgent {
        0%, 100% { box-shadow: 0 4px 24px rgba(255, 51, 102, 0.10); }
        50% { box-shadow: 0 4px 30px rgba(255, 51, 102, 0.28); }
    }

    .task-card-project {
        border-left: 4px solid #FF9933;
    }

    .task-card-routine {
        border-left: 4px solid #00FFFF;
    }

    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(45deg, #FF3366, #FF9933) !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 0 12px rgba(255, 51, 102, 0.35) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.25s ease-in-out;
    }

    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(45deg, #FF9933, #FF3366) !important;
        box-shadow: 0 0 22px rgba(255, 51, 102, 0.6) !important;
        transform: translateY(-2px) scale(1.01);
    }

    div.stButton > button:active, div.stFormSubmitButton > button:active {
        transform: translateY(0) scale(0.98);
    }

    .nav-active > div > button {
        background: linear-gradient(45deg, #00FFFF, #0088FF) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.55) !important;
    }

    .btn-minimal > div > button {
        padding: 0.3rem 0.8rem !important;
        font-size: 0.8rem !important;
        border-radius: 10px !important;
    }

    .btn-danger > div > button {
        background: linear-gradient(45deg, #FF5757, #99001F) !important;
        box-shadow: 0 0 8px rgba(255, 0, 0, 0.25) !important;
    }

    /* --- MENU A TENDINA COMPATTO SULLE TASK CARD --- */
    .task-menu {
        display: flex;
        justify-content: flex-end;
        margin-top: -6px;
    }

    .task-menu div[data-testid="stPopover"] > button {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        font-weight: 700;
        padding: 0.25rem 0.6rem !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        min-height: 0 !important;
    }

    .task-menu div[data-testid="stPopover"] > button:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
        transform: none;
    }

    div[data-testid="stPopoverBody"] {
        background: rgba(20, 12, 35, 0.92) !important;
        backdrop-filter: blur(18px) saturate(150%) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        padding: 10px !important;
        gap: 6px !important;
    }

    div[data-testid="stPopoverBody"] button {
        text-transform: none !important;
        letter-spacing: 0.2px !important;
        font-size: 0.85rem !important;
        padding: 0.45rem 0.8rem !important;
        box-shadow: none !important;
    }

    .stats-container {
        display: flex;
        gap: 10px;
        width: 100%;
        margin-bottom: 20px;
    }
    .stat-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        padding: 12px 6px;
        text-align: center;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.22);
        transition: transform 0.2s ease;
    }
    .stat-box:hover {
        transform: translateY(-2px);
    }
    .stat-box .stat-value {
        color: #00FFFF;
        font-weight: 700;
        font-size: 1.35rem;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.35);
        line-height: 1.2;
    }
    .stat-box .stat-label {
        color: #C9C9D6;
        font-weight: 500;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    .fixed-bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 8, 30, 0.85);
        backdrop-filter: blur(24px) saturate(160%);
        -webkit-backdrop-filter: blur(24px) saturate(160%);
        border-top: 1px solid rgba(255, 255, 255, 0.10);
        box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.5);
        z-index: 999999;
        padding: 8px 0;
    }

    .fixed-bottom-nav div.stButton > button {
        box-shadow: none !important;
        padding: 0.4rem 0 !important;
    }

    .fixed-bottom-nav .nav-active > div > button {
        box-shadow: 0 0 14px rgba(0, 255, 255, 0.45) !important;
    }

    .fixed-bottom-inner {
        max-width: 500px;
        margin: 0 auto;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #FF3366, #00FFFF) !important;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.45);
        transition: width 0.6s ease-in-out;
    }

    .badge-unlocked {
        padding: 18px 24px;
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 255, 0.25);
        border-left: 5px solid #00FFFF;
        box-shadow: 0 8px 24px rgba(0, 255, 255, 0.10);
        margin-bottom: 16px;
        animation: fadeSlideIn 0.5s ease-out;
    }

    .badge-locked {
        padding: 18px 24px;
        background: rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        margin-bottom: 16px;
        opacity: 0.45;
    }

    .stTextInput input, .stSelectbox div div, .stNumberInput input {
        background: rgba(0, 0, 0, 0.25) !important;
        color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        padding: 12px 16px !important;
        font-weight: 500;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .stTextInput input:focus {
        border-color: #00FFFF !important;
        box-shadow: 0 0 12px rgba(0, 255, 255, 0.35) !important;
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
            db = req.json().get("record", default_data)
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
    except Exception:
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

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "bacheca"

# --- RENDER TAB: BACHECA (RADAR OPERATIVO) ---
if st.session_state.active_tab == "bacheca":
    col_title, col_btn = st.columns([8, 2])
    with col_title:
        st.title("BYPASS")
        st.markdown("#### RADAR OPERATIVO")
    with col_btn:
        st.write("")
        st.write("")
        st.markdown('<div class="btn-minimal">', unsafe_allow_html=True)
        if st.button("ADD", use_container_width=True):
            st.session_state.show_mission_form = not st.session_state.show_mission_form
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # Form di Inserimento Missione
    if st.session_state.show_mission_form:
        with st.form("new_mission_form", clear_on_submit=True):
            st.markdown("**NUOVA MISSIONE OPERATIVA**")
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

            xp_anteprima = 40 if "URGENTE" in tipo else (30 if "Priorità" in tipo else 15)
            st.caption(f"Ricompensa stimata: `{xp_anteprima} XP` nell'area `{stat_clean.upper()}`")

            submit = st.form_submit_button("INSERISCI A SISTEMA")

            if submit and titolo:
                nuova_missione = {
                    "id": max([t.get("id", 0) for t in data.get("tasks", [])], default=0) + 1,
                    "titolo": titolo,
                    "tipo": tipo,
                    "stat": stat_clean,
                    "scadenza": str(scadenza) if scadenza else None,
                    "completato": False
                }
                data["tasks"].append(nuova_missione)
                save_data(data)
                st.session_state.show_mission_form = False
                st.success("Task registrato nel radar!")
                st.rerun()

    all_tasks = data.get("tasks", [])
    attive = [t for t in all_tasks if not t.get("completato", False)]

    if not attive:
        st.info("Nessun task in sospeso. Sistema allineato.")
    else:
        # Filtri rapidi puliti
        col_f_a, col_f_b = st.columns(2)
        with col_f_a:
            filtro_tipo = st.selectbox("Filtra per Tipo:", ["Tutti", "Scadenze Urgenti", "Progetti", "Routine"])
        with col_f_b:
            filtro_area = st.selectbox("Filtra per Area:", ["Tutte le aree", "disciplina", "focus", "skill"])

        task_filtrati = attive
        if filtro_tipo == "Scadenze Urgenti":
            task_filtrati = [t for t in task_filtrati if "URGENTE" in t.get("tipo", "")]
        elif filtro_tipo == "Progetti":
            task_filtrati = [t for t in task_filtrati if "Priorità" in t.get("tipo", "")]
        elif filtro_tipo == "Routine":
            task_filtrati = [t for t in task_filtrati if "Routine" in t.get("tipo", "")]

        if filtro_area != "Tutte le aree":
            task_filtrati = [t for t in task_filtrati if t.get("stat") == filtro_area]

        st.write("")

        # Render delle Card Interattive per ogni task
        for task in task_filtrati:
            t_id = task.get("id")
            t_titolo = task.get("titolo")
            t_tipo = task.get("tipo", "")
            t_stat = task.get("stat", "disciplina")
            t_scadenza = task.get("scadenza")

            # Determinazione classe CSS e badge in base al tipo
            if "URGENTE" in t_tipo:
                card_class = "task-card task-card-urgent"
                badge_text = "URGENTE"
                xp_reward = 40
                cat_stat = "urgenti"
                if t_scadenza:
                    try:
                        giorni = (datetime.strptime(t_scadenza, "%Y-%m-%d").date() - date.today()).days
                        badge_text = f"SCADUTA ({t_scadenza})" if giorni < 0 else f"SCADE TRA {giorni} GG"
                    except:
                        pass
            elif "Priorità" in t_tipo:
                card_class = "task-card task-card-project"
                badge_text = "PROGETTO"
                xp_reward = 30
                cat_stat = "grossi"
            else:
                card_class = "task-card task-card-routine"
                badge_text = "ROUTINE"
                xp_reward = 15
                cat_stat = "lavoretti"

            # Layout Card con Colonne per Pulsanti Azione (Completa / Elimina)
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.7rem; color:#00FFFF; font-weight:700; letter-spacing:1px;'>{badge_text} • AREA: {t_stat.upper()} (+{xp_reward} XP)</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.05rem; font-weight:600; color:#FFFFFF; margin: 4px 0;'>{t_titolo}</div>", unsafe_allow_html=True)

            col_spacer, col_menu = st.columns([5, 1])
            with col_menu:
                st.markdown('<div class="task-menu">', unsafe_allow_html=True)
                with st.popover("⋮", use_container_width=True):
                    if st.button("✅ Completa", key=f"comp_{t_id}", use_container_width=True):
                        for item in data["tasks"]:
                            if item.get("id") == t_id:
                                item["completato"] = True
                        data["mission_stats"]["totale"] = data["mission_stats"].get("totale", 0) + 1
                        data["mission_stats"][cat_stat] = data["mission_stats"].get(cat_stat, 0) + 1
                        save_data(data)
                        aggiungi_xp(t_stat, xp_reward)
                        st.toast(f"Missione completata (+{xp_reward} XP in {t_stat.upper()})")
                        st.rerun()
                    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                    if st.button("🗑️ Elimina", key=f"del_{t_id}", use_container_width=True):
                        data["tasks"] = [item for item in data["tasks"] if item.get("id") != t_id]
                        save_data(data)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

# --- RENDER TAB: PROFILO ---
elif st.session_state.active_tab == "profilo":
    st.title("STATO OPERATIVO")
    st.markdown(f"#### LIVELLO REP: {data['stats']['rep']['level']}")
    st.write("---")

    st.markdown("### STATISTICHE")
    m_stats = data.get("mission_stats", {"totale": 0, "urgenti": 0, "grossi": 0, "lavoretti": 0})

    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-value">{m_stats.get("totale", 0)}</div>
                <div class="stat-label">Totali</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{m_stats.get("urgenti", 0)}</div>
                <div class="stat-label">Scadenze</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{m_stats.get("grossi", 0)}</div>
                <div class="stat-label">Progetti</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{m_stats.get("lavoretti", 0)}</div>
                <div class="stat-label">Routine</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
            st.markdown(f"<div class='badge-unlocked'><b>{b['nome']}</b><br><span style='color:#CCCCCC;'>{b['desc']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='badge-locked'><b>{b['nome']}</b><br><span style='color:#888888;'>{b['desc']}</span></div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 📂 STORICO MISSIONI COMPLETATE")
    completati = [t for t in data.get("tasks", []) if t.get("completato", False)]
    if not completati:
        st.caption("Nessuna missione completata di recente.")
    else:
        for t in reversed(completati[-10:]):
            st.markdown(f"✅ ~~{t.get('titolo')}~~ `({t.get('stat', 'base').upper()})`")

# --- RENDER TAB: GARAGE (GESTIONE FONDI) ---
elif st.session_state.active_tab == "garage":
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
                st.success("Obiettivo aggiunto!")
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

# --- BARRA DI NAVIGAZIONE INFERIORE FISSA CON STATO ATTIVO ---
st.markdown('<div class="fixed-bottom-nav"><div class="fixed-bottom-inner">', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    class_b = "nav-active" if st.session_state.active_tab == "bacheca" else ""
    st.markdown(f'<div class="{class_b}">', unsafe_allow_html=True)
    if st.button("📋", use_container_width=True, key="nav_bacheca"):
        st.session_state.active_tab = "bacheca"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nav_col2:
    class_p = "nav-active" if st.session_state.active_tab == "profilo" else ""
    st.markdown(f'<div class="{class_p}">', unsafe_allow_html=True)
    if st.button("📊", use_container_width=True, key="nav_profilo"):
        st.session_state.active_tab = "profilo"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nav_col3:
    class_g = "nav-active" if st.session_state.active_tab == "garage" else ""
    st.markdown(f'<div class="{class_g}">', unsafe_allow_html=True)
    if st.button("🚗", use_container_width=True, key="nav_garage"):
        st.session_state.active_tab = "garage"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
