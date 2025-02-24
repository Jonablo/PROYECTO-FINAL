import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction

def metodo_voguel(oferta, demanda, costos):
    filas, columnas = len(oferta), len(demanda)
    asignacion = np.zeros((filas, columnas), dtype=object)
    oferta = oferta.copy()
    demanda = demanda.copy()
    costos = costos.astype(object)
    
    while np.any(oferta > 0) and np.any(demanda > 0):
        # Evitar errores si todas las celdas son inf
        diferencias_filas = []
        diferencias_columnas = []

        for row in costos:
            valores_validos = row[row != np.inf]
            if len(valores_validos) > 1:
                dif = sorted(valores_validos)[:2]
            elif len(valores_validos) == 1:
                dif = [valores_validos[0], valores_validos[0]]
            else:
                dif = [0, 0]
            diferencias_filas.append(dif)

        for col in costos.T:
            valores_validos = col[col != np.inf]
            if len(valores_validos) > 1:
                dif = sorted(valores_validos)[:2]
            elif len(valores_validos) == 1:
                dif = [valores_validos[0], valores_validos[0]]
            else:
                dif = [0, 0]
            diferencias_columnas.append(dif)

        dif_filas = np.array([b - a for a, b in diferencias_filas])
        dif_columnas = np.array([b - a for a, b in diferencias_columnas])

        max_fila = np.nanmax(dif_filas)
        max_columna = np.nanmax(dif_columnas)

        if max_fila >= max_columna:
            fila = np.nanargmax(dif_filas)
            col = np.nanargmin(costos[fila])
        else:
            col = np.nanargmax(dif_columnas)
            fila = np.nanargmin(costos[:, col])

        asignado = min(oferta[fila], demanda[col])
        asignacion[fila, col] = asignado
        oferta[fila] -= asignado
        demanda[col] -= asignado

        if oferta[fila] == 0:
            costos[fila, :] = np.inf
        if demanda[col] == 0:
            costos[:, col] = np.inf

    return asignacion

st.title("Optimización de Transporte - Método de Voguel")

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
matrix_data = np.zeros((st.session_state.num_fuentes + 1, st.session_state.num_destinos + 1))
matrix_df = pd.DataFrame(matrix_data, columns=column_names, index=index_names)

matrix_df = st.data_editor(matrix_df, key="matriz_transporte")

if st.button("Resolver"):
    matrix_df = matrix_df.map(lambda x: Fraction(str(x)) if str(x).strip() else Fraction(0))
    costos = matrix_df.iloc[:-1, :-1].values
    oferta = matrix_df.iloc[:-1, -1].values
    demanda = matrix_df.iloc[-1, :-1].values

    # Verificar si está balanceado
    total_oferta = sum(oferta)
    total_demanda = sum(demanda)

    if total_oferta > total_demanda:
        # Agregar un destino ficticio con costo 0 y demanda igual a la diferencia
        demanda = np.append(demanda, total_oferta - total_demanda)
        costos = np.column_stack((costos, np.zeros((costos.shape[0], 1))))
    elif total_demanda > total_oferta:
        # Agregar una fuente ficticia con costo 0 y oferta igual a la diferencia
        oferta = np.append(oferta, total_demanda - total_oferta)
        costos = np.vstack((costos, np.zeros((1, costos.shape[1]))))  # Se usa np.vstack en lugar de np.row_stack

    asignacion = metodo_voguel(oferta, demanda, costos)
    costo_total = sum(asignacion[i, j] * costos[i, j] for i in range(len(oferta)) for j in range(len(demanda)) if asignacion[i, j] != 0)
    
    resultado_df = pd.DataFrame(asignacion, columns=[f"Destino {j+1}" for j in range(len(demanda))], index=[f"Fuente {i+1}" for i in range(len(oferta))])
    
    st.subheader("Asignación de Transporte")
    st.dataframe(resultado_df)
    st.write(f"**Costo Total del Transporte:** {costo_total}")
