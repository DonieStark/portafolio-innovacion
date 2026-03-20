import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Priorización de Iniciativas", layout="centered")

st.title("📊 Evaluador de Prioridad vs Complejidad")

st.subheader("Ingrese el nombre de la iniciativa")
nombre = st.text_input("Nombre de la iniciativa")

st.divider()

# =========================
# PRIORIDAD
# =========================
st.subheader("Evaluación de PRIORIDAD (Impacto)")

p1 = st.slider("Impacto en ingresos / ahorro", 1, 5, 3)
p2 = st.slider("Reducción de riesgos", 1, 5, 3)
p3 = st.slider("Mejora de eficiencia", 1, 5, 3)
p4 = st.slider("Impacto en el negocio", 1, 5, 3)
p5 = st.slider("Urgencia", 1, 5, 3)

prioridad = (p1 + p2 + p3 + p4 + p5) / 5

st.write(f"👉 Score Prioridad: **{prioridad:.2f}**")

st.divider()

# =========================
# COMPLEJIDAD
# =========================
st.subheader("🔵 Evaluación de COMPLEJIDAD")

c1 = st.slider("Nivel técnico requerido", 1, 5, 3)
c2 = st.slider("Integraciones necesarias", 1, 5, 3)
c3 = st.slider("Dependencia de otras áreas", 1, 5, 3)
c4 = st.slider("Tiempo de desarrollo", 1, 5, 3)
c5 = st.slider("Disponibilidad de recursos", 1, 5, 3)

complejidad = (c1 + c2 + c3 + c4 + c5) / 5

st.write(f"👉 Score Complejidad: **{complejidad:.2f}**")

st.divider()

# =========================
# CLASIFICACIÓN
# =========================
st.subheader("Resultado")

if prioridad >= 4 and complejidad <= 2:
    tipo = "Quick Win"
elif prioridad >= 4 and complejidad > 2:
    tipo = "🚀 Estratégico"
elif prioridad < 4 and complejidad <= 2:
    tipo = "Opcional"
else:
    tipo = "Descartar"

st.success(f"Tipo de iniciativa: {tipo}")

roi = prioridad / complejidad
st.write(f"ROI estimado: **{roi:.2f}**")

st.divider()

# =========================
# HEATMAP SIMPLE
# =========================
st.subheader("Mapa de Prioridad vs Complejidad")

fig, ax = plt.subplots()

ax.scatter(complejidad, prioridad, s=200)

ax.set_xlim(0, 5)
ax.set_ylim(0, 5)

ax.set_xlabel("Complejidad")
ax.set_ylabel("Prioridad")

ax.axhline(3, linestyle='--')
ax.axvline(3, linestyle='--')

ax.set_title("Matriz de Priorización")

st.pyplot(fig)