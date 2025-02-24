import streamlit as st

st.set_page_config(page_title="Optimización Operativa", layout="wide")

st.title("Aplicación de Optimización Operativa")

st.sidebar.header("Selecciona un método:")

# Lista de métodos
modulos = {
    "Programación Lineal (Simplex)": "app",
    "Método de Transporte - Costo Mínimo": "transporteCmin",
    "Método de Transporte - Esquina Noroeste": "transportEn",
    "Método de Transporte - Voguel": "transpVoguel",
    "Redes - Ruta Más Corta": "Ruta+corta",
    "Redes - Árbol de Expansión Mínima": "arbolEM",
    "Redes - Flujo Máximo": "flujoMax",
    "Método de Distribución - Modi": "modi",
}

# Opción seleccionada
opcion = st.sidebar.radio("Métodos de Optimización", list(modulos.keys()))

# Ejecutar el módulo correspondiente
if opcion:
    script = modulos[opcion]
    st.subheader(f"🔍 Método Seleccionado: {opcion}")

    # Importar y ejecutar el módulo dinámicamente
    exec(f"import {script}")  # Cargar el módulo
    exec(f"{script}.main()")  # Llamar a la función `main()` del módulo
