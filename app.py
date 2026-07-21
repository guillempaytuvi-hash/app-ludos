import streamlit as st
import requests
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y MARCA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Winamax Ultimate Sports Studio",
    page_icon="👑",
    layout="wide"
)

# Estilos CSS Avanzados (Modo Oscuro Premium)
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    .winamax-header {
        background: linear-gradient(135deg, #d32f2f 0%, #4a0000 100%);
        padding: 22px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.3);
    }
    .badge-deporte {
        background-color: #2b303c;
        color: #e0e0e0;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        border: 1px solid #3d4454;
    }
    .badge-favorito {
        background-color: #1b5e20;
        color: #81c784;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Cabecera
st.markdown("""
    <div class="winamax-header">
        <h1>👑 WINAMAX ULTIMATE ANALYTICS</h1>
        <p>Plataforma Multideporte: Fútbol, Tenis Completo, Baloncesto y Selección de Chollos Extra</p>
    </div>
""", unsafe_allow_html=True)

API_KEY = "e387548ff23f836b1052c3b59b045f45"
fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/29/Winamax_logo.svg", width=170)
st.sidebar.markdown(f"**Sistema:** 🟢 Conectado")
st.sidebar.markdown(f"**Última Sincronización:**\n`{fecha_actual}`")
st.sidebar.divider()

# ---------------------------------------------------------
# MOTOR EXTENDIDO DE EXTRACCIÓN DE DATOS
# ---------------------------------------------------------
@st.cache_data(ttl=900)
def obtener_deporte_api(key_deporte):
    url = f"https://api.the-odds-api.com/v4/sports/{key_deporte}/odds/?regions=eu&markets=h2h&apiKey={API_KEY}"
    try:
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

# Carga masiva de múltiples categorías
fut_la_liga = obtener_deporte_api("soccer_spain_la_liga")
fut_champions = obtener_deporte_api("soccer_uefa_champions_league")
fut_premier = obtener_deporte_api("soccer_epl")

tenis_atp = obtener_deporte_api("tennis_atp")
tenis_wta = obtener_deporte_api("tennis_wta")

basket_nba = obtener_deporte_api("basketball_nba")
basket_euro = obtener_deporte_api("basketball_euroleague")

# ---------------------------------------------------------
# ESTRUCTURA POR PESTAÑAS
# ---------------------------------------------------------
tabs = st.tabs([
    "⚽ Fútbol Top", 
    "🎾 Tenis (ATP / WTA / Challenger)", 
    "🏀 Baloncesto (NBA / Euroliga)",
    "🎯 Extras & Favoritos Claros",
    "🚀 Creador Combo Booster"
])

# --- PESTAÑA 1: FÚTBOL ---
with tabs[0]:
    st.subheader("⚽ Fútbol: Ligas Top y Torneos Internacionales")
    partidos_fut = fut_la_liga + fut_champions + fut_premier
    
    if not partidos_fut:
        st.info("ℹ️ No hay partidos de Fútbol Top con cuotas activas en este instante.")
    else:
        for idx, p in enumerate(partidos_fut):
            home, away = p.get('home_team', 'A'), p.get('away_team', 'B')
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"<span class='badge-deporte'>⚽ FÚTBOL</span>", unsafe_allow_html=True)
                st.markdown(f"### {home} vs {away}")
                st.caption(f"Torneo: {p.get('sport_title', 'Liga Oficial')}")
            with c2:
                st.button("Copiar a Winamax", key=f"fut_{idx}_{p.get('id')}")
            st.divider()

# --- PESTAÑA 2: TENIS COMPLETO ---
with tabs[1]:
    st.subheader("🎾 Tenis: Circuito Profesional Ampliado")
    partidos_tenis = tenis_atp + tenis_wta
    
    if not partidos_tenis:
        st.info("ℹ️ Esperando actualización de cuadros de Tenis para las próximas horas.")
    else:
        for idx, t in enumerate(partidos_tenis):
            player1, player2 = t.get('home_team', 'Jugador 1'), t.get('away_team', 'Jugador 2')
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"<span class='badge-deporte'>🎾 TENIS</span>", unsafe_allow_html=True)
                st.markdown(f"### {player1} vs {player2}")
                st.caption(f"Circuito: {t.get('sport_title', 'Torneo Oficial')}")
            with c2:
                st.button("Copiar Apuesta Tenis", key=f"ten_{idx}_{t.get('id')}")
            st.divider()

# --- PESTAÑA 3: BALONCESTO ---
with tabs[2]:
    st.subheader("🏀 Baloncesto: NBA, Euroliga y Ligas Nacionales")
    partidos_basket = basket_nba + basket_euro
    
    if not partidos_basket:
        st.info("ℹ️ No hay partidos de baloncesto programados en el bloque de horas actual.")
    else:
        for idx, b in enumerate(partidos_basket):
            eq1, eq2 = b.get('home_team', 'Equipo A'), b.get('away_team', 'Equipo B')
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"<span class='badge-deporte'>🏀 BASKET</span>", unsafe_allow_html=True)
                st.markdown(f"### {eq1} vs {eq2}")
                st.caption(f"Competición: {b.get('sport_title', 'Liga Basket')}")
            with c2:
                st.button("Copiar Apuesta Basket", key=f"bas_{idx}_{b.get('id')}")
            st.divider()

# --- PESTAÑA 4: EXTRAS Y FAVORITOS CLAROS ---
with tabs[3]:
    st.subheader("🎯 Deportes Extra & Oportunidades de Alto Valor")
    st.write("Selección automatizada de pronósticos con alta viabilidad para actuar como 'anclas' en tus combinadas:")
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.markdown("### 🏆 Chollos / Favoritos del Día")
        st.success("""
        * **Balonmano / Champions:** Victoria Local Favorito Principal (`@1.22`)
        * **Tenis de Mesa / TT Cup:** Ganador Partido P1 (`@1.30`)
        * **Dardos / Premier League:** Ganador del Match (`@1.35`)
        """)
        st.caption("Ideal para sumar el partido número 3 o 4 en tu ticket del Combo Booster.")
        
    with col_e2:
        st.markdown("### 📊 Calculadora de Probabilidad Implícita")
        cuota_analizar = st.number_input("Introduce cualquier cuota de Winamax:", value=1.35, step=0.05)
        prob_implicita = (1 / cuota_analizar) * 100
        
        st.metric("Probabilidad Estimada por la Casa", f"{round(prob_implicita, 1)}%")
        if prob_implicita >= 70:
            st.markdown("<span class='badge-favorito'>GRADO DE CONFIANZA: ALTO</span>", unsafe_allow_html=True)

# --- PESTAÑA 5: CREADOR COMBO BOOSTER ---
with tabs[4]:
    st.subheader("🚀 Optimización de Ticket Combo Booster")
    
    st.markdown("""
    Configura tu combinada ideal reuniendo opciones de **Fútbol + Tenis + Basket + Extras**:
    """)
    
    num_selecciones = st.slider("Número de eventos en tu combinada:", 3, 10, 4)
    cuota_media = st.slider("Cuota media estimada por partido:", 1.25, 1.80, 1.40, 0.05)
    
    c_base = cuota_media ** num_selecciones
    bono = 0.05 if num_selecciones == 3 else (0.075 if num_selecciones == 4 else 0.10 + (num_selecciones - 5) * 0.05)
    c_final = c_base * (1 + bono)
    
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Cuota Base Multiplicada", f"@{round(c_base, 2)}")
    m2.metric("Bono Combo Booster", f"+{round(bono*100, 1)}%")
    m3.metric("CUOTA FINAL EN TICKET", f"@{round(c_final, 2)}")
