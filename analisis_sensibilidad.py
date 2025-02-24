import shap
import numpy as np
import streamlit as st

# Diccionario para almacenar análisis de sensibilidad de cada módulo
if "analisis_global" not in st.session_state:
    st.session_state.analisis_global = {}

def analizar_sensibilidad(tipo_problema, modelo, datos):
    """
    Aplica SHAP para el análisis de sensibilidad del modelo de optimización.

    Parámetros:
    - tipo_problema: str, indica el tipo de problema ("simplex", "transporte", "redes").
    - modelo: función que resuelve el problema de optimización.
    - datos: lista con los parámetros del problema.

    Retorna:
    - Importancia de cada variable en la solución final.
    """
    
    st.subheader(f"🔍 Análisis de Sensibilidad - {tipo_problema.upper()}")

    # Convertir datos a formato numérico
    datos_np = np.array(datos, dtype=float)

    # Crear explicador SHAP
    explicador = shap.Explainer(modelo, datos_np)
    shap_values = explicador(datos_np)

    # Guardar resultados en el estado de sesión
    st.session_state.analisis_global[tipo_problema] = shap_values

    # Mostrar análisis en Streamlit
    st.write("### Importancia de Variables:")
    st.pyplot(shap.summary_plot(shap_values, datos_np))

    return shap_values
