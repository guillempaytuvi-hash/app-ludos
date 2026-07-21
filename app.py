import streamlit as st
import random
from datetime import datetime

# Configuración de la app
st.set_page_config(
    page_title="Winamax & Flashscore Studio",
    page_icon="⚽",
    layout="wide"
)

# Estilos personalizados visuales
st.markdown("""
    <style>
    .live-badge {
        background-color: #e63946;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 12px;
    }
    .card {
        background-color: #1a1d24;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2d323e;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Winamax & Flashscore Analyst")
st.caption(f"Última actualización de datos: {datetime.now().strftime('%H:%M:%S')}")

# Botón para actualizar datos al momento
if st.button("🔄 Actualizar Datos y Cuotas en Vivo"):
    st.toast("¡Datos actualizados desde el servidor!", icon="✅")

# Menú principal superior estilo App
tabs = st.tabs([
    "📊 Resultados en Vivo (Flashscore)", 
    "🎯 Apuestas Fáciles & MyMatch", 
    "🚀 Generador Combo Booster"
])

# Base de datos interactiva
partidos_datos = [
    {
        "id": 1,
        "liga": "🏆 Champions League",
        "local": "Real Madrid",
        "visitante": "Borussia Dortmund",
        "minuto": "67'",
        "marcador": "2 - 1",
        "estado": "EN DIRECTO",
        "cuota_local": 1.30,
        "cuota_empate": 4.50,
        "cuota_visita": 7.50,
        "facil": "Gana Real Madrid o Empate (@1.18)",
        "mymatch": "Real Madrid gana + Más de 2.5 goles + Vinícius tira a puerta",
        "cuota_mymatch": 2.65
    },
    {
        "id": 2,
        "liga": "🇬🇧 Premier League",
        "local": "Liverpool",
        "visitante": "Everton",
        "minuto": "15'",
        "marcador": "0 - 0",
        "estado": "EN DIRECTO",
        "cuota_local": 1.38,
        "cuota_empate": 4.20,
        "cuota_visita": 6.80,
        "facil": "Victoria Liverpool (@1.38)",
        "mymatch": "Liverpool gana + Ambos marcan: NO",
        "cuota_mymatch": 3.10
    },
    {
        "id": 3,
        "liga": "🇪🇸 LaLiga",
        "local": "FC Barcelona",
        "visitante": "Getafe",
        "minuto": "Por empezar",
        "marcador": "21:00",
        "estado": "PROXIMO",
        "cuota_local": 1.25,
        "cuota_empate": 5.00,
        "cuota_visita": 9.00,
        "facil": "FC Barcelona +1.5 goles (@1.22)",
        "mymatch": "FC Barcelona gana al descanso/final + Getafe +2.5 tarjetas",
        "cuota_mymatch": 2.40
    }
]

# --- PESTAÑA 1: FLASHSCORE (RESULTADOS EN DIRECTO) ---
with tabs[0]:
    st.header("⚡ Marcadores y Partidos del Día")
    
    for p in partidos_datos:
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            st.markdown(f"**{p['liga']}**")
            st.write(f"### {p['local']} vs {p['visitante']}")
            
        with col2:
            if p['estado'] == "EN DIRECTO":
                st.markdown(f"<span class='live-badge'>🔴 EN VIVO {p['minuto']}</span>", unsafe_allow_html=True)
            else:
                st.caption(f"🕒 Inicio: {p['marcador']}")
            st.title(p['marcador'] if p['estado'] == "EN DIRECTO" else "vs")

        with col3:
            st.caption("Cuotas 1X2 Winamax")
            st.write(f"1: `{p['cuota_local']}` | X: `{p['cuota_empate']}` | 2: `{p['cuota_visita']}`")
        
        st.divider()

# --- PESTAÑA 2: MYMATCH & APUESTAS FÁCILES ---
with tabs[1]:
    st.header("🎯 Sugerencias de Pronósticos")
    
    for p in partidos_datos:
        with st.expander(f"📌 {p['local']} vs {p['visitante']} ({p['liga']})", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🟢 Opción Favorable / Fácil")
                st.info(p["facil"])
            with c2:
                st.subheader("🔥 Combinada MyMatch")
                st.warning(f"**{p['mymatch']}**\n\nCuota Total: **@{p['cuota_mymatch']}**")

# --- PESTAÑA 3: GENERADOR COMBO BOOSTER ---
with tabs[2]:
    st.header("🚀 Creador de Combinadas con Combo Booster")
    st.write("Selecciona los partidos que quieres incluir en tu ticket diario:")
    
    cuota_total = 1.0
    seleccionados = 0
    
    for p in partidos_datos:
        check = st.checkbox(f"{p['local']} vs {p['visitante']} - Opción Fácil ({p['facil']})", key=f"chk_{p['id']}")
        if check:
            # Extraer cuota aproximada
            cuota_partido = p['cuota_local']
            cuota_total *= cuota_partido
            seleccionados += 1
            
    st.divider()
    
    # Cálculo de bonificación Combo Booster
    bonus = 0
    if seleccionados >= 3:
        bonus = 0.05  # 5% extra para 3 partidos
    elif seleccionados >= 4:
        bonus = 0.10
        
    cuota_final = cuota_total * (1 + bonus)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Partidos Seleccionados", f"{seleccionados}")
    m2.metric("Cuota Combinada Base", f"@{round(cuota_total, 2)}")
    m3.metric("Cuota Final (Con Booster)", f"@{round(cuota_final, 2)}", delta=f"+{int(bonus*100)}% Bono Winamax" if bonus > 0 else "Añade 3+ partidos")
