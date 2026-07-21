import streamlit as st
import requests
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO DE MARCA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Winamax Pro Analytics Studio",
    page_icon="🟥",
    layout="wide"
)

# Estilos CSS profesionales (Tema Oscuro Winamax)
st.markdown("""
    <style>
    .main { background-color: #121418; }
    .stApp { background-color: #121418; }
    .css-1d3912b { background-color: #1a1d24; }
    
    .winamax-header {
        background: linear-gradient(90deg, #d32f2f 0%, #8e0000 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #1e222d;
        border: 1px solid #2d323e;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .badge-live {
        background-color: #d32f2f;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-value {
        background-color: #2e7d32;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CABECERA DE LA APLICACIÓN
# ---------------------------------------------------------
st.markdown("""
    <div class="winamax-header">
        <h1>🟥 WINAMAX PRO ANALYTICS</h1>
        <p>Motor de Algoritmos para Selección de Valor, MyMatch y Optimización Combo Booster</p>
    </div>
""", unsafe_allow_html=True)

API_KEY = "e387548ff23f836b1052c3b59b045f45"
fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/29/Winamax_logo.svg", width=180)
st.sidebar.markdown(f"**Estado del Sistema:** 🟢 En Línea")
st.sidebar.markdown(f"**Última Sincronización:**\n`{fecha_actual}`")
st.sidebar.divider()

# ---------------------------------------------------------
# EXTRACCIÓN Y PROCESAMIENTO DE DATOS EN TIEMPO REAL
# ---------------------------------------------------------
@st.cache_data(ttl=900)  # Actualiza automáticamente cada 15 minutos
def obtener_datos_api(deporte_key):
    url = f"https://api.the-odds-api.com/v4/sports/{deporte_key}/odds/?regions=eu&markets=h2h&apiKey={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []

# Carga de deportes principales
partidos_futbol = obtener_datos_api("soccer_spain_la_liga") + obtener_datos_api("soccer_uefa_champions_league") + obtener_datos_api("soccer_epl")
partidos_tenis = obtener_datos_api("tennis_atp") + obtener_datos_api("tennis_wta")

# ---------------------------------------------------------
# ESTRUCTURA PRINCIPAL DE LA APP
# ---------------------------------------------------------
tabs = st.tabs([
    "📊 Panel Analítico de Partidos", 
    "🎯 Algoritmo MyMatch & DNB", 
    "🚀 Generador Combo Booster",
    "📈 Estudio de Valor Esperado (EV)"
])

# --- PESTAÑA 1: PANEL ANALÍTICO ---
with tabs[0]:
    st.subheader("⚽ / 🎾 Eventos Programados y Cuotas Directas")
    
    col_deporte = st.radio("Filtrar Disciplina:", ["Todos", "Fútbol (Top Ligas/Champions)", "Tenis (ATP/WTA)"], horizontal=True)
    
    partidos_a_mostrar = []
    if col_deporte in ["Todos", "Fútbol (Top Ligas/Champions)"]:
        for p in partidos_futbol:
            p['tipo_deporte'] = 'Fútbol'
            partidos_a_mostrar.append(p)
    if col_deporte in ["Todos", "Tenis (ATP/WTA)"]:
        for p in partidos_tenis:
            p['tipo_deporte'] = 'Tenis'
            partidos_a_mostrar.append(p)
            
    if not partidos_a_mostrar:
        st.info("ℹ️ No hay eventos en vivo o de cuotas directas programados en las próximas horas para los filtros seleccionados.")
    else:
        for idx, evento in enumerate(partidos_a_mostrar):
            with st.container():
                c1, c2, c3 = st.columns([3, 2, 2])
                
                home = evento.get('home_team', 'Equipo A')
                away = evento.get('away_team', 'Equipo B')
                deporte = evento.get('tipo_deporte', 'Deporte')
                
                # Extracción de cuotas si están disponibles
                cuota_1, cuota_x, cuota_2 = "N/A", "N/A", "N/A"
                if evento.get('bookmakers'):
                    for bm in evento['bookmakers']:
                        for mkt in bm.get('markets', []):
                            if mkt['key'] == 'h2h':
                                for outcome in mkt['outcomes']:
                                    if outcome['name'] == home:
                                        cuota_1 = outcome['price']
                                    elif outcome['name'] == away:
                                        cuota_2 = outcome['price']
                                    elif outcome['name'] == 'Draw':
                                        cuota_x = outcome['price']

                with c1:
                    st.markdown(f"<span class='badge-value'>{deporte.upper()}</span>", unsafe_allow_html=True)
                    st.markdown(f"### {home} vs {away}")
                    st.caption(f"ID Evento: `{evento.get('id', 'N/A')}` | Inicio: {evento.get('commence_time', 'Hoy')[:16].replace('T', ' ')}")
                
                with c2:
                    st.markdown("**Cuotas de Mercado (1X2 / ML)**")
                    if deporte == 'Fútbol':
                        st.write(f"**1:** `{cuota_1}` | **X:** `{cuota_x}` | **2:** `{cuota_2}`")
                    else:
                        st.write(f"**1:** `{cuota_1}` | **2:** `{cuota_2}`")
                        
                with c3:
                    st.button("Copiar a Winamax", key=f"btn_copy_{idx}_{evento.get('id')}")
                    
                st.divider()

# --- PESTAÑA 2: MYMATCH & DNB ---
with tabs[1]:
    st.subheader("🛡️ Cobertura DNB (Draw No Bet) & Creación MyMatch")
    st.write("Estrategia de minimización del riesgo mediante anulación por empate y apuestas correlacionadas.")
    
    st.warning("""
    **Criterio Técnico DNB:**
    El mercado *Empate No Apuesta* elimina la opción X. Si el partido termina igualado, el importe de la apuesta es reembolsado íntegramente por la casa.
    """)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("### 📋 Ejemplo de Estructuración MyMatch")
        st.code("""
1. Resultado Final: Victoria Local
2. Total Goles: Más de 1.5 goles
3. Disparos a Puerta: Delantero +1.5 remates
---
Cuota Estimada Compuesta: @2.85
        """, language="text")
        
    with col_d2:
        st.markdown("### 📊 Calculadora de Cobertura DNB")
        m_cuota = st.number_input("Cuota Victoria Directa (1):", value=2.10, step=0.05)
        m_empate = st.number_input("Cuota Empate (X):", value=3.20, step=0.05)
        
        # Fórmula matemática de cobertura DNB manual
        porcentaje_empate = (1 / m_empate)
        cuota_dnb_efectiva = m_cuota * (1 - porcentaje_empate)
        
        st.success(f"**Cuota DNB Resultante:** @{round(cuota_dnb_efectiva, 2)}")

# --- PESTAÑA 3: COMBO BOOSTER ---
with tabs[2]:
    st.subheader("🚀 Motor Optimizado Combo Booster")
    st.write("El Combo Booster de Winamax añade un porcentaje de beneficio extra en función del número de selecciones en la combinada.")
    
    n_partidos = st.slider("Número de partidos en la combinada:", min_value=3, max_value=7, value=4)
    cuota_promedio = st.slider("Cuota promedio por selección:", min_value=1.20, max_value=2.00, value=1.45, step=0.05)
    
    cuota_base = cuota_promedio ** n_partidos
    
    # Tabla oficial aproximada de bonificación Combo Booster
    tabla_booster = {3: 0.05, 4: 0.075, 5: 0.10, 6: 0.15, 7: 0.20}
    bono_pct = tabla_booster.get(n_partidos, 0.05)
    
    cuota_con_booster = cuota_base * (1 + bono_pct)
    
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Cuota Base Multiplicada", f"@{round(cuota_base, 2)}")
    m2.metric("Bonificación Winamax", f"+{int(bono_pct * 100)}%")
    m3.metric("Cuota Final Real", f"@{round(cuota_con_booster, 2)}", delta=f"+{round(cuota_con_booster - cuota_base, 2)} extra")

# --- PESTAÑA 4: ESTUDIO EV ---
with tabs[3]:
    st.subheader("📈 Análisis de Valor Esperado (Expected Value)")
    st.write("Fundamento matemático para evaluar si una cuota ofrecida por la casa de apuestas tiene valor a largo plazo.")
    
    st.latex(r"EV = (P_{real} \times \text{Cuota}) - 1")
    
    col_ev1, col_ev2 = st.columns(2)
    with col_ev1:
        prob_estimada = st.slider("Tu Estimación de Probabilidad (%):", min_value=1, max_value=99, value=60) / 100
        cuota_casa = st.number_input("Cuota Ofrecida por Winamax:", value=1.80, step=0.05)
        
    with col_ev2:
        ev = (prob_estimada * cuota_casa) - 1
        if ev > 0:
            st.success(f"**EV Positivo (+{round(ev*100, 2)}%)**\n\nEsta apuesta tiene valor estadístico a largo plazo.")
        else:
            st.error(f"**EV Negativo ({round(ev*100, 2)}%)**\n\nNo se recomienda apostar a esta cuota con la probabilidad estimada.")
