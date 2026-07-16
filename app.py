import streamlit as st
import json
import os
from datetime import datetime, date

# --- CONFIGURAZIONE PAGINA STILE NEON ---
st.set_page_config(
    page_title="STREET_GUIDE.EXE",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STILI CSS PERSONALIZZATI (GTA / STREET STYLE) ---
st.markdown("""
<style>
    /* Sfondo scuro e font moderni */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    h1, h2, h3 {
        color: #66fcf1 !important; /* Ciano Neon */
        font-family: 'Courier New', Courier, monospace;
    }
    /* Pulsanti ed elementi interattivi */
    div.stButton > button {
        background-color: #1f2833;
        color: #66fcf1;
        border: 2px solid #45f3ff;
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #45f3ff;
        color: #0b0c10;
        box-shadow: 0 0 15px #45f3ff;
    }
    /* Badge e Box */
    .badge-unlocked {
        padding: 8px;
        background-color: #1f2833;
        border-left: 5px solid #ff007f; /* Rosa Neon */
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .badge-locked {
        padding: 8px;
        background-color: #121212;
        border-left: 5px solid #444;
        border-radius: 4px;
        margin-bottom: 10px;
        opacity: 0.6;
    }
</style>
""", unsafe_allow_html=True)

DB_FILE = "street_guide_db.json"

# --- FUNZIONI DATABASE ---
def load_data():
    if not os.path.exists(DB_FILE):
        # Stato iniziale
        return {
            "stats": {
                "fisico": {"xp": 100, "level": 1, "last_active": str(date.today())},
                "mente": {"xp": 100, "level": 1, "last_active": str(date.today())},
                "skill": {"xp": 100, "level": 1, "last_active": str(date.today())},
                "rep": {"xp": 100, "level": 1}
            },
            "tasks": [],
            "garage": [],
            "records": {},
            "bar_streak": 0,
            "last_bar_check": str(date.today())
        }
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Carica i dati
data = load_data()

# --- LOGICA DEL DECADIMENTO (LA RUGGINE) ---
def applica_decadimento(data):
    today = date.today()
    regole = {
        "fisico": {"giorni": 3, "tasso": 0.05},
        "mente": {"giorni": 4, "tasso": 0.04},
        "skill": {"giorni": 5, "tasso": 0.03}
    }
    modificato = False
    for stat_name, regola in regole.items():
        last_active_str = data["stats"][stat_name].get("last_active", str(today))
        last_active_date = datetime.strptime(last_active_str, "%Y-%m-%d").date()
        days_passed = (today - last_active_date).days
        
        if days_passed > regola["giorni"]:
            # Applica perdita giornaliera accumulata per i giorni oltre la grazia
            giorni_penalita = days_passed - regola["giorni"]
            perdita = int(data["stats"][stat_name]["xp"] * (regola["tasso"] * giorni_penalita))
            if perdita > 0:
                data["stats"][stat_name]["xp"] = max(10, data["stats"][stat_name]["xp"] - perdita)
                # Resetta l'ultimo giorno di decadimento a oggi per non accumularlo di continuo
                data["stats"][stat_name]["last_active"] = str(today)
                modificato = True
                st.warning(f"⚠️ La tua statistica {stat_name.upper()} sta perdendo smalto per inattività! (-{perdita} XP)")
    
    # Ricalcola la REP globale (media dei livelli delle tre statistiche)
    livelli = [data["stats"]["fisico"]["level"], data["stats"]["mente"]["level"], data["stats"]["skill"]["level"]]
    media_livelli = sum(livelli) // 3
    if data["stats"]["rep"]["level"] != media_livelli:
        data["stats"]["rep"]["level"] = max(1, media_livelli)
        modificato = True
        
    if modificato:
        save_data(data)

applica_decadimento(data)

# --- FUNZIONI DI SUPPORTO LIVELLI ---
def aggiungi_xp(stat, quantita):
    data["stats"][stat]["xp"] += quantita
    data["stats"][stat]["last_active"] = str(date.today())
    
    # Formula livello: 100 * Livello attuale = XP per il livello successivo
    xp_necessari = 100 * data["stats"][stat]["level"]
    if data["stats"][stat]["xp"] >= xp_necessari:
        data["stats"][stat]["level"] += 1
        data["stats"][stat]["xp"] -= xp_necessari
        st.balloons()
        st.success(f"⚡ LIVELLO SU! La statistica {stat.upper()} è salita al Livello {data['stats'][stat]['level']}!")
    
    # Aggiorna anche la barra globale di REP
    data["stats"]["rep"]["xp"] += int(quantita * 0.5)
    rep_necessari = 100 * data["stats"]["rep"]["level"]
    if data["stats"]["rep"]["xp"] >= rep_necessari:
        data["stats"]["rep"]["level"] += 1
        data["stats"]["rep"]["xp"] -= rep_necessari
        st.success(f"👑 RISPETTO +! La tua REP globale è salita al Livello {data['stats']['rep']['level']}!")
        
    save_data(data)

# --- INTERFACCIA UTENTE ---
st.title("⚡ PROJECT: STREET_GUIDE ⚡")

# Intestazione status globale
lvl_rep = data["stats"]["rep"]["level"]
xp_rep = data["stats"]["rep"]["xp"]
rep_next = 100 * lvl_rep
st.subheader(f"👑 REP GLOBALE: Livello {lvl_rep}")
st.progress(min(1.0, xp_rep / rep_next))

tab1, tab2, tab3 = st.tabs(["📋 BACHECA", "📊 STATUS & RECORD", "🚘 IL GARAGE"])

# --- TAB 1: BACHECA ---
with tab1:
    st.write("### I TUOI IMPEGNI IN CITTÀ")
    
    # Form aggiunta task
    with st.expander("➕ Inserisci un nuovo compito"):
        nuovo_titolo = st.text_input("Cosa devi fare?")
        tipo_task = st.selectbox("Importanza", ["I Grossi (Priorità)", "Lavoretti (Commissioni)"])
        stat_associata = st.selectbox("Statistica collegata", ["fisico", "mente", "skill"])
        if st.button("Pianifica Attività"):
            if nuovo_titolo:
                data["tasks"].append({
                    "id": len(data["tasks"]) + 1,
                    "titolo": nuovo_titolo,
                    "tipo": tipo_task,
                    "stat": stat_associata,
                    "completato": False
                })
                save_data(data)
                st.success(f"Attività '{nuovo_titolo}' aggiunta in bacheca!")
                st.rerun()

    # Mostra i compiti attivi
    grossi = [t for t in data["tasks"] if t["tipo"] == "I Grossi (Priorità)" and not t["completato"]]
    lavoretti = [t for t in data["tasks"] if t["tipo"] == "Lavoretti (Commissioni)" and not t["completato"]]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("#### 🎯 I Grossi (Priorità)")
        for idx, task in enumerate(grossi):
            if st.checkbox(f"🔴 {task['titolo']}", key=f"g_{task['id']}"):
                # Trova e marca completato
                for t in data["tasks"]:
                    if t["id"] == task["id"]:
                        t["completato"] = True
                aggiungi_xp(task["stat"], 35) # I grossi danno 35 XP
                st.rerun()
                
    with col2:
        st.write("#### 🔧 Lavoretti (Commissioni)")
        for idx, task in enumerate(lavoretti):
            if st.checkbox(f"⚪ {task['titolo']}", key=f"l_{task['id']}"):
                for t in data["tasks"]:
                    if t["id"] == task["id"]:
                        t["completato"] = True
                aggiungi_xp(task["stat"], 15) # I lavoretti danno 15 XP
                st.rerun()

    st.write("---")
    
    # Sezione speciale "Niente Bar"
    st.write("#### 🚭 Sotto i Radar (Sfida del Bar)")
    today_str = str(date.today())
    if data.get("last_bar_check") != today_str:
        st.info("Hai speso soldi al bar oggi?")
        col_bar1, col_bar2 = st.columns(2)
        with col_bar1:
            if st.button("No, sono rimasto pulito! 💸"):
                data["bar_streak"] += 1
                data["last_bar_check"] = today_str
                save_data(data)
                aggiungi_xp("mente", 15)  # Dà XP a mente per la disciplina
                st.success(f"Grande! Scia senza bar: {data['bar_streak']} giorni di fila! (+15 XP)")
                st.rerun()
        with col_bar2:
            if st.button("Sì, ho ceduto..."):
                data["bar_streak"] = 0
                data["last_bar_check"] = today_str
                save_data(data)
                st.warning("Scia azzerata. Riprenderai il controllo domani!")
                st.rerun()
    else:
        st.write(f"Scia attuale senza bar: **{data['bar_streak']}** giorni di fila. Torna domani per continuare la scia!")

# --- TAB 2: STATUS & RECORD ---
with tab2:
    st.write("### LE TUE STATISTICHE")
    
    for stat, info in data["stats"].items():
        if stat == "rep": continue
        st.write(f"**{stat.upper()}** (Lvl. {info['level']})")
        prossimo_livello = 100 * info['level']
        st.progress(min(1.0, info['xp'] / prossimo_livello))
        st.write(f"XP: {info['xp']}/{prossimo_livello} — *Ultima attività: {info['last_active']}*")
        st.write("")

    st.write("---")
    st.write("#### ⏱️ Cronometro e Record Personali")
    
    with st.form("add_record"):
        nome_attivita = st.text_input("Attività (es. Corsa 5km, Circuito fune):")
        nuovo_tempo = st.text_input("Tempo registrato (es: 22m 10s):")
        submit_record = st.form_submit_code = st.form_submit_button("Registra Tempo")
        if submit_record and nome_attivita and nuovo_tempo:
            data["records"][nome_attivita] = nuovo_tempo
            save_data(data)
            aggiungi_xp("fisico", 20)
            st.success(f"Nuovo tempo registrato per {nome_attivita}: {nuovo_tempo}! (+20 XP Fisico)")
            st.rerun()
            
    if data["records"]:
        for att, tempo in data["records"].items():
            st.write(f"⚡ **{att}**: `{tempo}`")

    st.write("---")
    st.write("#### 🏆 Sblocco Badge d'Onore")
    
    # Logica Badge (Semplice controllo sul database)
    badge_list = [
        {"nome": "Piede di Piombo", "desc": "Registra un record sul cronometro", "condizione": len(data["records"]) >= 1},
        {"nome": "Sotto i Radar", "desc": "Arriva a 5 giorni di fila senza bar", "condizione": data["bar_streak"] >= 5},
        {"nome": "Infiltrato Invisibile", "desc": "Arriva a 14 giorni di fila senza bar", "condizione": data["bar_streak"] >= 14},
    ]
    
    for b in badge_list:
        if b["condizione"]:
            st.markdown(f"<div class='badge-unlocked'>🏆 <b>{b['nome']}</b> (SBLOCCATO)<br><small>{b['desc']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='badge-locked'>🔒 <b>{b['nome']}</b> (BLOCCATO)<br><small>{b['desc']}</small></div>", unsafe_allow_html=True)

# --- TAB 3: IL GARAGE ---
with tab3:
    st.write("### IL GARAGE (I tuoi Obiettivi di Risparmio)")
    
    with st.expander("🚘 Aggiungi un nuovo pezzo al Garage"):
        oggetto = st.text_input("Nome dell'oggetto (es. Nuovo Sintetizzatore):")
        costo = st.number_input("Costo totale (€):", min_value=1)
        if st.button("Aggiungi Target"):
            if oggetto and costo:
                data["garage"].append({
                    "oggetto": oggetto,
                    "costo": costo,
                    "risparmiati": 0
                })
                save_data(data)
                st.success(f"Oggetto '{oggetto}' inserito in rimessa!")
                st.rerun()
                
    # Visualizza e finanzia obiettivi
    for idx, item in enumerate(data["garage"]):
        percentuale = min(1.0, item["risparmiati"] / item["costo"])
        st.write(f"#### {item['oggetto']} - {item['risparmiati']}€ / {item['costo']}€")
        st.progress(percentuale)
        
        # Gestione risparmi depositati
        col_dep1, col_dep2 = st.columns([2, 1])
        with col_dep1:
            deposito = st.number_input(f"Aggiungi risparmio a {item['oggetto']}", min_value=1, key=f"dep_val_{idx}")
        with col_dep2:
            if st.button("Deposita", key=f"dep_btn_{idx}"):
                item["risparmiati"] += deposito
                save_data(data)
                if item["risparmiati"] >= item["costo"]:
                    st.balloons()
                    st.success(f"MISSIONE COMPIUTA! Puoi acquistare {item['oggetto']}! 🍻")
                    aggiungi_xp("skill", 100) # Sblocca grossi XP quando completi l'obiettivo
                else:
                    aggiungi_xp("skill", 10) # Guadagni XP minori quando risparmi
                st.rerun()
