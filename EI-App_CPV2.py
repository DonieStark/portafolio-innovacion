import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="AliDoc Evaluador", layout="wide")

# =========================
# ESTILO PRO (MEJORADO)
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* TITULOS */
.title {
    font-size: 36px;
    font-weight: 700;
    color: #111827;
}

.subtitle {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 30px;
}

/* CARDS */
.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* SECTION */
.section {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
}

/* RESULT BOX */
.result-box {
    padding: 20px;
    border-radius: 12px;
    background: #f1f5f9;
}

/* CLASIFICACION COLORES */
.quick {color:#16a34a; font-weight:700;}
.estrategico {color:#2563eb; font-weight:700;}
.opcional {color:#ca8a04; font-weight:700;}
.descartar {color:#dc2626; font-weight:700;}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">Evaluador Estratégico</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Priorización de iniciativas basada en impacto vs esfuerzo</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([2,1])

# =========================
# FORM
# =========================
with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section">📊 Evaluación</div>', unsafe_allow_html=True)

    # PRIORIDAD
    st.markdown("### Impacto")
    p1 = st.slider("Ingresos",1,5,3)
    p2 = st.slider("Riesgos",1,5,3)
    p3 = st.slider("Eficiencia",1,5,3)

    st.markdown("---")

    # COMPLEJIDAD
    st.markdown("### Complejidad")
    c1 = st.slider("Nivel técnico",1,5,3)
    c2 = st.slider("Dependencias",1,5,3)
    c3 = st.slider("Tiempo",1,5,3)

    st.markdown("---")

    # VARIABLES
    st.markdown("### Variables Operativas")

    colA, colB, colC, colD = st.columns(4)

    with colA:
        horas = st.number_input("Horas",0.0,500.0,176.0)

    with colB:
        repetitivo = st.selectbox("Repetitivo",["Alto","Medio","Bajo"])

    with colC:
        estandarizado = st.selectbox("Estandarizado",["Sí","No"])

    with colD:
        errores = st.selectbox("Errores",["Alto","Medio","Bajo"])

    fte = horas / 176
    st.metric("FTE estimado", f"{fte:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # CALCULO
    # =========================
    score_map = {"Alto":5,"Medio":3,"Bajo":1}
    bool_map = {"Sí":5,"No":1}

    prioridad = (p1+p2+p3+score_map[errores])/4
    complejidad = (c1+c2+c3+(6-bool_map[estandarizado]))/4
    roi = prioridad/complejidad

    # CLASIFICACION
    if prioridad >=4 and complejidad <=2:
        tipo = "Quick Win"
        clase = "quick"
    elif prioridad >=4:
        tipo = "Estratégico"
        clase = "estrategico"
    elif complejidad <=2:
        tipo = "Opcional"
        clase = "opcional"
    else:
        tipo = "Descartar"
        clase = "descartar"

    # =========================
    # RESULTADO PRO
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section">📌 Resultado Ejecutivo</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Prioridad", f"{prioridad:.2f}")
    m2.metric("Complejidad", f"{complejidad:.2f}")
    m3.metric("ROI", f"{roi:.2f}")

    m4.markdown(f"<div class='{clase}'>{tipo}</div>", unsafe_allow_html=True)

    st.markdown("""
<div class="result-box">
<b>ROI = Prioridad / Complejidad</b><br><br>
👉 ROI alto → ejecutar<br>
👉 ROI bajo → evaluar o descartar
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# MATRIZ
# =========================
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section">📍 Matriz</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots()

    ax.scatter(complejidad, prioridad, s=250)
    ax.axhline(3, linestyle='--')
    ax.axvline(3, linestyle='--')

    ax.set_xlim(0,5)
    ax.set_ylim(0,5)

    ax.set_xlabel("Complejidad")
    ax.set_ylabel("Prioridad")

    st.pyplot(fig)

    st.markdown("""
🟢 Quick Win  
🔵 Estratégico  
🟡 Opcional  
🔴 Descartar  
""")

    st.markdown('</div>', unsafe_allow_html=True)