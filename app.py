import streamlit as st
import json
import os
from datetime import datetime, date

# --- CONFIGURAZIONE PAGINA BYPASS ---
st.set_page_config(
    page_title="BYPASS.EXE",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- NUOVO STILE CSS FLUIDO & MORBIDO (SMOOTH NEON STREET) ---
st.markdown("""
<style>
    /* Font globale più pulito e moderno */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sfondo principale con leggero gradiente profondo */
    .stApp {
        background: linear-gradient(135deg, #08090c 0%, #11131a 100%);
        color: #e0e2ec;
    }
    
    /* Sidebar personalizzata e morbida */
    section[data-testid="stSidebar"] {
        background-color: #0d0f17 !important;
        border-right: 1px solid rgba(255, 42, 109, 0.15);
    }
    
    /* Titoli ed Intestazioni: Font Mono con bagliore neon morbido */
    h1, h2, h3 {
        font-family: 'JetBrains Mono', monospace !important;
        color: #ff2a6d !important; /* Rosa Neon Morbido */
        text-shadow: 0 0 15px rgba(255, 42, 109, 0.4);
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    h4, h5 {
        font-family: 'JetBrains Mono', monospace !important;
        color: #05d9e8 !important; /* Ciano Elettrico */
        font-weight: 700 !important;
    }

    /* Form ed Expander trasparenti tipo vetro (Glassmorphism) */
    div[data-testid="stExpander"], div[data-testid="stForm"] {
        background: rgba(20, 22, 34, 0.6) !important;
        border: 1px solid rgba(5, 217, 232, 0.2) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(8px);
        padding: 10px;
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="stExpander"]:hover {
        border-color: rgba(5, 217, 232, 0.5) !important;
        box-shadow: 0 8px 32px 0 rgba(5, 217, 232, 0.15) !important;
    }

    /* Pulsanti ultra-fluidi con bagliore ed effetto sollevamento */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(90deg, #161a26 0%, #1f2438 100%);
        color: #05d9e8;
        border: 1px solid #05d9e8;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(90deg, #05d9e8 0%, #03b6c2 100%);
        color: #08090c;
        border-color: #05d9e8;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(5, 217, 232, 0.4);
    }
    div.stButton > button:active {
        transform: translateY(0px);
    }

    /* Campi di input e selezione più dolci */
    .stTextInput input, .stSelectbox div div, .stNumberInput input {
        background-color: #121520 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus {
        border-color: #ff2a6d !important;
        box-shadow: 0 0 10px rgba(255, 42, 109, 0.3) !important;
    }

    /* Barre di avanzamento (Progress Bar) luminescenti */
    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #ff2a6d 0%, #05d9e8 100%) !important;
        box-shadow: 0 0 12px rgba(255, 42, 109, 0.5);
        border-radius: 10px;
    }

    /* Card Badge e Notifiche con transizione morbida */
    .badge-unlocked {
        padding: 14px 18px;
        background: linear-gradient(135deg, rgba(255, 42, 109, 0.15) 0%, rgba(20, 22, 34, 0.8) 100%);
        border: 1px solid rgba(255, 42, 109, 0.4);
        border-left: 6px solid #ff2a6d;
        border-radius: 12px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .badge-unlocked:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(255, 42, 109, 0.25);
    }
    .badge-locked {
        padding: 14px 18px;
        background: rgba(15, 17, 25, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 6px solid #333645;
        border-radius: 12px;
        margin-bottom: 12px;
        opacity: 0.45;
        transition: opacity 0.2s ease;
    }
    .badge-locked:hover {
        opacity: 0.7;
    }
    
    /* Nascondi elementi di sistema inutili per pulizia visiva */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
            "tasks": [],
            "records": {},
            "garage": [],
            "bar_streak": 0,
            "last_bar_check": str(date.today())
        }
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
            if "records" not in db: db["records"] = {}
            if "garage" not in db: db["garage"] = []
            if "bar_streak" not in db: db["bar_streak"] = 0
            if "last_bar_check" not in db: db["last_bar_check"] = str(date.today())
            return db
    except Exception:
        return {
            "stats": {
                "fisico": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "mente": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "skill": {"xp": 0, "level": 1, "last_active": str(date.today())},
                "rep": {"xp": 0, "level": 1}
            },
            "tasks": [],
            "records": {},
            "garage": [],
            "bar_streak": 0,
            "last_bar_check": str(date.today())
        }

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def aggiungi_xp(stat, quantita):
    if stat not in data["stats"]:
        data["stats"][stat] = {"xp": 0, "level": 1, "last_active": str(date.today())}
    
    data["stats"][stat]["xp"] += quantita
    data["stats"][stat]["last_active"] = str(date.today())
    
    xp_necessari = 100 * data["stats"][stat]["level"]
    if data["stats"][stat]["xp"] >= xp_necessari:
        data["stats"][stat]["level"] += 1
        data["stats"][stat]["xp"] -= xp_necessari
        st.toast(f"⚡ SKILL UP: {stat.upper()} sale al Livello {data['stats'][stat]['level']}!", icon="🆙")
        
    livelli = [
        data["stats"].get("fisico", {}).get("level", 1),
        data["stats"].get("mente", {}).get("level", 1),
        data["stats"].get("skill", {}).get("level", 1)
    ]
    media_livelli = sum(livelli) // 3
    data["stats"]["rep"]["level"] = max(1, media_livelli)
    
    save_data(data)

# --- MENU DI NAVIGAZIONE NELLA SIDEBAR ---
st.sidebar.title("⚡ BYPASS")
st.sidebar.caption("SISTEMA DI CONTROLLO ROUTINE")
st.sidebar.write("---")

scelta_menu = st.sidebar.radio(
    "NAVIGAZIONE SYSTEM:",
    ["📋 BACHECA MISSIONI", "👤 PROFILO & STATS", "🚘 GARAGE & RISPARMI"],
    label_visibility="collapsed"
)

st.sidebar.write("---")
st.sidebar.markdown(f"### 👑 REP GLOBALE: `Lvl. {data['stats']['rep']['level']}`")
st.sidebar.progress(min(1.0, (data['stats']['rep'].get('xp', 0)) / (100 * max(1, data['stats']['rep']['level']))))
st.sidebar.caption("Completa missioni per espandere il tuo impero.")

# --- SEZIONE 1: BACHECA ---
if scelta_menu == "📋 BACHECA MISSIONI":
    st.title("⚡ BYPASS")
    st.markdown("#### `SOVRASCRIVI LA ROUTINE. PRENDI IL CONTROLLO.`")
    st.write("")

    # Inserimento Missione
    with st.expander("➕ APRI TERMINALE: AGGIUNGI MISSIONE", expanded=False):
        with st.form("new_mission_form", clear_on_submit=True):
            titolo = st.text_input("Nome della Missione (es. Pagare multa, Allenamento gambe)")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                tipo = st.selectbox("Tipologia", ["Scadenza URGENTE", "I Grossi (Priorità)", "Lavoretti (Secondari)"])
            with col_f2:
                stat = st.selectbox("Statistica potenziata", ["fisico", "mente", "skill"])
            
            scadenza = None
            if tipo == "Scadenza URGENTE":
                scadenza = st.date_input("Scade il:", min_value=date.today())
                
            submit = st.form_submit_button("🔥 REGISTRA NEI SISTEMI")
            
            if submit and titolo:
                nuova_missione = {
                    "id": len(data.get("tasks", [])) + 1,
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
                st.toast(f"Missione '{titolo}' caricata nei sistemi!", icon="🚀")
                st.rerun()

    # Mostra attività attive
    st.write("---")
    st.markdown("### 📋 MISSIONI ATTIVE")
    all_tasks = data.get("tasks", [])
    attive = [t for t in all_tasks if not t.get("completato", False)]

    if not attive:
        st.info("⚡ Nessuna missione attiva. Il sistema è pulito. Sei libero o è il momento di pianificare un nuovo colpo?")
    else:
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
                        label = f"⚠️ [SCADE OGGI/DOMANI] — {t_titolo}"
                    else:
                        label = f"⏳ [TRA {giorni_rimasti} GG] — {t_titolo}"
                except Exception:
                    label = f"⏳ [SCADENZA] — {t_titolo}"
                xp_reward = 40
            elif t_tipo == "I Grossi (Priorità)":
                label = f"🔴 [PRIORITÀ] — {t_titolo}"
                xp_reward = 30
            else:
                label = f"⚪ [LAVORETTO] — {t_titolo}"
                xp_reward = 15
                
            if st.checkbox(label, key=f"task_{t_id}"):
                for t in data["tasks"]:
                    if t.get("id") == t_id:
                        t["completato"] = True
                save_data(data)
                aggiungi_xp(t_stat, xp_reward)
                st.toast(f"Completato! +{xp_reward} XP in {t_stat.upper()}", icon="⚡")
                st.rerun()

# --- SEZIONE 2: PROFILO & STATISTICHE ---
elif scelta_menu == "👤 PROFILO & STATS":
    st.title("👤 PROFILO UTENTE")
    st.markdown(f"#### STATUS GENERALE: `Livello {data['stats']['rep']['level']}`")
    st.write("---")
    
    st.markdown("### 📊 PARAMETRI FISICI & MENTALI")
    for stat in ["fisico", "mente", "skill"]:
        info = data["stats"].get(stat, {"xp": 0, "level": 1, "last_active": str(date.today())})
        livello_attuale = info.get("level", 1)
        xp_attuali = info.get("xp", 0)
        prossimo_livello = 100 * livello_attuale
        
        st.markdown(f"**{stat.upper()}** — `Livello {livello_attuale}`")
        st.progress(min(1.0, xp_attuali / prossimo_livello))
        st.caption(f"Esperienza: {xp_attuali}/{prossimo_livello} XP | Ultima attività: {info.get('last_active')}")
        st.write("")

    st.write("---")
    st.markdown("### ⏱️ CRONOMETRO & RECORD")
    
    with st.form("add_record_form"):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            nome_att = st.text_input("Esercizio (es. Corsa 5km, Circuito):")
        with col_r2:
            tempo_att = st.text_input("Tempo/Risultato (es. 21m 15s):")
        submit_rec = st.form_submit_button("⚡ REGISTRA NUOVO RECORD")
        if submit_rec and nome_att and tempo_att:
            data["records"][nome_att] = tempo_att
            save_data(data)
            aggiungi_xp("fisico", 20)
            st.toast(f"Nuovo record per {nome_att}! (+20 XP FISICO)", icon="🏆")
            st.rerun()
            
    if data["records"]:
        for att, temp in data["records"].items():
            st.markdown(f"⚡ **{att}**: `{temp}`")
    else:
        st.info("Nessun record registrato. Fai partire il cronometro e supera i tuoi limiti!")

    st.write("---")
    st.markdown("### 🏆 BACHECA TROFEI")
    
    streak = data.get("bar_streak", 0)
    badge_list = [
        {"nome": "Piede di Piombo", "desc": "Inserisci il tuo primo record personale sul cronometro.", "sbloccato": len(data["records"]) >= 1},
        {"nome": "Sotto i Radar", "desc": "Mantieni una scia di disciplina senza bar di 5 giorni.", "sbloccato": streak >= 5},
        {"nome": "Infiltrato Invisibile", "desc": "Raggiungi 14 giorni di fila senza micro-spese superflue.", "sbloccato": streak >= 14},
    ]
    
    for b in badge_list:
        if b["sbloccato"]:
            st.markdown(f"<div class='badge-unlocked'>👑 <b>{b['nome']}</b> (ATTIVO)<br><small style='color: #a0a6b8;'>{b['desc']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='badge-locked'>🔒 <b>{b['nome']}</b> (BLOCCATO)<br><small style='color: #606678;'>{b['desc']}</small></div>", unsafe_allow_html=True)

# --- SEZIONE 3: GARAGE & RISPARMI ---
elif scelta_menu == "🚘 GARAGE & RISPARMI":
    st.title("🚘 IL GARAGE")
    st.markdown("#### `GESTISCI I TUOI INVESTIMENTI E ACCUMULA CAPITALE.`")
    st.write("---")
    
    st.markdown("### 🚭 Sotto i Radar (Sfida del Bar)")
    today_str = str(date.today())
    last_check = data.get("last_bar_check", "")
    
    if last_check != today_str:
        st.info("⚡ Hai resistito alla tentazione di spendere soldi al bar oggi?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("SÌ, SONO RIMASTO PULITO! 💸"):
                data["bar_streak"] += 1
                data["last_bar_check"] = today_str
                save_data(data)
                aggiungi_xp("mente", 15)
                st.toast("Ottima disciplina! Scia prolungata.", icon="🔥")
                st.rerun()
        with col2:
            if st.button("NO, HO SPESO SOLDI."):
                data["bar_streak"] = 0
                data["last_bar_check"] = today_str
                save_data(data)
                st.toast("Scia azzerata. Riprenderai il controllo domani.", icon="⚠️")
                st.rerun()
    else:
        st.markdown(f"🔥 **Scia attuale senza bar:** `{data['bar_streak']} giorni di fila`")
        st.caption("Controllo giornaliero completato. Torna domani per continuare a incrementare la scia e fare XP.")
        
    st.write("---")
    st.markdown("### 📦 OBIETTIVI DI ACQUISTO")
    
    with st.expander("➕ AGGIUNGI OBIETTIVO ALLA RIMESSA", expanded=False):
        with st.form("new_garage_item"):
            col_g1, col_g2 = st.columns([2, 1])
            with col_g1:
                oggetto = st.text_input("Nome dell'oggetto / Traguardo:")
            with col_g2:
                costo = st.number_input("Budget necessario (€):", min_value=1)
            submit_item = st.form_submit_button("🔥 METTI IN CODA NEL GARAGE")
            if submit_item and oggetto and costo:
                data["garage"].append({
                    "oggetto": oggetto,
                    "costo": costo,
                    "risparmiati": 0
                })
                save_data(data)
                st.toast(f"'{oggetto}' inserito nel garage!", icon="🚘")
                st.rerun()
                
    if not data["garage"]:
        st.info("🚘 Nessun obiettivo di acquisto presente nel garage. Metti in coda il tuo primo target!")
    else:
        for idx, item in enumerate(data["garage"]):
            costo_tot = item["costo"]
            risp = item["risparmiati"]
            percentuale = min(1.0, risp / costo_tot)
            
            st.markdown(f"##### 📦 {item['oggetto']} — `{risp}€` su `{costo_tot}€`")
            st.progress(percentuale)
            
            col_dep1, col_dep2 = st.columns([2, 1])
            with col_dep1:
                deposito = st.number_input(f"Quota da depositare (€):", min_value=1, key=f"dep_val_{idx}")
            with col_dep2:
                st.write("") # Spaziatore per allineare il bottone all'input
                if st.button("DEPOSITA", key=f"dep_btn_{idx}"):
                    item["risparmiati"] += deposito
                    save_data(data)
                    if item["risparmiati"] >= item["costo"]:
                        st.balloons()
                        st.success(f"🔥 TARGET RAGGIUNTO! Hai i fondi necessari per acquistare {item['oggetto']}!")
                        aggiungi_xp("skill", 100)
                    else:
                        aggiungi_xp("skill", 10)
                    st.rerun()
            st.write("---")
