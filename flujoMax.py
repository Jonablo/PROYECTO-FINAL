import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Configurar página en modo ancho
st.set_page_config(layout="wide")

st.title("Cálculo del Flujo Máximo")

# Crear columnas principales
col1, col2, col3 = st.columns([1.5, 2.5, 2])

# Columna 1 - Ingreso de Datos
with col1:
    st.markdown("""
    **Ingrese las conexiones en el siguiente formato:**  
    **Nodo1 Nodo2 Capacidad**  
    **Ejemplo:**  
    `O A 5`  
    `O B 7`  
    `A C 3`  
    `B C 4`
    """)

    entrada_texto = st.text_area("", height=150, placeholder="Ejemplo:\nO A 5\nO B 7\nA C 3\nB C 4")

    if st.button("Procesar Datos", use_container_width=True):
        # Procesar la entrada del usuario
        lineas = entrada_texto.strip().split("\n")
        conexiones = []

        for linea in lineas:
            partes = linea.split()
            if len(partes) == 3:
                nodo1, nodo2, capacidad = partes
                try:
                    capacidad = float(capacidad)  # Convertir a número
                    conexiones.append((nodo1, nodo2, capacidad))
                except ValueError:
                    st.error(f"Error en la línea: {linea} (capacidad inválida)")
        
        # Guardar en la sesión
        if conexiones:
            st.session_state.conexiones = conexiones
            st.success("Datos procesados correctamente.")
            st.rerun()

# Columna 2 - Tabla de Conexiones + Cálculo de Flujo Máximo
with col2:
    st.subheader("Tabla de Conexiones")
    if "conexiones" in st.session_state and st.session_state.conexiones:
        df = pd.DataFrame(st.session_state.conexiones, columns=["Nodo 1", "Nodo 2", "Capacidad"])
        st.dataframe(df, hide_index=True, height=250, use_container_width=True)

        # Selección de nodos de inicio y destino
        nodos = set(df["Nodo 1"]).union(set(df["Nodo 2"]))
        origen = st.selectbox("Nodo de Origen:", list(nodos), index=0)
        destino = st.selectbox("Nodo de Destino:", list(nodos), index=len(nodos) - 1)

        # Botón para calcular el Flujo Máximo
        if st.button("Calcular Flujo Máximo", use_container_width=True):
            # Construir el grafo dirigido con capacidades
            G = nx.DiGraph()
            for n1, n2, cap in st.session_state.conexiones:
                G.add_edge(n1, n2, capacity=cap)

            # Calcular el flujo máximo con Ford-Fulkerson
            flujo_max, flujo_detalle = nx.maximum_flow(G, origen, destino)

            # Guardar en la sesión y mostrar resultados
            st.session_state.flujo_max = flujo_max
            st.session_state.flujo_detalle = flujo_detalle
            st.success(f"El flujo máximo de {origen} a {destino} es: {flujo_max}")

# Columna 3 - Grafo con Flujo Máximo
with col3:
    st.subheader("Red de Flujo Máximo")

    if "flujo_max" in st.session_state:
        G = nx.DiGraph()
        for n1, n2, cap in st.session_state.conexiones:
            G.add_edge(n1, n2, capacity=cap, flow=st.session_state.flujo_detalle[n1][n2])

        fig, ax = plt.subplots(figsize=(4.5, 4))
        pos = nx.spring_layout(G)  # Distribución de nodos

        # Dibujar el grafo con capacidades
        edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G.edges(data=True)}
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=12, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=10, ax=ax)

        st.pyplot(fig)
