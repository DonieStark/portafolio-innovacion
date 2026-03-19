import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import json

st.set_page_config(page_title="Portafolio de Innovación", layout="wide")

# =========================
# CONFIG
# =========================
CONFIG_FILE = "config.json"

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"ruta_excel": ""}

def guardar_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = cargar_config()
ruta_excel = config.get("ruta_excel", "")

# =========================
# RUTA
# =========================
def obtener_archivo():
    if ruta_excel:
        ruta = os.path.normpath(ruta_excel.strip())
        return os.path.join(ruta, "iniciativas.xlsx")
    return "iniciativas.xlsx"

# =========================
# VALIDAR EXCEL
# =========================
def inicializar_excel():
    archivo = obtener_archivo()
    if not os.path.isfile(archivo):
        st.error(f"El archivo no existe: {archivo}")
        st.stop()

# =========================
# BACKLOG
# =========================
@st.cache_data
def cargar_backlog():
    archivo = obtener_archivo()
    df = pd.read_excel(archivo, sheet_name="Backlog")

    if "Nombre" in df.columns:
        return df["Nombre"].dropna().astype(str).tolist()
    else:
        return df.iloc[:, 0].dropna().astype(str).tolist()

# =========================
# GUARDAR
# =========================
def guardar_excel(data):
    archivo = obtener_archivo()

    try:
        df_nuevo = pd.DataFrame([data])

        try:
            df_historial = pd.read_excel(archivo, sheet_name="Historial")
        except:
            df_historial = pd.DataFrame()

        df_backlog = pd.read_excel(archivo, sheet_name="Backlog")

        df_final = pd.concat([df_historial, df_nuevo], ignore_index=True)

        with pd.ExcelWriter(archivo, engine="openpyxl", mode="w") as writer:
            df_final.to_excel(writer, sheet_name="Historial", index=False)
            df_backlog.to_excel(writer, sheet_name="Backlog", index=False)

        st.success("Evaluación guardada correctamente")

    except PermissionError:
        st.error("Cierra el archivo Excel")
    except Exception as e:
        st.error(f"Error: {e}")

# =========================
# ANALISIS DETALLADO
# =========================
def generar_analisis(nombre, prioridad, complejidad, tipo, roi, fte, repetitivo, estandarizado, volumen, errores, criticidad):
    return f"""
El proyecto "{nombre}" ha sido evaluado considerando variables cuantitativas y cualitativas.

En términos de prioridad, el proyecto presenta un puntaje de {prioridad:.2f}, lo que indica su nivel de impacto en el negocio considerando ingresos, riesgos, eficiencia y factores operativos.

Desde el punto de vista de complejidad, el puntaje obtenido es {complejidad:.2f}, lo cual refleja el esfuerzo técnico, dependencias y tiempo requerido para su implementación.

El tipo de iniciativa se clasifica como "{tipo}", con un retorno estimado (ROI) de {roi:.2f}.

Adicionalmente, el análisis operativo muestra:
- FTE estimado: {fte:.2f}
- Repetitividad del proceso: {repetitivo}
- Nivel de estandarización: {estandarizado}
- Volumen operativo: {volumen}
- Nivel de errores manuales: {errores}
- Criticidad del proceso: {criticidad}

Este conjunto de variables permite concluir que el proyecto tiene un nivel de viabilidad acorde a su impacto y esfuerzo, y su priorización debe alinearse con la estrategia operativa y disponibilidad de recursos.
"""

# =========================
# UI
# =========================
tab1, tab2 = st.tabs(["Evaluador", "Configuración"])

# =========================
# TAB 1
# =========================
with tab1:

    st.title("Evaluador de Iniciativas")

    archivo_actual = obtener_archivo()
    st.success(f"Archivo activo: {archivo_actual}")

    inicializar_excel()

    if st.button("Actualizar backlog", key="refresh"):
        st.cache_data.clear()
        st.rerun()

    opciones = cargar_backlog()

    if not opciones:
        st.warning("Backlog vacío")
        st.stop()

    col_left, col_right = st.columns([2,1])

    # =========================
    # IZQUIERDA
    # =========================
    with col_left:

        nombre = st.selectbox("Iniciativa", opciones)

        col1, col2 = st.columns(2)

        # PRIORIDAD
        with col1:
            st.subheader("Prioridad")
            p1 = st.slider("Impacto ingresos", 1, 5, 3)
            p2 = st.slider("Riesgos", 1, 5, 3)
            p3 = st.slider("Eficiencia", 1, 5, 3)

        # COMPLEJIDAD
        with col2:
            st.subheader("Complejidad")
            c1 = st.slider("Nivel técnico", 1, 5, 3)
            c2 = st.slider("Dependencias", 1, 5, 3)
            c3 = st.slider("Tiempo", 1, 5, 3)

        # NUEVOS INPUTS
        st.subheader("Variables Operativas")

        horas = st.number_input("Horas mensuales", min_value=0.0, value=176.0)
        fte = horas / 176
        st.write(f"FTE estimado: {fte:.2f}")

        repetitivo = st.selectbox("Proceso repetitivo", ["Alto", "Medio", "Bajo"])
        estandarizado = st.selectbox("Proceso estandarizado", ["Sí", "No"])
        volumen = st.selectbox("Volumen", ["Alto", "Medio", "Bajo"])
        errores = st.selectbox("Errores manuales", ["Alto", "Medio", "Bajo"])
        criticidad = st.selectbox("Criticidad", ["Alta", "Media", "Baja"])

        # CONVERSIÓN A SCORE
        score_map = {"Alto":5, "Medio":3, "Bajo":1}
        bool_map = {"Sí":5, "No":1}

        prioridad = (p1 + p2 + p3 + score_map[volumen] + score_map[errores]) / 5
        complejidad = (c1 + c2 + c3 + (6 - bool_map[estandarizado]) + (6 - score_map[repetitivo])) / 5

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
        Tipo: {tipo}  
        ROI: {roi:.2f}
        """)

        colb1, colb2 = st.columns(2)

        with colb1:
            if st.button("Analizar", key="analizar"):
                texto = generar_analisis(nombre, prioridad, complejidad, tipo, roi, fte, repetitivo, estandarizado, volumen, errores, criticidad)
                st.info(texto)

        with colb2:
            if st.button("Guardar", key="guardar"):
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
                guardar_excel(data)

    # =========================
    # DERECHA (GRÁFICO)
    # =========================
    with col_right:

        fig, ax = plt.subplots()

        ax.scatter(complejidad, prioridad, s=200)

        ax.axhline(3, linestyle='--')
        ax.axvline(3, linestyle='--')

        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)

        ax.set_xlabel("Complejidad")
        ax.set_ylabel("Prioridad")

        st.pyplot(fig)

# =========================
# TAB 2
# =========================
with tab2:

    st.title("Configuración")

    nueva_ruta = st.text_input("Ruta del Excel", value=ruta_excel)

    if st.button("Guardar configuración", key="config"):
        config["ruta_excel"] = nueva_ruta.strip()
        guardar_config(config)
        st.success("Configuración guardada")
        st.rerun()

# DEBUG
st.write("Ruta:", ruta_excel)
st.write("Archivo:", obtener_archivo())
st.write("Existe:", os.path.isfile(obtener_archivo()))