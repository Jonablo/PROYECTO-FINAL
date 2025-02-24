import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Configurar página en modo ancho
st.set_page_config(layout="wide")

st.title("Cálculo de Ruta Más Corta")

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

# Columna 2 - Tabla de Conexiones + Sección de Cálculo (Juntas)
with col2:
    st.subheader("Tabla de Conexiones")
    if "conexiones" in st.session_state and st.session_state.conexiones:
        df = pd.DataFrame(st.session_state.conexiones, columns=["Nodo 1", "Nodo 2", "Peso"])
        st.dataframe(df, hide_index=True, height=250, use_container_width=True)

        # Sección de Cálculo - Justo debajo de la tabla
        col4, col5 = st.columns([1, 1])
        with col4:
            st.subheader("Nodo de Inicio")
            nodo_inicio = st.selectbox("", list(df["Nodo 1"].unique()), key="inicio", label_visibility="collapsed")

        with col5:
            st.subheader("Nodo de Destino")
            nodo_fin = st.selectbox("", list(df["Nodo 2"].unique()), key="fin", label_visibility="collapsed")

        # Botón y resultados alineados
        col6, col7, col8 = st.columns([1, 2, 1])
        with col7:
            if st.button("Calcular Ruta Más Corta", use_container_width=True):
                # Construir el grafo para calcular la ruta
                G = nx.Graph()
                for n1, n2, w in st.session_state.conexiones:
                    G.add_edge(n1, n2, weight=w)

                if nodo_inicio != nodo_fin:
                    ruta = nx.shortest_path(G, source=nodo_inicio, target=nodo_fin, weight="weight")
                    distancia = nx.shortest_path_length(G, source=nodo_inicio, target=nodo_fin, weight="weight")

                    st.success(f"Ruta más corta: {' → '.join(ruta)}")
                    st.info(f"Distancia total: {distancia}")

# Columna 3 - Grafo
with col3:
    st.subheader("Representación del Grafo")
    
    if "conexiones" in st.session_state and st.session_state.conexiones:
        G = nx.Graph()
        for n1, n2, w in st.session_state.conexiones:
            G.add_edge(n1, n2, weight=w)

        fig, ax = plt.subplots(figsize=(4.5, 4))
        pos = nx.shell_layout(G)  # Distribución ordenada de nodos

        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=12, ax=ax)
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=10, ax=ax)

        st.pyplot(fig)
