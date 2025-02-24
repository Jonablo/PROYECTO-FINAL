import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction

def calcular_costos_reducidos(costos, u, v):
    filas, columnas = costos.shape
    costos_reducidos = np.full((filas, columnas), None)
    for i in range(filas):
        for j in range(columnas):
            if u[i] is not None and v[j] is not None:
                costos_reducidos[i, j] = costos[i, j] - (u[i] + v[j])
    return costos_reducidos

def metodo_modi(costos, asignacion):
    filas, columnas = costos.shape
    u = np.full(filas, None)
    v = np.full(columnas, None)
    u[0] = 0  # Inicializar la primera fila con 0
    
    while None in u or None in v:
        for i in range(filas):
            for j in range(columnas):
                if asignacion[i, j] != 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = costos[i, j] - u[i]
                    elif v[j] is not None and u[i] is None:
                        u[i] = costos[i, j] - v[j]
    
    costos_reducidos = calcular_costos_reducidos(costos, u, v)
    if all(costo is None or costo >= 0 for costo in costos_reducidos.flatten()):
        return asignacion, sum(asignacion[i, j] * costos[i, j] for i in range(filas) for j in range(columnas) if asignacion[i, j] != 0)
    
    return asignacion, sum(asignacion[i, j] * costos[i, j] for i in range(filas) for j in range(columnas) if asignacion[i, j] != 0)

def obtener_asignacion_inicial(oferta, demanda, costos):
    filas, columnas = len(oferta), len(demanda)
    asignacion = np.zeros((filas, columnas), dtype=object)
    oferta = oferta.copy()
    demanda = demanda.copy()
    
    while np.any(oferta > 0) and np.any(demanda > 0):
        i, j = np.unravel_index(np.argmin(costos), costos.shape)
        asignado = min(oferta[i], demanda[j])
        asignacion[i, j] = asignado
        oferta[i] -= asignado
        demanda[j] -= asignado
        
        if oferta[i] == 0:
            costos[i, :] = np.inf
        if demanda[j] == 0:
            costos[:, j] = np.inf
    
    return asignacion

st.title("Optimización de Transporte - Método MODI")

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

if st.button("Optimizar con MODI"):
    matrix_df = matrix_df.map(lambda x: Fraction(str(x)) if str(x).strip() else Fraction(0))
    costos = matrix_df.iloc[:-1, :-1].values
    oferta = matrix_df.iloc[:-1, -1].values
    demanda = matrix_df.iloc[-1, :-1].values
    
    asignacion_inicial = obtener_asignacion_inicial(oferta, demanda, costos.copy())
    asignacion_optima, costo_total = metodo_modi(costos, asignacion_inicial)
    
    resultado_df = pd.DataFrame(asignacion_optima, columns=column_names[:-1], index=index_names[:-1])
    
    st.subheader("Asignación Óptima de Transporte")
    st.dataframe(resultado_df)
    st.write(f"**Costo Total del Transporte:** {costo_total}")
