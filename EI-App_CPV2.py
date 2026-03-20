import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Evaluador Estratégico", layout="wide")

# =========================
# ESTILOS UX PRO
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 15px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
}

.big-title {
    font-size: 32px;
    font-weight: 700;
}

.subtitle {
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="big-title">Evaluador Estratégico de Iniciativas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Priorización basada en impacto vs esfuerzo</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col_main, col_side = st.columns([2,1])

# =========================
# MAIN
# =========================
with col_main:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Evaluación de la Iniciativa</div>', unsafe_allow_html=True)

    # =========================
    # PRIORIDAD
    # =========================
    st.markdown("### 📈 Prioridad (Impacto)")

    st.info("""
Escala 1 a 5:
1 = Muy bajo impacto  
5 = Alto impacto en el negocio  
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        p1 = st.slider("Impacto en ingresos", 1, 5, 3,
                       help="Incremento en ingresos o generación de valor económico")
        st.caption("💡 Generación directa de valor económico")

    with col2:
        p2 = st.slider("Reducción de riesgos", 1, 5, 3,
                       help="Mitigación de riesgos operativos, legales o financieros")
        st.caption("💡 Impacto en control y cumplimiento")

    with col3:
        p3 = st.slider("Eficiencia operativa", 1, 5, 3,
                       help="Optimización de tiempos, costos o recursos")
        st.caption("💡 Mejora de productividad")

    st.markdown("---")

    # =========================
    # COMPLEJIDAD
    # =========================
    st.markdown("### ⚙️ Complejidad (Esfuerzo)")

    st.info("""
Escala 1 a 5:
1 = Fácil implementación  
5 = Alta complejidad  
""")

    col4, col5, col6 = st.columns(3)

    with col4:
        c1 = st.slider("Nivel técnico", 1, 5, 3,
                       help="Nivel de dificultad técnica")
        st.caption("💡 Integraciones, desarrollo, arquitectura")

    with col5:
        c2 = st.slider("Dependencias", 1, 5, 3,
                       help="Cantidad de áreas o sistemas involucrados")
        st.caption("💡 Más dependencias = mayor complejidad")

    with col6:
        c3 = st.slider("Tiempo implementación", 1, 5, 3,
                       help="Duración estimada del proyecto")
        st.caption("💡 Proyectos largos = más esfuerzo")

    st.markdown("---")

    # =========================
    # VARIABLES
    # =========================
    st.markdown("### 🏭 Variables Operativas")

    col7, col8, col9, col10 = st.columns(4)

    with col7:
        horas = st.number_input("Horas mensuales", 0.0, 500.0, 176.0,
                                help="Horas invertidas en el proceso actual")
        st.caption("💡 Base para calcular FTE")

    with col8:
        repetitivo = st.selectbox("Repetitividad", ["Alto", "Medio", "Bajo"],
                                 help="Frecuencia del proceso")
        st.caption("💡 Alto = automatizable")

    with col9:
        estandarizado = st.selectbox("Estandarización", ["Sí", "No"],
                                    help="Nivel de reglas claras")
        st.caption("💡 No estandarizado = mayor complejidad")

    with col10:
        errores = st.selectbox("Errores manuales", ["Alto", "Medio", "Bajo"],
                              help="Frecuencia de errores humanos")
        st.caption("💡 Alto error = oportunidad de mejora")

    fte = horas / 176
    st.metric("👥 FTE estimado", f"{fte:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # CALCULO
    # =========================
    score_map = {"Alto":5, "Medio":3, "Bajo":1}
    bool_map = {"Sí":5, "No":1}

    prioridad = (p1 + p2 + p3 + score_map[errores]) / 4
    complejidad = (c1 + c2 + c3 + (6 - bool_map[estandarizado])) / 4

    # =========================
    # CLASIFICACIÓN
    # =========================
    if prioridad >= 4 and complejidad <= 2:
        tipo = "🟢 Quick Win"
    elif prioridad >= 4:
        tipo = "🔵 Estratégico"
    elif complejidad <= 2:
        tipo = "🟡 Opcional"
    else:
        tipo = "🔴 Descartar"

    roi = prioridad / complejidad

    # =========================
    # RESULTADO
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 Resultado Ejecutivo</div>', unsafe_allow_html=True)

    colr1, colr2, colr3, colr4 = st.columns(4)

    colr1.metric("Prioridad", f"{prioridad:.2f}")
    colr2.metric("Complejidad", f"{complejidad:.2f}")
    colr3.metric("ROI", f"{roi:.2f}")
    colr4.metric("Clasificación", tipo)

    st.info("""
ROI = Prioridad / Complejidad  

👉 ROI alto = ejecutar  
👉 ROI bajo = evaluar o descartar  
""")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PANEL DERECHO
# =========================
with col_side:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📍 Matriz de Priorización</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots()

    ax.scatter(complejidad, prioridad, s=300)

    ax.axhline(3, linestyle='--')
    ax.axvline(3, linestyle='--')

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)

    ax.set_xlabel("Complejidad")
    ax.set_ylabel("Prioridad")

    st.pyplot(fig)

    st.markdown("""
### 🧠 Interpretación

🟢 Quick Wins → alto impacto / bajo esfuerzo  
🔵 Estratégicos → alto impacto / alto esfuerzo  
🟡 Opcionales → bajo impacto / bajo esfuerzo  
🔴 Descartar → bajo impacto / alto esfuerzo  
""")

    st.markdown('</div>', unsafe_allow_html=True)