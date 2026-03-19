import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Portafolio de Innovación", layout="wide")

# =========================
# ARCHIVO EN LA NUBE
# =========================
ARCHIVO_DEFAULT = "iniciativas.xlsx"

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Configuración")

archivo_subido = st.sidebar.file_uploader("Sube tu Excel (opcional)", type=["xlsx"])

def obtener_archivo():
    if archivo_subido:
        return archivo_subido
    return ARCHIVO_DEFAULT

# =========================
# VALIDAR
# =========================
def inicializar_excel():
    archivo = obtener_archivo()

    if not archivo_subido and not os.path.isfile(archivo):
        st.error(f"El archivo no existe en el repo: {archivo}")
        st.stop()

# =========================
# BACKLOG
# =========================
@st.cache_data
def cargar_backlog(file):
    df = pd.read_excel(file, sheet_name="Backlog")

    if "Nombre" in df.columns:
        return df["Nombre"].dropna().astype(str).tolist()
    else:
        return df.iloc[:, 0].dropna().astype(str).tolist()

# =========================
# GUARDADO TEMPORAL
# =========================
if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame()

def guardar_historial(data):
    df_nuevo = pd.DataFrame([data])
    st.session_state.historial = pd.concat(
        [st.session_state.historial, df_nuevo],
        ignore_index=True
    )
    st.success("Guardado en sesión (cloud ready)")

# =========================
# ANALISIS
# =========================
def generar_analisis(nombre, prioridad, complejidad, tipo, roi, fte):
    return f"""
**Resumen Ejecutivo**

La iniciativa **{nombre}** presenta:

- Prioridad: **{prioridad:.2f}**
- Complejidad: **{complejidad:.2f}**
- ROI: **{roi:.2f}**

Clasificación: **{tipo}**

FTE estimado: **{fte:.2f}**

Recomendación:
Alinear la ejecución según impacto vs esfuerzo.
"""

# =========================
# COLORES
# =========================
def color_tipo(tipo):
    colores = {
        "Quick Win": "🟢",
        "Estratégico": "🔵",
        "Opcional": "🟡",
        "Descartar": "🔴"
    }
    return colores.get(tipo, "⚪")

# =========================
# UI
# =========================
tab1, tab2 = st.tabs(["Evaluador", "Info"])

# =========================
# TAB 1
# =========================
with tab1:

    st.title("Evaluador de Iniciativas")

    archivo = obtener_archivo()
    st.success("Archivo cargado correctamente")

    inicializar_excel()

    if st.button("Actualizar backlog"):
        st.cache_data.clear()
        st.rerun()

    opciones = cargar_backlog(archivo)

    if not opciones:
        st.warning("Backlog vacío")
        st.stop()

    col_left, col_right = st.columns([2,1])

    # =========================
    # IZQUIERDA
    # =========================
    with col_left:

        nombre = st.selectbox("Selecciona iniciativa", opciones)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Prioridad")
            p1 = st.slider("Impacto ingresos", 1, 5, 3)
            p2 = st.slider("Riesgos", 1, 5, 3)
            p3 = st.slider("Eficiencia", 1, 5, 3)

        with col2:
            st.subheader("Complejidad")
            c1 = st.slider("Nivel técnico", 1, 5, 3)
            c2 = st.slider("Dependencias", 1, 5, 3)
            c3 = st.slider("Tiempo", 1, 5, 3)

        st.subheader("🏭 Variables Operativas")

        horas = st.number_input("Horas mensuales", min_value=0.0, value=176.0)
        fte = horas / 176

        st.metric("FTE estimado", f"{fte:.2f}")

        repetitivo = st.selectbox("Proceso repetitivo", ["Alto", "Medio", "Bajo"])
        estandarizado = st.selectbox("Proceso estandarizado", ["Sí", "No"])
        volumen = st.selectbox("Volumen", ["Alto", "Medio", "Bajo"])
        errores = st.selectbox("Errores manuales", ["Alto", "Medio", "Bajo"])

        score_map = {"Alto":5, "Medio":3, "Bajo":1}
        bool_map = {"Sí":5, "No":1}

        prioridad = (p1 + p2 + p3 + score_map[volumen] + score_map[errores]) / 5
        complejidad = (c1 + c2 + c3 + (6 - bool_map[estandarizado]) + (6 - score_map[repetitivo])) / 5

        # CLASIFICACIÓN
        if prioridad >= 4 and complejidad <= 2:
            tipo = "Quick Win"
        elif prioridad >= 4:
            tipo = "Estratégico"
        elif complejidad <= 2:
            tipo = "Opcional"
        else:
            tipo = "Descartar"

        roi = prioridad / complejidad

        st.markdown(f"""
### {color_tipo(tipo)} Tipo: **{tipo}**
### ROI: **{roi:.2f}**
""")

        colb1, colb2 = st.columns(2)

        with colb1:
            if st.button("Analizar"):
                texto = generar_analisis(nombre, prioridad, complejidad, tipo, roi, fte)
                st.info(texto)

        with colb2:
            if st.button("Guardar"):
                data = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre,
                    "Prioridad": prioridad,
                    "Complejidad": complejidad,
                    "Tipo": tipo,
                    "ROI": roi,
                    "FTE": fte,
                    "Horas": horas
                }
                guardar_historial(data)

        # DESCARGA
        if not st.session_state.historial.empty:
            st.download_button(
                "⬇️ Descargar historial",
                st.session_state.historial.to_csv(index=False),
                "historial.csv",
                "text/csv"
            )

    # =========================
    # DERECHA (GRÁFICO)
    # =========================
    with col_right:

        fig, ax = plt.subplots()

        ax.scatter(complejidad, prioridad, s=250)

        ax.axhline(3, linestyle='--')
        ax.axvline(3, linestyle='--')

        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)

        ax.set_xlabel("Complejidad")
        ax.set_ylabel("Prioridad")

        ax.set_title("Matriz de Priorización")

        st.pyplot(fig)

# =========================
# TAB 2
# =========================
with tab2:

    st.title("Información")

    st.markdown("""
Esta herramienta permite evaluar iniciativas considerando:

- Impacto (prioridad)
- Esfuerzo (complejidad)
- Variables operativas

Clasificación:

- Quick Wins → alto impacto / bajo esfuerzo
- Estratégico → alto impacto / alto esfuerzo
- Opcional → bajo impacto / bajo esfuerzo
- Descartar → bajo impacto / alto esfuerzo
""")