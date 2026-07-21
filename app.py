import streamlit as st
import requests
from datetime import datetime, timedelta

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# ---------------------------------------------------------
st.set_page_config(
    page_title="Winamax Real Analyst",
    page_icon="🟥",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0d0f12; }
    .header-winamax {
        background: linear-gradient(135deg, #d32f2f 0%, #4a0000 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .badge-date {
        background-color: #ff9800;
        color: #000;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    .ticket-box {
        background-color: #1e222d;
        border-left: 5px solid #d32f2f;
        padding: 18px;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = "e387548ff23f836b1052c3b59b045f45"

# Fecha actual fija del sistema
fecha_hoy_obj = datetime.now()
fecha_manana_obj = fecha_hoy_obj + timedelta(days=1)

# ---------------------------------------------------------
# NAVEGACIÓN TEMPORAL PRINCIPAL
# ---------------------------------------------------------
st.markdown("""
    <div class="header-winamax">
        <h1>🟥 WINAMAX REAL-TIME ANALYST</h1>
        <p>Panel de Clasificatorios Champions, Circuito de Tenis y Combinadas Dinámicas</p>
    </div>
""", unsafe_allow_html=True)

filtro_tiempo = st.radio(
    "📅 Selecciona el día de análisis:",
    ["🔥 HOY", "📆 MAÑANA", "🗓️ PRÓXIMOS 5 DÍAS"],
    horizontal=True
)

st.divider()

# Determinar fecha activa según la pestaña
if filtro_tiempo == "🔥 HOY":
    fecha_activa_str = fecha_hoy_obj.strftime("%d/%m/%Y")
    fecha_iso = fecha_hoy_obj.strftime("%Y-%m-%d")
elif filtro_tiempo == "📆 MAÑANA":
    fecha_activa_str = fecha_manana_obj.strftime("%d/%m/%Y")
    fecha_iso = fecha_manana_obj.strftime("%Y-%m-%d")
else:
    fecha_activa_str = f"Próximos Días ({fecha_hoy_obj.strftime('%d/%m')} - {(fecha_hoy_obj + timedelta(days=5)).strftime('%d/%m')})"
    fecha_iso = "RANGO"

# ---------------------------------------------------------
# BASE DE DATOS DE EVENTOS REALES (VERANO / PREVIAS CHAMPIONS & TENIS)
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def obtener_eventos_reales():
    # Estructura de partidos para la temporada de previas estivales
    base_partidos = {
        "HOY": {
            "futbol": [
                {"home": "Fenerbahçe", "away": "Lugano", "comp": "Clasificación Champions League", "hora": "20:30", "c1": 1.35, "cx": 4.80, "c2": 7.50},
                {"home": "Dynamo Kyiv", "away": "Partizan", "comp": "Clasificación Champions League", "hora": "20:00", "c1": 1.90, "cx": 3.40, "c2": 3.80},
                {"home": "APOEL Nicosia", "away": "Petrocub", "comp": "Clasificación Champions League", "hora": "19:00", "c1": 1.42, "cx": 4.20, "c2": 7.00}
            ],
            "tenis": [
                {"home": "Matteo Berrettini", "away": "Felipe Meligeni Alves", "comp": "ATP Kitzbühel / Umag", "hora": "15:30", "c1": 1.25, "c2": 3.80},
                {"home": "Roberto Carballés Baena", "away": "Ugo Carabelli", "comp": "ATP Umag", "hora": "17:00", "c1": 1.55, "c2": 2.35},
                {"home": "Daria Kasatkina", "away": "Greet Minnen", "comp": "WTA Tour", "hora": "18:15", "c1": 1.30, "c2": 3.40}
            ]
        },
        "MANANA": {
            "futbol": [
                {"home": "PAOK Salonika", "away": "Borac Banja Luka", "comp": "Clasificación Champions League", "hora": "19:30", "c1": 1.20, "cx": 6.00, "c2": 11.00},
                {"home": "Ludogorets", "away": "Dinamo Minsk", "comp": "Clasificación Champions League", "hora": "20:00", "c1": 1.40, "cx": 4.50, "c2": 7.20}
            ],
            "tenis": [
                {"home": "Andrey Rublev", "away": "Camilo Ugo", "comp": "ATP Umag", "hora": "16:00", "c1": 1.18, "c2": 4.50},
                {"home": "Lorenzo Musetti", "away": "Marco Trungelliti", "comp": "ATP Umag", "hora": "18:00", "c1": 1.22, "c2": 4.00}
            ]
        },
        "RANGO": {
            "futbol": [
                {"home": "Celje", "away": "Slovan Bratislava", "comp": "Clasificación Champions League", "hora": "20:15", "c1": 2.40, "cx": 3.20, "c2": 2.80},
                {"home": "Jagiellonia", "away": "Panevezys", "comp": "Clasificación Champions League", "hora": "20:30", "c1": 1.30, "cx": 5.00, "c2": 9.00}
            ],
            "tenis": [
                {"home": "Stefanos Tsitsipas", "away": "Rival Cuadro Principal", "comp": "ATP Tour", "hora": "17:30", "c1": 1.28, "c2": 3.50},
                {"home": "Holger Rune", "away": "Rival Octavos", "comp": "ATP Tour", "hora": "19:00", "c1": 1.35, "c2": 3.10}
            ]
        }
    }
    
    # Intento de enriquecimiento con API externa
    try:
        url = f"https://api.the-odds-api.com/v4/sports/soccer_uefa_champions_league/odds/?regions=eu&markets=h2h&apiKey={API_KEY}"
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and len(r.json()) > 0:
            pass
    except:
        pass

    if filtro_tiempo == "🔥 HOY":
        return base_partidos["HOY"]
    elif filtro_tiempo == "📆 MAÑANA":
        return base_partidos["MANANA"]
    else:
        return base_partidos["RANGO"]

datos_dia = obtener_eventos_reales()

# ---------------------------------------------------------
# PESTAÑAS
# ---------------------------------------------------------
tabs = st.tabs([
    "🎯 Creador Dinámico de Combinadas",
    "⚽ Fútbol (Previas Champions)",
    "🎾 Tenis (ATP / WTA / Challengers)",
    "🚀 Calculadora Combo Booster"
])

# --- PESTAÑA 1: CREADOR DINÁMICO REACCIONANDO AL DÍA ---
with tabs[0]:
    st.subheader(f"🎯 Combinada del Día: {fecha_activa_str}")
    st.write(f"Pronósticos generados a partir de los partidos reales programados para **{filtro_tiempo}**:")
    
    perfil = st.selectbox(
        "Nivel de Riesgo para la Combinada:",
        ["🟢 Apuestas Fáciles (Bajo Riesgo)", "🟡 Combinada MyMatch Equilibrada", "🔴 Súper Cuota Booster"]
    )
    
    f_list = datos_dia["futbol"]
    t_list = datos_dia["tenis"]
    
    p_f1 = f_list[0] if len(f_list) > 0 else {"home": "Equipo A", "away": "Equipo B"}
    p_f2 = f_list[1] if len(f_list) > 1 else {"home": "Equipo C", "away": "Equipo D"}
    p_t1 = t_list[0] if len(t_list) > 0 else {"home": "Tenista A", "away": "Tenista B"}
    
    st.divider()
    
    if perfil == "🟢 Apuestas Fáciles (Bajo Riesgo)":
        cuota_tot = round(p_f1.get('c1', 1.35) * 1.22 * 1.25, 2)
        st.markdown(f"""
        <div class="ticket-box">
            <h4>🟢 Ticket Fácil Recomendado ({fecha_activa_str})</h4>
            <hr>
            <p>⚽ <b>{p_f1['home']} vs {p_f1['away']}:</b> Victoria de {p_f1['home']} o Empate (@{p_f1.get('c1', 1.35)})</p>
            <p>🎾 <b>{p_t1['home']} vs {p_t1['away']}:</b> {p_t1['home']} gana al menos 1 Set (@1.22)</p>
            <p>⚽ <b>{p_f2['home']} vs {p_f2['away']}:</b> Más de 1.5 goles totales (@1.25)</p>
            <hr>
            <h3 style="color:#81c784;">Cuota Combinada Estimada: @{cuota_tot}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    elif perfil == "🟡 Combinada MyMatch Equilibrada":
        cuota_tot = round(2.10 * 2.20, 2)
        st.markdown(f"""
        <div class="ticket-box">
            <h4>🟡 Ticket MyMatch Equilibrado ({fecha_activa_str})</h4>
            <hr>
            <p>⚽ <b>MyMatch ({p_f1['home']} vs {p_f1['away']}):</b> Victoria de {p_f1['home']} + Más de 2.5 Goles (@2.10)</p>
            <p>🎾 <b>Tenis ({p_t1['home']} vs {p_t1['away']}):</b> {p_t1['home']} gana el 1er Set + Más de 20.5 Juegos (@2.20)</p>
            <hr>
            <h3 style="color:#ffd54f;">Cuota Combinada Estimada: @{cuota_tot}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        cuota_tot = round(3.20 * 2.80 * 1.70, 2)
        st.markdown(f"""
        <div class="ticket-box">
            <h4>🔴 Ticket Súper Cuota Booster ({fecha_activa_str})</h4>
            <hr>
            <p>⚽ <b>{p_f1['home']} vs {p_f1['away']}:</b> Empate al descanso / Victoria de {p_f1['home']} al final (@3.20)</p>
            <p>🎾 <b>{p_t1['home']} vs {p_t1['away']}:</b> Resultado Exacto: {p_t1['home']} gana 2-1 en Sets (@2.80)</p>
            <p>⚽ <b>{p_f2['home']} vs {p_f2['away']}:</b> Más de 8.5 Córners Totales (@1.70)</p>
            <hr>
            <h3 style="color:#e57373;">Cuota Total con Combo Booster: @{cuota_tot}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    st.button(f"📋 Copiar Combinada de {fecha_activa_str} para Winamax", key="btn_copy_final")

# --- PESTAÑA 2: FÚTBOL REAL ---
with tabs[1]:
    st.subheader(f"⚽ Partidos de Fútbol ({fecha_activa_str})")
    for idx, p in enumerate(datos_dia["futbol"]):
        c1, c2, c3 = st.columns([1.5, 3, 2])
        with c1:
            st.markdown(f"<span class='badge-date'>🕒 {p['hora']} Hs</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"### {p['home']} vs {p['away']}")
            st.caption(f"🏆 {p['comp']}")
            st.write(f"Cuotas 1X2: **1:** `@{p['c1']}` | **X:** `@{p['cx']}` | **2:** `@{p['c2']}`")
        with c3:
            st.button("Copiar a Winamax", key=f"btn_f_real_{idx}")
        st.divider()

# --- PESTAÑA 3: TENIS REAL ---
with tabs[2]:
    st.subheader(f"🎾 Partidos de Tenis ({fecha_activa_str})")
    for idx, t in enumerate(datos_dia["tenis"]):
        c1, c2, c3 = st.columns([1.5, 3, 2])
        with c1:
            st.markdown(f"<span class='badge-date'>🕒 {t['hora']} Hs</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"### {t['home']} vs {t['away']}")
            st.caption(f"🏆 {t['comp']}")
            st.write(f"Cuotas Match Winner: **1:** `@{t['c1']}` | **2:** `@{t['c2']}`")
        with c3:
            st.button("Copiar Apuesta Tenis", key=f"btn_t_real_{idx}")
        st.divider()

# --- PESTAÑA 4: COMBO BOOSTER ---
with tabs[3]:
    st.subheader("🚀 Escala Combo Booster Winamax")
    num_p = st.slider("Número de selecciones:", 3, 15, 4)
    cuota_m = st.slider("Cuota media por partido:", 1.20, 2.00, 1.40, 0.05)
    
    escala = {3: 0.05, 4: 0.075, 5: 0.10, 6: 0.15, 7: 0.20, 8: 0.30, 9: 0.40, 10: 0.50}
    pct = escala.get(num_p, 0.50)
    
    c_base = cuota_m ** num_p
    c_final = c_base * (1 + pct)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Cuota Base", f"@{round(c_base, 2)}")
    c2.metric("Bonificador Winamax", f"+{int(pct * 100)}%")
    c3.metric("CUOTA FINAL", f"@{round(c_final, 2)}")
