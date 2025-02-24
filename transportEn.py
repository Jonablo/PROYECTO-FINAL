import numpy as np
import streamlit as st
import pandas as pd

def esquina_noroeste(oferta, demanda, costos):
    filas, columnas = len(oferta), len(demanda)
    asignacion = np.zeros((filas, columnas))
    i, j = 0, 0
    
    while i < filas and j < columnas:
        asignado = min(oferta[i], demanda[j])
        asignacion[i, j] = asignado
        oferta[i] -= asignado
        demanda[j] -= asignado
        
        if oferta[i] == 0:
            i += 1
        if demanda[j] == 0:
            j += 1
    
    return asignacion

st.title("Método de Esquina Noroeste - Problema de Transporte")

# Selección de tamaño del problema
num_fuentes = st.number_input("Número de fuentes (plantas):", min_value=1, step=1, value=3)
num_destinos = st.number_input("Número de destinos (ciudades):", min_value=1, step=1, value=3)

# Ingreso de matriz de costos, oferta y demanda
st.subheader("Ingrese la Matriz de Costos, Oferta y Demanda")

column_names = [f"Destino {j+1}" for j in range(num_destinos)] + ["Suministro"]
index_names = [f"Fuente {i+1}" for i in range(num_fuentes)] + ["Demanda"]

# Matriz de entrada
matriz = np.zeros((num_fuentes + 1, num_destinos + 1))

def input_matrix():
    df = pd.DataFrame(matriz, columns=column_names, index=index_names)
    edited_df = st.data_editor(df, key="matriz_input")
    return edited_df.to_numpy()

matriz = input_matrix()

if st.button("Resolver"):
    oferta = matriz[:-1, -1].tolist()
    demanda = matriz[-1, :-1].tolist()
    costos = matriz[:-1, :-1]
    resultado = esquina_noroeste(oferta, demanda, costos)
    costo_total = (resultado * costos).sum()
    
    st.subheader("Asignación de Transporte")
    st.write(pd.DataFrame(resultado, columns=column_names[:-1], index=index_names[:-1]))
    
    st.write(f"**Costo Total del Transporte:** {costo_total}")
