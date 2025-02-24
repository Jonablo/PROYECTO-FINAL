import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction

# Función para resolver el problema de Costo Mínimo
def costo_minimo(oferta, demanda, costos):
    filas, columnas = len(oferta), len(demanda)
    asignacion = np.zeros((filas, columnas), dtype=object)
    
    # Convertir a fracciones seguras
    oferta = list(map(Fraction, oferta))
    demanda = list(map(Fraction, demanda))
    costos = np.array([[Fraction(str(c)) for c in row] for row in costos], dtype=object)

    # Usamos un número muy grande para simular "infinito" en costos
    INFINITO = Fraction(9999999, 1)

    while any(oferta) and any(demanda):
        # Evitar errores si hay valores bloqueados (reemplazamos None)
        costos_temp = np.where(costos == None, INFINITO, costos)

        # Encontrar la celda con menor costo
        min_idx = np.unravel_index(np.argmin(costos_temp), costos.shape)
        i, j = min_idx

        # Asignar la cantidad mínima posible
        asignado = min(oferta[i], demanda[j])
        asignacion[i, j] = asignado
        oferta[i] -= asignado
        demanda[j] -= asignado

        # Bloquear fila/columna cuando se llena
        if oferta[i] == 0:
            costos[i, :] = [INFINITO] * columnas
        if demanda[j] == 0:
            costos[:, j] = [INFINITO] * filas
    
    return asignacion

# Configuración de la Interfaz en Streamlit
st.title("Optimización de Transporte - Método de Costo Mínimo")

if "num_fuentes" not in st.session_state:
    st.session_state.num_fuentes = 3
if "num_destinos" not in st.session_state:
    st.session_state.num_destinos = 3

def update_model():
    st.session_state.num_fuentes = st.session_state.new_num_fuentes
    st.session_state.num_destinos = st.session_state.new_num_destinos

with st.form("configuracion"):
    st.subheader("Definir el Problema de Transporte")
    st.session_state.new_num_fuentes = st.number_input("Cantidad de Fuentes:", min_value=1, step=1, value=st.session_state.num_fuentes, key="fuentes")
    st.session_state.new_num_destinos = st.number_input("Cantidad de Destinos:", min_value=1, step=1, value=st.session_state.num_destinos, key="destinos")
    if st.form_submit_button("Actualizar Modelo"):
        update_model()
        st.rerun()

st.subheader("Ingrese la Matriz de Costos, Oferta y Demanda")
column_names = [f"Destino {j+1}" for j in range(st.session_state.num_destinos)] + ["Suministro"]
index_names = [f"Fuente {i+1}" for i in range(st.session_state.num_fuentes)] + ["Demanda"]
matrix_data = np.zeros((st.session_state.num_fuentes + 1, st.session_state.num_destinos + 1), dtype=object)
matrix_df = pd.DataFrame(matrix_data, columns=column_names, index=index_names)

matrix_df = st.data_editor(matrix_df, key="matriz_transporte")

if st.button("Resolver"):
    matrix_df = matrix_df.map(lambda x: Fraction(str(x)) if str(x).strip() else Fraction(0))  # Convertir a fracciones
    costos = matrix_df.iloc[:-1, :-1].values
    oferta = matrix_df.iloc[:-1, -1].values
    demanda = matrix_df.iloc[-1, :-1].values

    asignacion = costo_minimo(oferta, demanda, costos)
    costo_total = sum(asignacion[i, j] * costos[i, j] for i in range(len(oferta)) for j in range(len(demanda)))

    resultado_df = pd.DataFrame(asignacion, columns=column_names[:-1], index=index_names[:-1])
    resultado_df["Suministro"] = list(map(str, oferta))  # Convertir fracciones a string
    resultado_df.loc["Demanda"] = list(map(str, demanda)) + [""]

    st.subheader("Asignación de Transporte")
    st.dataframe(resultado_df)
    st.write(f"**Costo Total del Transporte:** {costo_total}")
