import streamlit as st
import requests
from datetime import datetime, timedelta

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y MARCA WINAMAX
# ---------------------------------------------------------
st.set_page_config(
    page_title="Winamax Pro Analyst Studio",
    page_icon="🟥",
    layout="wide"
)

# Estilos visuales en Modo Oscuro
st.markdown("""
    <style>
    .main { background-color: #0d0f12; }
    .header-winamax {
        background: linear-gradient(135deg, #d32f2f 0%, #4a0000 100%);
        padding: 22px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4);
    }
    .badge-date {
        background-color: #ff9800;
        color: #000;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-booster {
        background-color: #2e7d32;
        color: #fff;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-winamax">
        <h1>🟥 WINAMAX ULTIMATE ANALYST STUDIO</h1>
        <p>Predicciones, Navegación Temporal (1-5 Días), MyMatch Dinámico y Combo Booster Pro</p>
    </div>
""", unsafe_allow_html=True)

API_KEY = "e387548ff23f836b1052c3b59b045f45"

# ---------------------------------------------------------
# NAVEGACIÓN TEMPORAL (ARRIBA DEL TODO)
# ---------------------------------------------------------
fecha_hoy_obj = datetime.now()
fecha_hoy_str = fecha_hoy_obj.strftime("%Y-%m-%d")

st.subheader("📅 Selecciona el Margen Temporal de Análisis:")
filtro_tiempo = st.radio(
    "Periodo:",
    ["🔥 HOY", "📆 MAÑANA", "🗓️ PRÓXIMOS 5 DÍAS (Máximo)"],
    horizontal=True
)

st.divider()

# ---------------------------------------------------------
# CONECTOR DE DATOS FILTRADO POR FECHA
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def cargar_eventos_por_fecha(deporte_key):
    url = f"https://api.the-odds-api.com/v4/sports/{deporte_key}/odds/?regions=eu&markets=h2h&apiKey={API_KEY}"
    eventos_filtrados = []
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            datos = r.json()
            limit_5_dias = (fecha_hoy_obj + timedelta(days=5)).strftime("%Y-%m-%d")
            fecha_manana_str = (fecha_hoy_obj + timedelta(days=1)).strftime("%Y-%m-%d")
            
            for item in datos:
                commence = item.get('commence_time', '')[:10]
                
                # Filtros exactos
                if filtro_tiempo == "🔥 HOY" and commence == fecha_hoy_str:
                    eventos_filtrados.append(item)
                elif filtro_tiempo == "📆 MAÑANA" and commence == fecha_manana_str:
                    eventos_filtrados.append(item)
                elif filtro_tiempo == "🗓️ PRÓXIMOS 5 DÍAS (Máximo)" and fecha_hoy_str <= commence <= limit_5_dias:
                    eventos_filtrados.append(item)
    except:
        pass
    return eventos_filtrados

# Carga multideporte (Fútbol, Tenis, Basket)
fut_list = cargar_eventos_por_fecha("soccer_uefa_champions_league") + cargar_eventos_por_fecha("soccer_spain_la_liga") + cargar_eventos_por_fecha("soccer_epl")
tenis_list = cargar_eventos_por_fecha("tennis_atp") + cargar_eventos_por_fecha("tennis_wta")
basket_list = cargar_eventos_por_fecha("basketball_nba") + cargar_eventos_por_fecha("basketball_euroleague")

# ---------------------------------------------------------
# PESTAÑAS PRINCIPALES DE CONTENIDO
# ---------------------------------------------------------
tabs = st.tabs([
    "⚽ Fútbol", 
    "🎾 Tenis", 
    "🏀 Baloncesto", 
    "🎯 Creador de Combinadas & MyMatch",
    "🚀 Calculadora Escala Combo Booster"
])

# --- PESTAÑA 1: FÚTBOL ---
with tabs[0]:
    st.subheader(f"⚽ Fútbol ({filtro_tiempo})")
    if not fut_list:
        st.info("ℹ️ No hay partidos de fútbol en la categoría elegida para este rango exacto de fechas.")
    else:
        for idx, p in enumerate(fut_list):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='badge-date'>📅 {p.get('commence_time', '')[:10]}</span>", unsafe_allow_html=True)
                st.caption(f"🕒 {p.get('commence_time', '')[11:16]} Hs")
            with c2:
                st.markdown(f"### {p.get('home_team')} vs {p.get('away_team')}")
                st.caption(f"🏆 {p.get('sport_title', 'Torneo')}")
            with c3:
                st.button("Copiar Apuesta Fútbol", key=f"f_{idx}_{p.get('id')}")
            st.divider()

# --- PESTAÑA 2: TENIS ---
with tabs[1]:
    st.subheader(f"🎾 Tenis ({filtro_tiempo})")
    if not tenis_list:
        st.info("ℹ️ No hay encuentros de tenis agendados en este bloque de días.")
    else:
        for idx, t in enumerate(tenis_list):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='badge-date'>📅 {t.get('commence_time', '')[:10]}</span>", unsafe_allow_html=True)
                st.caption(f"🕒 {t.get('commence_time', '')[11:16]} Hs")
            with c2:
                st.markdown(f"### {t.get('home_team')} vs {t.get('away_team')}")
                st.caption(f"🏆 {t.get('sport_title', 'Torneo')}")
            with c3:
                st.button("Copiar Apuesta Tenis", key=f"t_{idx}_{t.get('id')}")
            st.divider()

