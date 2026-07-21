import streamlit as st

st.set_page_config(
    page_title="Winamax Combo App",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Mi App de Análisis Winamax")
st.caption("Versión Privada v1.0")

# Menú lateral
seccion = st.sidebar.radio(
    "Selecciona sección:",
    [
        "🔥 Apuestas Fáciles",
        "🏆 Partidos Top & Champions (MyMatch)",
        "🚀 Combinadas Destacadas (Combo Booster)"
    ]
)

partidos = [
    {
        "liga": "Champions League",
        "partido": "Real Madrid vs Dortmund",
        "faciles": "Gana Real Madrid o Empate (@1.22)",
        "mymatch": "Real Madrid gana + Más de 2.5 goles + Vinícius tira a puerta (@2.85)"
    },
    {
        "liga": "Premier League",
        "partido": "Liverpool vs Everton",
        "faciles": "Victoria Liverpool (@1.35)",
        "mymatch": "Liverpool gana + Ambos anotan: NO (@3.40)"
    }
]

if seccion == "🔥 Apuestas Fáciles":
    st.header("🎯 Apuestas de Bajo Riesgo")
    for p in partidos:
        st.subheader(p["partido"])
        st.caption(p["liga"])
        st.success(f"Opción recomendada: **{p['faciles']}**")
        st.divider()

elif seccion == "🏆 Partidos Top & Champions (MyMatch)":
    st.header("⭐ Partidazos y MyMatch")
    for p in partidos:
        with st.expander(f"{p['partido']} ({p['liga']})", expanded=True):
            st.write(f"**Sugerencia MyMatch:** {p['mymatch']}")
            st.button("Copiar jugada", key=p["partido"])

elif seccion == "🚀 Combinadas Destacadas (Combo Booster)":
    st.header("⚡ Combinadas de 3+ Partidos")
    st.markdown("""
    1. Real Madrid vs Dortmund -> Gana Real Madrid
    2. Liverpool vs Everton -> Victoria Liverpool
    3. FC Barcelona vs Getafe -> FC Barcelona +1.5 goles
    """)
    st.metric("Cuota con Combo Booster", "@2.54")
