"""
Actividad Sera1 - World Cup 2026 Survivor Pool
================================================
12 players. 48 teams. One rule: survive.
"""

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Actividad Sera1", page_icon="🏆", layout="wide")

DATA_FILE = Path("game_data.json")

PLAYERS = ["Parrita", "Sirio", "Morsa", "Chuky", "Temo", "Jevu", "Pats", "Caborka", "Chirris", "Joe", "Tommy", "Buks"]

GROUPS = {
    "A": ["Mexico", "Colombia", "Ecuador", "Senegal"],
    "B": ["Portugal", "Iran", "Paraguay", "New Zealand"],
    "C": ["France", "Australia", "Indonesia", "UAE"],
    "D": ["Brazil", "Cameroon", "Albania", "Fiji"],
    "E": ["Argentina", "Peru", "Egypt", "Bahrain"],
    "F": ["Netherlands", "Canada", "Turkey", "Ivory Coast"],
    "G": ["Spain", "Bolivia", "Qatar", "Honduras"],
    "H": ["England", "Nigeria", "Chile", "Uzbekistan"],
    "I": ["Germany", "Uruguay", "USA", "Trinidad and Tobago"],
    "J": ["Italy", "South Korea", "Saudi Arabia", "Kenya"],
    "K": ["Belgium", "Japan", "Scotland", "Panama"],
    "L": ["Croatia", "Serbia", "Morocco", "Denmark"],
}

ALL_TEAMS = sorted([team for group in GROUPS.values() for team in group])
STAGES = ["group", "r32", "r16", "qf", "sf", "final", "complete"]
STAGE_NAMES = {
    "group": "Fase de Grupos", "r32": "Octavos de Final", "r16": "Octavos",
    "qf": "Cuartos de Final", "sf": "Semifinales", "final": "Final", "complete": "Torneo Terminado",
}
STAGE_EMOJI = {
    "group": "🏟️", "r32": "⚔️", "r16": "🔥", "qf": "💪", "sf": "🏆", "final": "👑", "complete": "🎉",
}

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    # Initialize with all 12 players
    players = {name: {"picks": {}, "eliminated": False} for name in PLAYERS}
    return {
        "players": players,
        "stage": "group",
        "eliminated_teams": [],
        "advanced_teams": [],
        "admin_password": "sera1admin",
    }

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

