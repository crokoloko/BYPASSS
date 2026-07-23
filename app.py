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
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --ink: #17140F;
        --panel: #221D16;
        --panel-soft: #2A2419;
        --brass: #C9A227;
        --brass-dim: #8F7620;
        --moss: #6B8F71;
        --rust: #B5453A;
        --ivory: #F0EAE0;
        --muted: #9C9484;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--ivory) !important;
    }

    /* --- SFONDO: espresso caldo, vignette naturale, quasi immobile --- */
    .stApp {
        background:
            radial-gradient(circle at 22% -10%, rgba(201, 162, 39, 0.07), transparent 55%),
            radial-gradient(circle at 85% 105%, rgba(107, 143, 113, 0.05), transparent 55%),
            var(--ink);
        background-attachment: fixed !important;
        padding-bottom: 118px !important;
        position: relative;
    }

    .main .block-container {
        position: relative;
        z-index: 1;
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] { display: none !important; }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Fraunces', serif !important;
        color: var(--ivory) !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }

    h1 {
        color: var(--brass) !important;
        font-weight: 700 !important;
        font-size: 2.4rem !important;
        margin-bottom: 0.2rem !important;
        border-bottom: 1px solid rgba(201, 162, 39, 0.22);
        padding-bottom: 10px;
    }

    h4 {
        font-family: 'Inter', sans-serif !important;
        color: var(--muted) !important;
        text-transform: uppercase;
        font-size: 0.78rem !important;
        letter-spacing: 3px;
        font-weight: 500 !important;
    }

    h3 {
        font-size: 1.15rem !important;
        color: var(--ivory) !important;
    }

    /* --- NUMERI E DATI IN MONOSPACE --- */
    .num, .medallion-level, .medallion-xp, .stat-value {
        font-family: 'IBM Plex Mono', monospace !important;
    }

    /* --- PANNELLI / FORM --- */
    div[data-testid="stForm"], .card-panel {
        background: var(--panel) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(201, 162, 39, 0.14) !important;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4) !important;
        padding: 22px;
        margin-bottom: 20px;
    }

    /* --- TASK CARD --- */
    .task-card {
        background: var(--panel);
        border-radius: 14px;
        border: 1px solid rgba(240, 234, 224, 0.06);
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.32);
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .task-card-urgent { border-left: 3px solid var(--rust); }
    .task-card-project { border-left: 3px solid var(--brass); }
    .task-card-routine { border-left: 3px solid var(--moss); }

    .task-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .task-eyebrow.urgent { color: var(--rust); }
    .task-eyebrow.project { color: var(--brass); }
    .task-eyebrow.routine { color: var(--moss); }

    .urgent-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--rust);
        display: inline-block;
        animation: dotBreathe 2.4s ease-in-out infinite;
    }

    @keyframes dotBreathe {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }

    .task-title {
        font-family: 'Fraunces', serif;
        font-size: 1.08rem;
        font-weight: 500;
        color: var(--ivory);
        margin: 2px 0 4px 0;
    }

    /* --- BOTTONI --- */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(160deg, var(--brass), var(--brass-dim)) !important;
        color: var(--ink) !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: none !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: 0.3px;
        width: 100%;
        transition: transform 0.18s ease, filter 0.18s ease;
    }

    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
    }

    div.stButton > button:active, div.stFormSubmitButton > button:active {
        transform: translateY(0);
        filter: brightness(0.96);
    }

    .btn-ghost > div > button {
        background: transparent !important;
        color: var(--brass) !important;
        border: 1px solid rgba(201, 162, 39, 0.35) !important;
        padding: 0.35rem 0.9rem !important;
        font-size: 0.82rem !important;
    }

    .btn-danger-text > div > button {
        background: transparent !important;
        color: var(--rust) !important;
        border: none !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        text-align: left !important;
    }

    .btn-confirm-text > div > button {
        background: transparent !important;
        color: var(--moss) !important;
        border: none !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        text-align: left !important;
    }

    /* --- MENU AZIONI SULLA TASK (popover a tendina) --- */
    .task-menu {
        display: flex;
        justify-content: flex-end;
        margin-top: -4px;
    }

    .task-menu div[data-testid="stPopover"] > button {
        background: transparent !important;
        color: var(--muted) !important;
        border: 1px solid rgba(240, 234, 224, 0.12) !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        font-weight: 700;
        padding: 0.15rem 0.55rem !important;
        min-height: 0 !important;
    }

    .task-menu div[data-testid="stPopover"] > button:hover {
        border-color: rgba(201, 162, 39, 0.4) !important;
        color: var(--brass) !important;
        transform: none;
    }

    div[data-testid="stPopoverBody"] {
        background: var(--panel-soft) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(201, 162, 39, 0.18) !important;
        padding: 8px !important;
        gap: 2px !important;
    }

    div[data-testid="stPopoverBody"] button {
        font-size: 0.85rem !important;
        padding: 0.4rem 0.5rem !important;
    }

    /* --- STAT BOX (Profilo) --- */
    .stats-container {
        display: flex;
        gap: 10px;
        width: 100%;
        margin-bottom: 18px;
    }
    .stat-box {
        flex: 1;
        background: var(--panel);
        border-radius: 12px;
        border: 1px solid rgba(240, 234, 224, 0.06);
        padding: 12px 6px;
        text-align: center;
    }
    .stat-box .stat-value {
        color: var(--brass);
        font-weight: 600;
        font-size: 1.3rem;
        line-height: 1.2;
    }
    .stat-box .stat-label {
        color: var(--muted);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 4px;
    }

    /* --- MEDAGLIONI CIRCOLARI DI LIVELLO --- */
    .medallions-row {
        display: flex;
        justify-content: space-around;
        gap: 12px;
        margin: 8px 0 22px 0;
        flex-wrap: wrap;
    }

    .medallion-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    .medallion-ring {
        width: 104px;
        height: 104px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 5px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35);
    }

    .medallion-face {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: var(--panel);
        border: 1px solid rgba(201, 162, 39, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .medallion-level {
        font-size: 1.7rem;
        font-weight: 600;
        color: var(--ivory);
        line-height: 1;
    }

    .medallion-xp {
        font-size: 0.58rem;
        color: var(--muted);
        margin-top: 3px;
        letter-spacing: 0.3px;
    }

    .medallion-tag {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--muted);
    }

    .medallion-hero .medallion-ring { width: 140px; height: 140px; }
    .medallion-hero .medallion-level { font-size: 2.3rem; }

    /* --- BADGE / TRAGUARDI --- */
    .badge-unlocked {
        padding: 16px 20px;
        background: rgba(201, 162, 39, 0.06);
        border-radius: 12px;
        border: 1px solid rgba(201, 162, 39, 0.28);
        border-left: 4px solid var(--brass);
        margin-bottom: 14px;
    }

    .badge-locked {
        padding: 16px 20px;
        background: rgba(240, 234, 224, 0.015);
        border-radius: 12px;
        border: 1px dashed rgba(240, 234, 224, 0.08);
        margin-bottom: 14px;
        opacity: 0.55;
    }

    .badge-unlocked b, .badge-locked b {
        font-family: 'Fraunces', serif;
        font-weight: 600;
    }

    /* --- PROGRESS BAR --- */
    div[data-testid="stProgress"] > div > div > div > div {
        background: var(--brass) !important;
        border-radius: 8px;
    }
    div[data-testid="stProgress"] > div > div > div {
        background: rgba(240, 234, 224, 0.08) !important;
        border-radius: 8px;
    }

    /* --- INPUT --- */
    .stTextInput input, .stSelectbox div div, .stNumberInput input {
        background: var(--panel-soft) !important;
        color: var(--ivory) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(240, 234, 224, 0.10) !important;
        padding: 10px 14px !important;
        font-weight: 500;
    }

    .stTextInput input:focus {
        border-color: var(--brass) !important;
        box-shadow: none !important;
    }

    /* --- STORICO --- */
    .history-row {
        font-family: 'Inter', sans-serif;
        color: var(--muted);
        font-size: 0.9rem;
        padding: 6px 0;
        border-bottom: 1px solid rgba(240, 234, 224, 0.05);
    }
    .history-row .tag {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        color: var(--brass-dim);
        margin-left: 6px;
    }

    /* --- NAVIGAZIONE INFERIORE --- */
    .fixed-bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(23, 20, 15, 0.94);
        border-top: 1px solid rgba(201, 162, 39, 0.14);
        box-shadow: 0 -10px 24px rgba(0, 0, 0, 0.45);
        z-index: 999999;
        padding: 10px 0;
    }

    .fixed-bottom-inner {
        max-width: 500px;
        margin: 0 auto;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    .fixed-bottom-nav div.stButton > button {
        background: transparent !important;
        color: var(--muted) !important;
        box-shadow: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        padding: 0.4rem 0 !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
    }

    .fixed-bottom-nav .nav-active > div > button {
        color: var(--brass) !important;
        border-bottom: 2px solid var(--brass) !important;
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
        req = requests.get(URL, headers=HEADERS, timeout=8)
        if req.status_code == 200:
            db = req.json().get("record", default_data)
            if "garage" not in db: db["garage"] = []
            if "bar_streak" not in db: db["bar_streak"] = 0
            if "last_bar_check" not in db: db["last_bar_check"] = str(date.today())
            if "mission_stats" not in db: db["mission_stats"] = {"totale": 0, "urgenti": 0, "grossi": 0, "lavoretti": 0}
            if "stats" not in db: db["stats"] = default_data["stats"]
            return db
        else:
            st.warning(f"Connessione a JSONBin non riuscita (codice {req.status_code}). Uso dati vuoti temporanei.")
            return default_data
    except requests.exceptions.Timeout:
        st.warning("JSONBin non ha risposto in tempo. Uso dati vuoti temporanei.")
        return default_data
    except Exception as e:
        st.warning(f"Errore di connessione a JSONBin: {e}. Uso dati vuoti temporanei.")
        return default_data


def save_data(data):
    try:
        requests.put(URL, json=data, headers=HEADERS, timeout=8)
    except Exception:
        pass


with st.spinner("Sincronizzazione dati..."):
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
        st.toast(f"Livello superato: {stat.upper()} sale al Livello {data['stats'][stat]['level']}")

    livelli = [
        data["stats"].get("disciplina", {}).get("level", 1),
        data["stats"].get("focus", {}).get("level", 1),
        data["stats"].get("skill", {}).get("level", 1)
    ]
    media_livelli = sum(livelli) // 3
    data["stats"]["rep"]["level"] = max(1, media_livelli)

    save_data(data)


def medaglione_html(level, xp, xp_max, label, hero=False):
    pct = max(0, min(100, int((xp / xp_max) * 100))) if xp_max else 0
    wrap_class = "medallion-wrap medallion-hero" if hero else "medallion-wrap"
    return f"""
    <div class="{wrap_class}">
        <div class="medallion-ring" style="background: conic-gradient(#C9A227 {pct}%, rgba(240,234,224,0.08) {pct}%);">
            <div class="medallion-face">
                <div class="medallion-level">{level}</div>
                <div class="medallion-xp">{xp}/{xp_max} XP</div>
            </div>
        </div>
        <div class="medallion-tag">{label}</div>
    </div>
    """


if "show_mission_form" not in st.session_state:
    st.session_state.show_mission_form = False

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "bacheca"

# --- RENDER TAB: BACHECA (RADAR OPERATIVO) ---
if st.session_state.active_tab == "bacheca":
    col_title, col_btn = st.columns([8, 3])
    with col_title:
        st.title("BYPASS")
        st.markdown("#### Radar Operativo")
    with col_btn:
        st.write("")
        st.write("")
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("+ Nuova", use_container_width=True):
            st.session_state.show_mission_form = not st.session_state.show_mission_form
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Form di Inserimento Missione
    if st.session_state.show_mission_form:
        with st.form("new_mission_form", clear_on_submit=True):
            st.markdown("**Nuova missione operativa**")
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
            st.caption(f"Ricompensa stimata: {xp_anteprima} XP nell'area {stat_clean.upper()}")

            submit = st.form_submit_button("Inserisci a sistema")

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
                st.success("Task registrato nel radar.")
                st.rerun()

    all_tasks = data.get("tasks", [])
    attive = [t for t in all_tasks if not t.get("completato", False)]

    if not attive:
        st.info("Nessun task in sospeso. Sistema allineato.")
    else:
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

        for task in task_filtrati:
            t_id = task.get("id")
            t_titolo = task.get("titolo")
            t_tipo = task.get("tipo", "")
            t_stat = task.get("stat", "disciplina")
            t_scadenza = task.get("scadenza")

            if "URGENTE" in t_tipo:
                card_class = "task-card task-card-urgent"
                eyebrow_class = "task-eyebrow urgent"
                badge_text = "URGENTE"
                xp_reward = 40
                cat_stat = "urgenti"
                dot_html = '<span class="urgent-dot"></span>'
                if t_scadenza:
                    try:
                        giorni = (datetime.strptime(t_scadenza, "%Y-%m-%d").date() - date.today()).days
                        badge_text = f"SCADUTA ({t_scadenza})" if giorni < 0 else f"SCADE TRA {giorni} GG"
                    except Exception:
                        pass
            elif "Priorità" in t_tipo:
                card_class = "task-card task-card-project"
                eyebrow_class = "task-eyebrow project"
                badge_text = "PROGETTO"
                xp_reward = 30
                cat_stat = "grossi"
                dot_html = ""
            else:
                card_class = "task-card task-card-routine"
                eyebrow_class = "task-eyebrow routine"
                badge_text = "ROUTINE"
                xp_reward = 15
                cat_stat = "lavoretti"
                dot_html = ""

            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            st.markdown(
                f"<div class='{eyebrow_class}'>{dot_html}{badge_text} · {t_stat.upper()} · +{xp_reward} XP</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"<div class='task-title'>{t_titolo}</div>", unsafe_allow_html=True)

            col_spacer, col_menu = st.columns([5, 1])
            with col_menu:
                st.markdown('<div class="task-menu">', unsafe_allow_html=True)
                with st.popover("⋮", use_container_width=True):
                    st.markdown('<div class="btn-confirm-text">', unsafe_allow_html=True)
                    if st.button("✓  Completa", key=f"comp_{t_id}", use_container_width=True):
                        for item in data["tasks"]:
                            if item.get("id") == t_id:
                                item["completato"] = True
                        data["mission_stats"]["totale"] = data["mission_stats"].get("totale", 0) + 1
                        data["mission_stats"][cat_stat] = data["mission_stats"].get(cat_stat, 0) + 1
                        save_data(data)
                        aggiungi_xp(t_stat, xp_reward)
                        st.toast(f"Missione completata (+{xp_reward} XP in {t_stat.upper()})")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div class="btn-danger-text">', unsafe_allow_html=True)
                    if st.button("✕  Elimina", key=f"del_{t_id}", use_container_width=True):
                        data["tasks"] = [item for item in data["tasks"] if item.get("id") != t_id]
                        save_data(data)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

# --- RENDER TAB: PROFILO ---
elif st.session_state.active_tab == "profilo":
    st.title("Stato Operativo")

    rep_level = data['stats']['rep']['level']
    st.markdown(
        f"<div style='display:flex; justify-content:center; margin: 10px 0 28px 0;'>"
        f"{medaglione_html(rep_level, 0, 1, 'Reputazione', hero=True)}"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Statistiche")
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

    st.markdown("### Parametri Vitali")
    medaglioni_html = "<div class='medallions-row'>"
    for stat, label in [("disciplina", "Disciplina"), ("focus", "Focus"), ("skill", "Skill")]:
        info = data["stats"].get(stat, {"xp": 0, "level": 1, "last_active": str(date.today())})
        livello_attuale = info.get("level", 1)
        xp_attuali = info.get("xp", 0)
        prossimo_livello = 100 * livello_attuale
        medaglioni_html += medaglione_html(livello_attuale, xp_attuali, prossimo_livello, label)
    medaglioni_html += "</div>"
    st.markdown(medaglioni_html, unsafe_allow_html=True)

    st.markdown("### Traguardi")
    badge_list = [
        {"nome": "Efficienza Fiscale", "desc": "Risolvi 3 scadenze urgenti.", "sbloccato": m_stats.get("urgenti", 0) >= 3},
        {"nome": "Inarrestabile", "desc": "Porta a termine 10 task totali.", "sbloccato": m_stats.get("totale", 0) >= 10},
    ]

    for b in badge_list:
        css_class = "badge-unlocked" if b["sbloccato"] else "badge-locked"
        colore_desc = "#C9BFA6" if b["sbloccato"] else "#6E675A"
        st.markdown(
            f"<div class='{css_class}'><b>{b['nome']}</b><br>"
            f"<span style='color:{colore_desc};'>{b['desc']}</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("### Storico Missioni Completate")
    completati = [t for t in data.get("tasks", []) if t.get("completato", False)]
    if not completati:
        st.caption("Nessuna missione completata di recente.")
    else:
        for t in reversed(completati[-10:]):
            st.markdown(
                f"<div class='history-row'>{t.get('titolo')} "
                f"<span class='tag'>{t.get('stat', 'base').upper()}</span></div>",
                unsafe_allow_html=True
            )

# --- BARRA DI NAVIGAZIONE INFERIORE ---
st.markdown('<div class="fixed-bottom-nav"><div class="fixed-bottom-inner">', unsafe_allow_html=True)
nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    class_b = "nav-active" if st.session_state.active_tab == "bacheca" else ""
    st.markdown(f'<div class="{class_b}">', unsafe_allow_html=True)
    if st.button("Radar", use_container_width=True, key="nav_bacheca"):
        st.session_state.active_tab = "bacheca"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nav_col2:
    class_p = "nav-active" if st.session_state.active_tab == "profilo" else ""
    st.markdown(f'<div class="{class_p}">', unsafe_allow_html=True)
    if st.button("Stato", use_container_width=True, key="nav_profilo"):
        st.session_state.active_tab = "profilo"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
