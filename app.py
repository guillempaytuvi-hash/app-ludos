import streamlit as st
import requests
from datetime import datetime, timezone

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Winamax Today Analyst",
    page_icon="📅",
    layout="wide"
)

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    .winamax-header {
        background: linear-gradient(135deg, #d32f2f 0%, #4a0000 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .time-badge {
        background-color: #ff9800;
        color: #000000;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
    }
    .badge-deporte {
        background-color: #2b303c;
        color: #e0e0e0;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Cabecera con fecha de HOY
hoy_dt = datetime.now()
fecha_hoy_str = hoy_dt.strftime("%d/%m/%Y")

st.markdown(f"""
    <div class="winamax-header">
        <h1>📅 PARTIDOS Y CUOTAS DE HOY ({fecha_hoy_str})</h1>
        <p>Filtrado exclusivo de eventos que se disputan el día de hoy con hora local.</p>
    </div>
""", unsafe_allow_html=True)

API_KEY = "e387548ff23f836b1052c3b59b045f45"

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/29/Winamax_logo.svg", width=170)
st.sidebar.markdown(f"**Fecha Filtro:** `{fecha_hoy_str}`")
st.sidebar.divider()

# ---------------------------------------------------------
# FUNCIÓN DE FILTRADO EXCLUSIVO PARA HOY
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def obtener_eventos_solo_hoy(key_deporte):
    url = f"https://api.the-odds-api.com/v4/sports/{key_deporte}/odds/?regions=eu&markets=h2h&apiKey={API_KEY}"
    eventos_hoy = []
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            datos = r.json()
            fecha_hoy_iso = datetime.now().strftime("%Y-%m-%d")
            
            for item in datos:
                commence_time = item.get('commence_time', '')
                # Verificar si el partido se juega HOY (comparando fecha ISO YYYY-MM-DD)
                if commence_time.startswith(fecha_hoy_iso):
                    # Formatear la hora HH:MM
                    try:
                        dt_obj = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
                        item['hora_formateada'] = dt_obj.strftime("%H:%M")
                    except:
                        item['hora_formateada'] = commence_time[11:16]
                    eventos_hoy.append(item)
    except:
        pass
    return eventos_hoy

# Carga de datos filtrados solo para hoy
fut_hoy = obtener_eventos_solo_hoy("soccer_spain_la_liga") + obtener_eventos_solo_hoy("soccer_uefa_champions_league") + obtener_eventos_solo_hoy("soccer_epl")
tenis_hoy = obtener_eventos_solo_hoy("tennis_atp") + obtener_eventos_solo_hoy("tennis_wta")
basket_hoy = obtener_eventos_solo_hoy("basketball_nba") + obtener_eventos_solo_hoy("basketball_euroleague")

# ---------------------------------------------------------
# INTERFAZ
# ---------------------------------------------------------
tabs = st.tabs([
    "⚽ Fútbol de Hoy", 
    "🎾 Tenis de Hoy", 
    "🏀 Baloncesto de Hoy",
    "🚀 Calculadora Combo Booster"
])

# --- PESTAÑA FÚTBOL ---
with tabs[0]:
    st.subheader(f"⚽ Partidos de Fútbol Programados para Hoy ({fecha_hoy_str})")
    if not fut_hoy:
        st.info("ℹ️ No hay partidos de las ligas principales programados para lo que resta del día de hoy.")
    else:
        for idx, p in enumerate(fut_hoy):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='time-badge'>🕒 HOY {p.get('hora_formateada', '--:--')}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"### {p.get('home_team')} vs {p.get('away_team')}")
                st.caption(f"🏆 {p.get('sport_title', 'Competición')}")
            with c3:
                st.button("Copiar a Winamax", key=f"f_hoy_{idx}_{p.get('id')}")
            st.divider()

# --- PESTAÑA TENIS ---
with tabs[1]:
    st.subheader(f"🎾 Encuentros de Tenis de Hoy ({fecha_hoy_str})")
    if not tenis_hoy:
        st.info("ℹ️ No hay partidos de tenis ATP/WTA agendados para las horas restantes de hoy.")
    else:
        for idx, t in enumerate(tenis_hoy):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='time-badge'>🕒 HOY {t.get('hora_formateada', '--:--')}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"### {t.get('home_team')} vs {t.get('away_team')}")
                st.caption(f"🏆 {t.get('sport_title', 'Torneo')}")
            with c3:
                st.button("Copiar Apuesta Tenis", key=f"t_hoy_{idx}_{t.get('id')}")
            st.divider()

# --- PESTAÑA BALONCESTO ---
with tabs[2]:
    st.subheader(f"🏀 Partidos de Basket de Hoy ({fecha_hoy_str})")
    if not basket_hoy:
        st.info("ℹ️ No hay partidos de baloncesto fijados para el día de hoy.")
    else:
        for idx, b in enumerate(basket_hoy):
            c1, c2, c3 = st.columns([1.5, 3, 2])
            with c1:
                st.markdown(f"<span class='time-badge'>🕒 HOY {b.get('hora_formateada', '--:--')}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"### {b.get('home_team')} vs {b.get('away_team')}")
                st.caption(f"🏆 {b.get('sport_title', 'Liga')}")
            with c3:
                st.button("Copiar Apuesta Basket", key=f"b_hoy_{idx}_{b.get('id')}")
            st.divider()

# --- COMBO BOOSTER ---
with tabs[3]:
    st.subheader("🚀 Simulador Combo Booster para Ticket Diario")
    selecciones = st.slider("Número de partidos seleccionados hoy:", 3, 8, 3)
    cuota_m = st.slider("Cuota media estimada por evento:", 1.20, 1.80, 1.35, 0.05)
    
    cuota_base = cuota_m ** selecciones
    bono = 0.05 if selecciones == 3 else (0.075 if selecciones == 4 else 0.10)
    cuota_total = cuota_base * (1 + bono)
    
    m1, m2 = st.columns(2)
    m1.metric("Cuota Combinada", f"@{round(cuota_base, 2)}")
    m2.metric("Cuota Final con Combo Booster", f"@{round(cuota_total, 2)}", delta=f"+{int(bono*100)}% Extra")
