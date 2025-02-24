import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Configurar página en modo ancho
st.set_page_config(layout="wide")

st.title("Cálculo del Árbol de Expansión Mínima")

# Crear columnas principales
col1, col2, col3 = st.columns([1.5, 2.5, 2])

# Columna 1 - Ingreso de Datos
with col1:
    st.markdown("""
    **Ingrese las conexiones en el siguiente formato:**  
    **Nodo1 Nodo2 Peso**  
    **Ejemplo:**  
    `O A 2`  
    `O B 5`  
    `A B 2`  
    `B D 4`
    """)

    entrada_texto = st.text_area("", height=150, placeholder="Ejemplo:\nO A 2\nO B 5\nA B 2\nB D 4")

    if st.button("Procesar Datos", use_container_width=True):
        # Procesar la entrada del usuario
        lineas = entrada_texto.strip().split("\n")
        conexiones = []

        for linea in lineas:
            partes = linea.split()
            if len(partes) == 3:
                nodo1, nodo2, peso = partes
                try:
                    peso = float(peso)  # Convertir a número
                    conexiones.append((nodo1, nodo2, peso))
                except ValueError:
                    st.error(f"Error en la línea: {linea} (peso inválido)")
        
        # Guardar en la sesión
        if conexiones:
            st.session_state.conexiones = conexiones
            st.success("Datos procesados correctamente.")
            st.rerun()

# Columna 2 - Tabla de Conexiones + Cálculo de MST
with col2:
    st.subheader("Tabla de Conexiones")
    if "conexiones" in st.session_state and st.session_state.conexiones:
        df = pd.DataFrame(st.session_state.conexiones, columns=["Nodo 1", "Nodo 2", "Peso"])
        st.dataframe(df, hide_index=True, height=250, use_container_width=True)

        # Botón para calcular el MST
        if st.button("Calcular Árbol de Expansión Mínima", use_container_width=True):
            # Construir el grafo
            G = nx.Graph()
            for n1, n2, w in st.session_state.conexiones:
                G.add_edge(n1, n2, weight=w)

            # Calcular el MST con Kruskal
            MST = nx.minimum_spanning_tree(G, algorithm="kruskal")

            # Obtener el costo total del MST
            costo_total = sum(d["weight"] for _, _, d in MST.edges(data=True))

            # Guardar en la sesión y mostrar resultados
            st.session_state.mst = MST
            st.success(f"El costo total del Árbol de Expansión Mínima es: {costo_total}")

# Columna 3 - Grafo con MST
with col3:
    st.subheader("Árbol de Expansión Mínima")

    if "mst" in st.session_state:
        G = nx.Graph()
        for n1, n2, w in st.session_state.conexiones:
            G.add_edge(n1, n2, weight=w)

        MST = st.session_state.mst

        fig, ax = plt.subplots(figsize=(4.5, 4))
        pos = nx.shell_layout(G)  # Distribución ordenada de nodos

        # Dibujar todo el grafo en gris
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=12, ax=ax)

        # Resaltar el MST en verde
        nx.draw(MST, pos, with_labels=True, node_color="lightblue", edge_color="green", width=2, node_size=2000, font_size=12, ax=ax)
        
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=10, ax=ax)

        st.pyplot(fig)
