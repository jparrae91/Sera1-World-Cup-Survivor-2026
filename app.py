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
    "A": ["Mexico", "South Korea", "Czechia", "South Africa"],
    "B": ["Canada", "Switzerland", "Qatar", "Bosnia-Herzegovina"],
    "C": ["Brazil", "Morocco", "Scotland", "Haiti"],
    "D": ["USA", "Australia", "Paraguay", "Turkiye"],
    "E": ["Germany", "Ecuador", "Ivory Coast", "Curacao"],
    "F": ["Netherlands", "Japan", "Tunisia", "Sweden"],
    "G": ["Belgium", "Iran", "Egypt", "New Zealand"],
    "H": ["Spain", "Uruguay", "Saudi Arabia", "Cape Verde"],
    "I": ["France", "Senegal", "Norway", "Iraq"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Colombia", "Uzbekistan", "DR Congo"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
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
PICKS_PER_STAGE = {
    "group": 4, "r32": 2, "r16": 1, "qf": 1, "sf": 1, "final": 1,
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
        "picks_locked": False,
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
                
                # Check if picks are locked
                if data.get("picks_locked") and not picks.get(data["stage"]):
                    st.warning("🔒 Los picks estan bloqueados por el admin. Ya no se pueden hacer selecciones para esta ronda.")
                elif data["stage"] == "group":
                    st.subheader("🏟️ Fase de Grupos")
                    st.write("Escoge **4 equipos**. Si alguno no avanza de fase de grupos, estas fuera.")
                    current_pick = picks.get("group", [])
                    available = [t for t in ALL_TEAMS if t not in used_teams or t in (current_pick if isinstance(current_pick, list) else [])]
                    
                    if data.get("picks_locked") and current_pick:
                        st.success(f"✅ Tus picks (bloqueados): **{', '.join(current_pick)}**")
                    else:
                        default = current_pick if current_pick else []
                        selected = st.multiselect("Selecciona exactamente 4 equipos:", ALL_TEAMS, default=default, max_selections=4)
                        
                        if len(selected) == 4:
                            if selected != current_pick:
                                if st.button("� Guardar Picks", type="primary"):
                                    data["players"][player_name]["picks"]["group"] = selected
                                    save_data(data)
                                    st.success(f"✅ Guardado: **{', '.join(selected)}**")
                                    st.rerun()
                            else:
                                st.success(f"✅ Tus picks: **{', '.join(selected)}**")
                                st.caption("Puedes cambiarlos hasta que el admin bloquee los picks.")
                        elif selected:
                            st.info(f"Faltan {4 - len(selected)} equipo(s)")
                
                elif data["stage"] in ["r32", "r16", "qf", "sf", "final"]:
                    num_picks = PICKS_PER_STAGE[data["stage"]]
                    st.subheader(f"{STAGE_EMOJI[data['stage']]} {STAGE_NAMES[data['stage']]}")
                    st.write(f"Escoge **{num_picks} equipo(s)**. Si alguno pierde, estas fuera.")
                    current_pick = picks.get(data["stage"], [])
                    # Normalize to list
                    if isinstance(current_pick, str):
                        current_pick = [current_pick] if current_pick else []
                    
                    # Available = advanced teams minus used (but allow current picks to show)
                    used_minus_current = used_teams - set(current_pick)
                    available = [t for t in data.get("advanced_teams", ALL_TEAMS) if t not in used_minus_current]
                    
                    if data.get("picks_locked") and current_pick:
                        st.success(f"✅ Tu(s) pick(s) (bloqueados): **{', '.join(current_pick)}**")
                    else:
                        if num_picks == 1:
                            default_idx = available.index(current_pick[0]) + 1 if current_pick and current_pick[0] in available else 0
                            selected = st.selectbox("Escoge tu equipo:", ["-- Escoge --"] + available, index=default_idx)
                            selected_list = [selected] if selected != "-- Escoge --" else []
                        else:
                            default = [t for t in current_pick if t in available]
                            selected_list = st.multiselect(f"Selecciona {num_picks} equipos:", available, default=default, max_selections=num_picks)
                        
                        if len(selected_list) == num_picks:
                            if selected_list != current_pick:
                                if st.button("� Guardar Pick(s)", type="primary"):
                                    data["players"][player_name]["picks"][data["stage"]] = selected_list if num_picks > 1 else selected_list[0]
                                    save_data(data)
                                    st.success(f"✅ Guardado: **{', '.join(selected_list)}**")
                                    st.rerun()
                            else:
                                st.success(f"✅ Tu(s) pick(s): **{', '.join(selected_list)}**")
                                st.caption("Puedes cambiarlos hasta que el admin bloquee los picks.")

with tab_standings:
    st.subheader("📊 Tabla de Posiciones")
    
    alive, dead = [], []
    for name, info in data["players"].items():
        p = info.get("picks", {})
        if info.get("eliminated"):
            dead.append({"Jugador": name, "Grupos": ", ".join(p.get("group", [])), 
                        "Razon": info.get("elimination_reason", "")})
        else:
            r32_pick = p.get("r32", [])
            if isinstance(r32_pick, list): r32_pick = ", ".join(r32_pick)
            alive.append({"Jugador": name, "Grupos": ", ".join(p.get("group", [])),
                         "R32": r32_pick, "R16": p.get("r16", ""),
                         "QF": p.get("qf", ""), "SF": p.get("sf", ""), "Final": p.get("final", "")})
    
    if alive:
        st.markdown(f"### 🟢 Vivos ({len(alive)})")
        st.dataframe(alive, use_container_width=True, hide_index=True)
    if dead:
        st.markdown(f"### 🔴 Eliminados ({len(dead)})")
        st.dataframe(dead, use_container_width=True, hide_index=True)

with tab_groups:
    st.subheader("📜 Reglas del Juego")
    st.markdown("""
    ### Como funciona Actividad Sera1
    
    **Objetivo:** Sobrevivir todas las rondas del Mundial. Los que sobrevivan al final se dividen el pozo.
    
    ---
    
    **Fase de Grupos:**
    - Cada jugador escoge **4 equipos**.
    - Si **cualquiera** de esos 4 equipos no avanza a la siguiente ronda, el jugador queda **eliminado**.
    
    **Octavos de Final (R32):**
    - Cada jugador sobreviviente escoge **2 equipos**.
    - Si cualquiera de esos 2 pierde, el jugador queda eliminado.
    
    **Round of 16, Cuartos, Semifinales y Final:**
    - Cada jugador sobreviviente escoge **1 equipo** por ronda.
    - Si ese equipo pierde, el jugador queda eliminado.
    
    ---
    
    ### Reglas importantes
    
    1. **No se puede repetir equipo.** Una vez que usas un equipo en cualquier ronda, no lo puedes volver a usar en rondas futuras.
    2. **Puedes cambiar tus picks** cuantas veces quieras HASTA que el admin (Parrita) bloquee las selecciones. Una vez bloqueadas, no hay cambios.
    3. **Si sobreviven multiples jugadores** hasta el final, se dividen el pozo.
    4. **Si todos mueren** en la misma ronda, el dinero se queda en la mesa (o se define entre los sobrevivientes de la ronda anterior).
    
    ---
    
    | Ronda | Equipos a escoger | Regla de eliminacion |
    |-------|-------------------|---------------------|
    | Fase de Grupos | 4 | Si alguno no avanza, estas fuera |
    | Octavos (R32) | 2 | Si alguno pierde, estas fuera |
    | R16 | 1 | Si pierde, estas fuera |
    | Cuartos | 1 | Si pierde, estas fuera |
    | Semifinales | 1 | Si pierde, estas fuera |
    | Final | 1 | Si pierde, estas fuera |
    
    ---
    
    **Tip estrategico:** No quemes a tus mejores equipos en fase de grupos. Los vas a necesitar en las rondas eliminatorias donde solo puedes escoger 1.
    """)
    
    st.markdown("---")
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
        
        # Lock/Unlock picks
        st.markdown("### Bloquear Picks")
        locked = data.get("picks_locked", False)
        if locked:
            st.error("🔒 Picks BLOQUEADOS — nadie puede hacer selecciones")
            if st.button("🔓 Desbloquear Picks"):
                data["picks_locked"] = False
                save_data(data)
                st.rerun()
        else:
            st.success("🔓 Picks ABIERTOS — jugadores pueden seleccionar")
            if st.button("🔒 Bloquear Picks (no mas selecciones)"):
                data["picks_locked"] = True
                save_data(data)
                st.rerun()
        
        st.markdown("---")
        
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
                data["picks_locked"] = False
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
                    if isinstance(pick, list):
                        failed = [t for t in pick if t in lost]
                        if failed:
                            data["players"][name]["eliminated"] = True
                            data["players"][name]["elimination_reason"] = f"{', '.join(failed)} perdio en {STAGE_NAMES[data['stage']]}"
                    elif pick and pick in lost:
                        data["players"][name]["eliminated"] = True
                        data["players"][name]["elimination_reason"] = f"{pick} perdio en {STAGE_NAMES[data['stage']]}"
                data["stage"] = STAGES[STAGES.index(data["stage"]) + 1]
                data["picks_locked"] = False
                save_data(data)
                st.rerun()
        
        st.markdown("---")
        if st.button("🗑️ Resetear Todo"):
            DATA_FILE.unlink(missing_ok=True)
            st.rerun()
    elif pw:
        st.error("Contrasena incorrecta")