data = load_data()

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main .block-container { max-width: 1100px; padding-top: 0.5rem; }
    
    /* Header */
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3.5rem;
        color: #ffffff;
        text-align: center;
        background: linear-gradient(135deg, #1a472a 0%, #2d8544 50%, #ce1126 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    .hero-subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    
    /* Stage badge */
    .stage-badge {
        background: linear-gradient(135deg, #ffd700, #ffaa00);
        color: #1a1a1a;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        text-align: center;
        margin: 0 auto;
        box-shadow: 0 2px 8px rgba(255,170,0,0.3);
    }
    
    /* Player cards */
    .player-alive {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        margin: 0.3rem;
        font-weight: 600;
    }
    .player-dead {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        margin: 0.3rem;
        font-weight: 600;
        text-decoration: line-through;
        opacity: 0.7;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: #f8f9fa; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 600; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: #1a472a !important; color: white !important; }
    
    /* Buttons */
    .stButton > button { border-radius: 8px !important; font-weight: 600 !important; }
    
    /* Group cards */
    .group-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .group-card h4 { margin: 0 0 0.3rem 0; color: #1a472a; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="hero-title">🏆 ACTIVIDAD SERA1 🏆</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">World Cup 2026 Survivor Pool | 12 Jugadores | El que sobrevive, gana</div>', unsafe_allow_html=True)

# Stage indicator
stage_text = f"{STAGE_EMOJI[data['stage']]} {STAGE_NAMES[data['stage']]}"
alive_count = sum(1 for p in data["players"].values() if not p.get("eliminated"))
st.markdown(f'<div style="text-align:center"><span class="stage-badge">{stage_text} | Vivos: {alive_count}/12</span></div>', unsafe_allow_html=True)
st.markdown("")

# --- Player status bar ---
cols = st.columns(12)
for i, (name, info) in enumerate(data["players"].items()):
    with cols[i]:
        if info.get("eliminated"):
            st.markdown(f'<div class="player-dead">💀<br>{name}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="player-alive">⚽<br>{name}</div>', unsafe_allow_html=True)

st.markdown("---")

# --- Tabs ---
tab_play, tab_standings, tab_groups, tab_admin = st.tabs(["⚽ Jugar", "📊 Tabla", "🌍 Grupos", "🔧 Admin"])

with tab_play:
    if data["stage"] == "complete":
        winners = [n for n, info in data["players"].items() if not info.get("eliminated")]
        if winners:
            st.balloons()
            st.success(f"🏆 GANADOR(ES): {', '.join(winners)}")
        else:
            st.info("Nadie sobrevivio. El dinero se queda en la mesa.")
    else:
        player_name = st.selectbox("¿Quien eres?", ["-- Selecciona tu nombre --"] + PLAYERS, key="play_select")
        
        if player_name and player_name != "-- Selecciona tu nombre --":
            player = data["players"][player_name]
            
            if player.get("eliminated"):
                st.error(f"💀 Lo siento {player_name}, estas eliminado.")
                st.caption(f"Razon: {player.get('elimination_reason', '')}")
            else:
                picks = player.get("picks", {})
                used_teams = set()
                for v in picks.values():
                    if isinstance(v, list): used_teams.update(v)
                    elif v: used_teams.add(v)
                
                if data["stage"] == "group":
                    st.subheader("🏟️ Fase de Grupos")
                    st.write("Escoge **4 equipos**. Si alguno no avanza de fase de grupos, estas fuera.")
                    current_pick = picks.get("group", [])
                    
                    if current_pick:
                        st.success(f"✅ Tus picks: **{', '.join(current_pick)}**")
                        st.caption("Tus picks estan bloqueados. Buena suerte!")
                    else:
                        available = [t for t in ALL_TEAMS if t not in used_teams]
                        selected = st.multiselect("Selecciona exactamente 4 equipos:", available, max_selections=4)
                        
                        if len(selected) == 4:
                            st.warning(f"Vas a lockear: **{', '.join(selected)}**. No hay vuelta atras.")
                            if st.button("🔒 Confirmar Picks", type="primary"):
                                data["players"][player_name]["picks"]["group"] = selected
                                save_data(data)
                                st.rerun()
                        elif selected:
                            st.info(f"Faltan {4 - len(selected)} equipo(s)")
                
                elif data["stage"] in ["r32", "r16", "qf", "sf", "final"]:
                    st.subheader(f"{STAGE_EMOJI[data['stage']]} {STAGE_NAMES[data['stage']]}")
                    st.write("Escoge **1 equipo**. Si pierde, estas fuera.")
                    current_pick = picks.get(data["stage"])
                    
                    if current_pick:
                        st.success(f"✅ Tu pick: **{current_pick}**")
                    else:
                        available = [t for t in data.get("advanced_teams", ALL_TEAMS) if t not in used_teams]
                        if available:
                            selected = st.selectbox("Escoge tu equipo:", ["-- Escoge --"] + available)
                            if selected != "-- Escoge --":
                                st.warning(f"Vas a lockear: **{selected}**")
                                if st.button("🔒 Confirmar Pick", type="primary"):
                                    data["players"][player_name]["picks"][data["stage"]] = selected
                                    save_data(data)
                                    st.rerun()
                        else:
                            st.error("No tienes equipos disponibles!")

with tab_standings:
    st.subheader("📊 Tabla de Posiciones")
    
    alive, dead = [], []
    for name, info in data["players"].items():
        p = info.get("picks", {})
        if info.get("eliminated"):
            dead.append({"Jugador": name, "Grupos": ", ".join(p.get("group", [])), 
                        "Razon": info.get("elimination_reason", "")})
        else:
            alive.append({"Jugador": name, "Grupos": ", ".join(p.get("group", [])),
                         "R32": p.get("r32", ""), "R16": p.get("r16", ""),
                         "QF": p.get("qf", ""), "SF": p.get("sf", ""), "Final": p.get("final", "")})
    
    if alive:
        st.markdown(f"### 🟢 Vivos ({len(alive)})")
        st.dataframe(alive, use_container_width=True, hide_index=True)
    if dead:
        st.markdown(f"### 🔴 Eliminados ({len(dead)})")
        st.dataframe(dead, use_container_width=True, hide_index=True)

with tab_groups:
    st.subheader("🌍 Grupos del Mundial 2026")
    cols = st.columns(3)
    for i, (g, teams) in enumerate(GROUPS.items()):
        with cols[i % 3]:
            team_list = "".join([f"<br>{'⚽' if t in data.get('advanced_teams', ALL_TEAMS) else '❌'} {t}" for t in teams])
            st.markdown(f'<div class="group-card"><h4>Grupo {g}</h4>{team_list}</div>', unsafe_allow_html=True)

with tab_admin:
    st.subheader("🔧 Panel de Admin (Solo Parrita)")
    pw = st.text_input("Contrasena:", type="password")
    
    if pw == data["admin_password"]:
        st.success("Acceso concedido")
        st.write(f"**Etapa actual:** {STAGE_NAMES[data['stage']]}")
        
        if data["stage"] == "group":
            st.markdown("### Finalizar Fase de Grupos")
            st.write("Marca los equipos que **NO avanzaron**:")
            eliminated = st.multiselect("Equipos eliminados:", ALL_TEAMS)
            if st.button("✅ Finalizar Grupos", type="primary"):
                data["eliminated_teams"] = eliminated
                data["advanced_teams"] = [t for t in ALL_TEAMS if t not in eliminated]
                for name, info in data["players"].items():
                    failed = [t for t in info.get("picks", {}).get("group", []) if t in eliminated]
                    if failed:
                        data["players"][name]["eliminated"] = True
                        data["players"][name]["elimination_reason"] = f"No avanzaron: {', '.join(failed)}"
                data["stage"] = "r32"
                save_data(data)
                st.rerun()
        
        elif data["stage"] in ["r32", "r16", "qf", "sf", "final"]:
            st.markdown(f"### Finalizar {STAGE_NAMES[data['stage']]}")
            st.write("Marca los equipos que **perdieron** esta ronda:")
            lost = st.multiselect("Equipos que perdieron:", data.get("advanced_teams", []))
            if st.button(f"✅ Finalizar {STAGE_NAMES[data['stage']]}", type="primary"):
                data["advanced_teams"] = [t for t in data.get("advanced_teams", []) if t not in lost]
                for name, info in data["players"].items():
                    if info.get("eliminated"): continue
                    pick = info.get("picks", {}).get(data["stage"])
                    if pick in lost:
                        data["players"][name]["eliminated"] = True
                        data["players"][name]["elimination_reason"] = f"{pick} perdio en {STAGE_NAMES[data['stage']]}"
                data["stage"] = STAGES[STAGES.index(data["stage"]) + 1]
                save_data(data)
                st.rerun()
        
        st.markdown("---")
        if st.button("🗑️ Resetear Todo"):
            DATA_FILE.unlink(missing_ok=True)
            st.rerun()
    elif pw:
        st.error("Contrasena incorrecta")
