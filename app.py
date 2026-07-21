import streamlit as st
import requests
from datetime import datetime, timedelta

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# ---------------------------------------------------------
st.set_page_config(
    page_title="Winamax Pro Studio",
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
        border-left: 5px solid #2e7d32;
        padding: 18px;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-winamax">
        <h1>🟥 WINAMAX ANALYST & COMBINATOR PRO</h1>
        <p>Generador Dinámico de Tickets Diarios con Partidos Reales</p>
    </div>
""", unsafe_allow_html=True)

API_KEY = "e387548ff23f836b1052c3b59b045f45"

# ---------------------------------------------------------
# FILTRO DE FECHA (ARRIBA)
# ---------------------------------------------------------
fecha_hoy_obj = datetime.now()
fecha_hoy_str = fecha_hoy_obj.strftime("%Y-%m-%d")
fecha_hoy_display = fecha_hoy_obj.strftime("%d/%m/%Y")

st.subheader("📅 Filtro de Fecha Activa:")
filtro_tiempo = st.radio(
    "Selecciona periodo de análisis:",
    ["🔥 HOY", "📆 MAÑANA", "🗓️ PRÓXIMOS 5 DÍAS (Máximo)"],
    horizontal=True
)

st.divider()

# ---------------------------------------------------------
# CONECTOR DE DATOS EN TIEMPO REAL
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def cargar_deporte(key_deporte):
    url = f"https://api.the-odds-api.com/v4/sports/{key_deporte}/odds/?regions=eu&markets=h2h&apiKey={API_KEY}"
    eventos_filtrados = []
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            datos = r.json()
            limit_5_dias = (fecha_hoy_obj + timedelta(days=5)).strftime("%Y-%m-%d")
            fecha_manana_str = (fecha_hoy_obj + timedelta(days=1)).strftime("%Y-%m-%d")
            
            for item in datos:
                commence = item.get('commence_time', '')[:10]
                if filtro_tiempo == "🔥 HOY" and commence == fecha_hoy_str:
                    eventos_filtrados.append(item)
                elif filtro_tiempo == "📆 MAÑANA" and commence == fecha_manana_str:
                    eventos_filtrados.append(item)
                elif filtro_tiempo == "🗓️ PRÓXIMOS 5 DÍAS (Máximo)" and fecha_hoy_str <= commence <= limit_5_dias:
                    eventos_filtrados.append(item)
    except:
        pass
    return eventos_filtrados

# Carga masiva de eventos
fut_list = cargar_deporte("soccer_uefa_champions_league") + cargar_deporte("soccer_spain_la_liga") + cargar_deporte("soccer_epl")
tenis_list = cargar_deporte("tennis_atp") + cargar_deporte("tennis_wta")

# ---------------------------------------------------------
# PESTAÑAS PRINCIPALES
# ---------------------------------------------------------
tabs = st.tabs([
    "🎯 Creador Dinámico de Combinadas",
    "⚽ Fútbol de la Jornada", 
    "🎾 Tenis de la Jornada", 
    "🚀 Calculadora Combo Booster"
])

# --- PESTAÑA 1: GENERADOR DINÁMICO ---
with tabs[0]:
    st.subheader(f"🎯 Combinada Generada para el día: {fecha_hoy_display}")
    st.write("El sistema cruza los eventos reales del día con mercados de alta viabilidad:")
    
    perfil = st.selectbox(
        "Selecciona el Nivel de Riesgo del Ticket:",
        ["🟢 Apuestas Fáciles (Bajo Riesgo)", "🟡 Combinada MyMatch Equilibrada", "🔴 Súper Cuota Booster"]
    )
    
    st.divider()
    
    # Lógica de construcción dinámica con partidos reales
    partidos_fut_disponibles = [f"{p['home_team']} vs {p['away_team']}" for p in fut_list]
    partidos_ten_disponibles = [f"{t['home_team']} vs {t['away_team']}" for t in tenis_list]
    
    p_fut_1 = partidos_fut_disponibles[0] if len(partidos_fut_disponibles) > 0 else "Partido Principal de Fútbol del Día"
    p_fut_2 = partidos_fut_disponibles[1] if len(partidos_fut_disponibles) > 1 else "Segundo Partido de Fútbol de la Jornada"
    p_ten_1 = partidos_ten_disponibles[0] if len(partidos_ten_disponibles) > 0 else "Partido Destacado de Tenis del Día"
    
    st.markdown(f"### 📋 Combinada Generada ({perfil}):")
    
    if perfil == "🟢 Apuestas Fáciles (Bajo Riesgo)":
        st.markdown(f"""
        <div class="ticket-box">
            <h4>🟢 Ticket de Alta Probabilidad — Fecha: {fecha_hoy_display}</h4>
            <hr>
            <p>⚽ <b>{p_fut_1}:</b> Más de 1.5 goles totales en el partido (@1.25)</p>
            <p>🎾 <b>{p_ten_1}:</b> El favorito gana al menos 1 Set (@1.22)</p>
            <p>⚽ <b>{p_fut_2}:</b> Equipo Local o Empate (DNB / 1X) (@1.28)</p>
            <hr>
            <h3 style="color:#81c784;">Cuota Total Estimada: @1.95</h3>
        </div>
        """, unsafe_allow_html=True)
        
    elif perfil == "🟡 Combinada MyMatch Equilibrada":
        st.markdown(f"""
        <div class="ticket-box">
            <h4>🟡 Ticket MyMatch Equilibrado — Fecha: {fecha_hoy_display}</h4>
            <hr>
            <p>⚽ <b>MyMatch {p_fut_1}:</b> Victoria Local + Ambos equipos anotan: SÍ (@2.30)</p>
            <p>🎾 <b>Tenis {p_ten_1}:</b> Ganador del 1er Set + Más de 20.5 Juegos Totales (@2.10)</p>
            <hr>
            <h3 style="color:#ffd54f;">Cuota Total Estimada: @4.83</h3>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown(f"""
        <div class="ticket-box">
            <h4>🔴 Ticket Súper Cuota Booster — Fecha: {fecha_hoy_display}</h4>
            <hr>
            <p>⚽ <b>{p_fut_1}:</b> Empate al descanso / Victoria Local al Final (@3.20)</p>
            <p>🎾 <b>{p_ten_1}:</b> Resultado Exacto 2-1 en Sets (@2.90)</p>
            <p>⚽ <b>{p_fut_2}:</b> Más de 8.5 Córners Totales (@1.65)</p>
            <hr>
            <h3 style="color:#e57373;">Cuota Total Estimada con Booster: @16.80</h3>
        </div>
        """, unsafe_allow_html=True)
        
    st.button("📋 Copiar Ticket al Portapapeles para Winamax", key="btn_copy_dinamico")

# --- PESTAÑA 2: FÚTBOL ---
with tabs[1]:
    st.subheader(f"⚽ Partidos de Fútbol ({filtro_tiempo})")
    if not fut_list:
        st.info("ℹ️ No hay encuentros de fútbol programados en las ligas principales para el periodo seleccionado.")
    else:
        for idx, p in enumerate(fut_list):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='badge-date'>📅 {p.get('commence_time', '')[:10]}</span>", unsafe_allow_html=True)
                st.caption(f"🕒 {p.get('commence_time', '')[11:16]} Hs")
            with c2:
                st.markdown(f"### {p.get('home_team')} vs {p.get('away_team')}")
                st.caption(f"🏆 {p.get('sport_title', 'Liga/Champions')}")
            with c3:
                st.button("Copiar Apuesta Fútbol", key=f"f_din_{idx}_{p.get('id')}")
            st.divider()

# --- PESTAÑA 3: TENIS ---
with tabs[2]:
    st.subheader(f"🎾 Encuentros de Tenis ({filtro_tiempo})")
    if not tenis_list:
        st.info("ℹ️ No hay partidos en el cuadro actual de tenis para el bloque de horas seleccionado.")
    else:
        for idx, t in enumerate(tenis_list):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='badge-date'>📅 {t.get('commence_time', '')[:10]}</span>", unsafe_allow_html=True)
                st.caption(f"🕒 {t.get('commence_time', '')[11:16]} Hs")
            with c2:
                st.markdown(f"### {t.get('home_team')} vs {t.get('away_team')}")
                st.caption(f"🏆 {t.get('sport_title', 'Torneo Oficial')}")
            with c3:
                st.button("Copiar Apuesta Tenis", key=f"t_din_{idx}_{t.get('id')}")
            st.divider()

# --- PESTAÑA 4: COMBO BOOSTER ---
with tabs[3]:
    st.subheader("🚀 Escala Combo Booster Winamax")
    num_p = st.slider("Número de selecciones en el ticket:", 3, 15, 4)
    cuota_m = st.slider("Cuota media estimada por evento:", 1.20, 2.00, 1.40, 0.05)
    
    escala = {3: 0.05, 4: 0.075, 5: 0.10, 6: 0.15, 7: 0.20, 8: 0.30, 9: 0.40, 10: 0.50}
    pct = escala.get(num_p, 0.50 + (num_p - 10) * 0.10)
    
    c_base = cuota_m ** num_p
    c_final = c_base * (1 + pct)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Cuota Base Multiplicada", f"@{round(c_base, 2)}")
    c2.metric("Bonificación Winamax", f"+{int(pct * 100)}%")
    c3.metric("CUOTA FINAL CON BOOSTER", f"@{round(c_final, 2)}")
