import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Evaluador de Iniciativas", layout="wide")

# =========================
# HEADER
# =========================
st.title("Evaluador Estratégico de Iniciativas")
st.caption("Herramienta de análisis para priorización basada en impacto vs esfuerzo")

# =========================
# DEFINICIONES
# =========================
def definicion_score():
    st.info("""
**Escala de evaluación (1 a 5):**

1 → Muy bajo impacto / muy simple  
2 → Bajo  
3 → Medio  
4 → Alto  
5 → Muy alto impacto / muy complejo  
""")

def definicion_roi():
    st.info("""
**ROI (Return on Investment)**

Relación entre el impacto (prioridad) y el esfuerzo (complejidad).

- ROI alto → conviene ejecutar  
- ROI bajo → evaluar o descartar  
""")

# =========================
# LAYOUT
# =========================
col_left, col_right = st.columns([2,1])

# =========================
# FORMULARIO PRINCIPAL
# =========================
with col_left:

    st.subheader("📊 Evaluación de la Iniciativa")

    st.markdown("### 📈 Prioridad (Impacto)")
    definicion_score()

    p1 = st.slider("Impacto en ingresos", 1, 5, 3, help="Impacto directo en generación de ingresos")
    p2 = st.slider("Reducción de riesgos", 1, 5, 3, help="Capacidad de mitigar riesgos operativos o financieros")
    p3 = st.slider("Eficiencia operativa", 1, 5, 3, help="Optimización de procesos o reducción de tiempos")

    st.markdown("---")

    st.markdown("### ⚙️ Complejidad (Esfuerzo)")
    definicion_score()

    c1 = st.slider("Nivel técnico requerido", 1, 5, 3, help="Nivel de dificultad técnica de implementación")
    c2 = st.slider("Dependencias", 1, 5, 3, help="Cantidad de áreas o sistemas involucrados")
    c3 = st.slider("Tiempo de implementación", 1, 5, 3, help="Duración estimada del proyecto")

    st.markdown("---")

    st.markdown("### 🏭 Variables Operativas")

    horas = st.number_input("Horas mensuales", min_value=0.0, value=176.0, help="Cantidad de horas invertidas en el proceso actual")
    fte = horas / 176

    st.metric("👥 FTE estimado", f"{fte:.2f}")

    repetitivo = st.selectbox("Proceso repetitivo", ["Alto", "Medio", "Bajo"], help="Frecuencia de ejecución del proceso")
    estandarizado = st.selectbox("Proceso estandarizado", ["Sí", "No"], help="Nivel de estandarización del proceso")
    volumen = st.selectbox("Volumen de operación", ["Alto", "Medio", "Bajo"], help="Cantidad de transacciones o actividades")
    errores = st.selectbox("Errores manuales", ["Alto", "Medio", "Bajo"], help="Frecuencia de errores humanos en el proceso")

    # =========================
    # SCORE
    # =========================
    score_map = {"Alto":5, "Medio":3, "Bajo":1}
    bool_map = {"Sí":5, "No":1}

    prioridad = (p1 + p2 + p3 + score_map[volumen] + score_map[errores]) / 5
    complejidad = (c1 + c2 + c3 + (6 - bool_map[estandarizado]) + (6 - score_map[repetitivo])) / 5

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

    st.markdown("---")

    st.markdown("### Resultado del Análisis")

    st.success(f"""
**Clasificación:** {tipo}  
**Prioridad:** {prioridad:.2f}  
**Complejidad:** {complejidad:.2f}  
**ROI:** {roi:.2f}
""")

    definicion_roi()

# =========================
# PANEL DERECHO (VISUAL)
# =========================
with col_right:

    st.subheader("📍 Matriz de Priorización")

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

- 🟢 Arriba izquierda → Quick Wins  
- 🔵 Arriba derecha → Estratégicos  
- 🟡 Abajo izquierda → Opcionales  
- 🔴 Abajo derecha → Descartar  
""")