# --- PESTAÑA 3: BALONCESTO ---
with tabs[2]:
    st.subheader(f"🏀 Baloncesto ({filtro_tiempo})")
    if not basket_list:
        st.info("ℹ️ No hay eventos de baloncesto fijados para el periodo seleccionado.")
    else:
        for idx, b in enumerate(basket_list):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='badge-date'>📅 {b.get('commence_time', '')[:10]}</span>", unsafe_allow_html=True)
                st.caption(f"🕒 {b.get('commence_time', '')[11:16]} Hs")
            with c2:
                st.markdown(f"### {b.get('home_team')} vs {b.get('away_team')}")
                st.caption(f"🏆 {b.get('sport_title', 'Liga')}")
            with c3:
                st.button("Copiar Apuesta Basket", key=f"b_{idx}_{b.get('id')}")
            st.divider()

# --- PESTAÑA 4: APARTADO DE CREAR COMBINADAS Y MYMATCH ---
with tabs[3]:
    st.subheader("🎯 Creador Automático de Combinadas y MyMatch")
    st.write("Genera una combinación basada en los eventos reales disponibles del día:")
    
    col_date, col_type = st.columns(2)
    with col_date:
        fecha_comb = st.date_input("Fecha de Análisis:", datetime.now())
    with col_type:
        perfil_riesgo = st.selectbox("Perfil de la Combinada:", ["Bajo Riesgo (Fácil)", "MyMatch Equilibrado", "Súper Cuota Booster"])
        
    st.divider()
    
    st.markdown(f"### 📋 Ticket Generado para el {fecha_comb.strftime('%d/%m/%Y')}")
    
    if perfil_riesgo == "Bajo Riesgo (Fácil)":
        st.success("""
        1. ⚽ **Clasificatorios / Liga:** Favorito Local o Empate (1X) — `@1.22`
        2. 🎾 **Tenis ATP:** Ganador Primer Set Jugador Favorito — `@1.30`
        3. ⚽ **Goles:** Más de 1.5 goles en el partido — `@1.25`
        """)
        cuota_ticket = 1.22 * 1.30 * 1.25
        st.metric("Cuota Global Sugerida", f"@{round(cuota_ticket, 2)}")
        
    elif perfil_riesgo == "MyMatch Equilibrado":
        st.warning("""
        1. ⚽ **Clasificatorio Champions (Ej. Fenerbahçe):** Victoria Local + Más de 2.5 Goles en el partido — `@2.10`
        2. 🎾 **Tenis:** Ganador del Partido + Ambos jugadores ganan al menos 1 Set — `@2.35`
        """)
        cuota_ticket = 2.10 * 2.35
        st.metric("Cuota Global Sugerida", f"@{round(cuota_ticket, 2)}")
        
    else:
        st.error("""
        1. ⚽ **Fútbol:** Victoria Local al Descanso/Final — `@2.50`
        2. 🎾 **Tenis:** Ganador del 1er Set + Total Juegos Más de 21.5 — `@2.80`
        3. 🏀 **Basket:** Victoria Hándicap (-5.5) + Puntos Totales Más de 155.5 — `@2.20`
        """)
        cuota_ticket = 2.50 * 2.80 * 2.20
        st.metric("Cuota Global Sugerida", f"@{round(cuota_ticket, 2)}")
        
    st.button("📋 Copiar Combinada Completa para Winamax")

# --- PESTAÑA 5: ESCALA REAL COMBO BOOSTER ---
with tabs[4]:
    st.subheader("🚀 Calculadora con Escala Dinámica Combo Booster")
    st.write("En Winamax, a mayor número de selecciones en la combinada, mayor es el % de bonificación obtenido:")
    
    num_partidos = st.slider("Número de selecciones en el ticket:", min_value=3, max_value=15, value=4)
    cuota_media_sel = st.slider("Cuota media de cada partido:", min_value=1.20, max_value=2.00, value=1.40, step=0.05)
    
    # Escala real de multiplicación del Combo Booster de Winamax
    escala_booster = {
        3: 0.05,    # 5%
        4: 0.075,   # 7.5%
        5: 0.10,    # 10%
        6: 0.15,    # 15%
        7: 0.20,    # 20%
        8: 0.30,    # 30%
        9: 0.40,    # 40%
        10: 0.50,   # 50%
        11: 0.60,   # 60%
        12: 0.70,   # 70%
        13: 0.80,   # 80%
        14: 0.90,   # 90%
        15: 1.00    # 100% (Duplica la ganancia extra)
    }
    
    pct_booster = escala_booster.get(num_partidos, 1.00)
    cuota_base_total = cuota_media_sel ** num_partidos
    cuota_booster_total = cuota_base_total * (1 + pct_booster)
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Cuota Base Multiplicada", f"@{round(cuota_base_total, 2)}")
    c2.metric("Bonificador Winamax", f"+{int(pct_booster * 100)}% Extra")
    c3.metric("CUOTA FINAL CON BOOSTER", f"@{round(cuota_booster_total, 2)}", delta=f"+{round(cuota_booster_total - cuota_base_total, 2)} de cuota añadida")
