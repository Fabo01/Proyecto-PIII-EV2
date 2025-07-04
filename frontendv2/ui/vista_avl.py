"""
Vista para análisis de rutas más frecuentes (AVL) de la simulación.
Cumple con la Pestaña 4: Análisis de rutas más frecuentes del documento de Requisitos.md
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from frontendv2.servicios.cache import inicializar_snapshot_datos
from frontendv2.ui.utils import boton_actualizar_datos


def mostrar():
    """
    Pestaña 4: Análisis de rutas más frecuentes (AVL).
    Componentes:
    - Lista: rutas más frecuentes (clave = camino, valor = frecuencia).
    - Gráfico: visualización del árbol AVL con etiquetas "A -> B -> C\nFreq: X" usando networkx.
    """
    st.header("Análisis de rutas más frecuentes (AVL)")
    boton_actualizar_datos(key_suffix="_avl")
    st.info("Visualiza las rutas más utilizadas registradas en una estructura AVL.")
    
    # Dependencia del snapshot único de datos
    if 'datos_red' not in st.session_state:
        st.warning("No hay datos disponibles. Inicia la simulación primero.")
        return
    
    datos = st.session_state['datos_red']
    estad = datos.get('estadisticas', {}) or {}
    rutas = estad.get('rutas_mas_frecuentes', [])
    # Calcular métricas adicionales
    total_unicas = estad.get('total_rutas_unicas', len(rutas))
    total_usos = sum(r.get('frecuencia', 1) for r in rutas)
    prom_freq = round(total_usos / total_unicas, 2) if total_unicas > 0 else 0.0
    longitudes = [len(r.get('camino', [])) for r in rutas]
    prom_long = round(sum(longitudes) / len(longitudes), 2) if longitudes else 0.0
    max_freq = max((r.get('frecuencia', 1) for r in rutas), default=0)
    min_freq = min((r.get('frecuencia', 1) for r in rutas), default=0)
    # Mostrar métricas de rutas frecuentes
    st.subheader("Métricas de rutas frecuentes")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rutas únicas", total_unicas)
    col2.metric("Total usos", total_usos)
    col3.metric("Freq. promedio", f"{prom_freq:.2f}")
    col4.metric("Longitud promedio", f"{prom_long:.2f}")
    st.markdown("---")
    # Tabla de rutas
    st.subheader("Detalle de rutas frecuentes")
    tabla = []
    for r in rutas:
        camino = ' → '.join(str(n) for n in r.get('camino', []))
        freq = r.get('frecuencia', 1)
        tabla.append({'Camino': camino, 'Frecuencia': freq})
    df = pd.DataFrame(tabla)
    if df.empty:
        st.info("No hay rutas frecuentes registradas.")
    else:
        st.table(df)
        # Gráfico de barras
        st.subheader("Gráfico de rutas frecuentes")
        df_plot = df.set_index('Camino')
        st.bar_chart(df_plot)

    # Visualización del árbol AVL (usando networkx)
    st.subheader("Visualización del árbol AVL")
    import networkx as nx
    from collections import deque

    # Construir un árbol binario balanceado a partir de la lista de rutas ordenadas (inorden)
    nodes = []  # lista de (etiqueta, frecuencia)
    for r in rutas:
        caminostr = ' → '.join(str(n) for n in r.get('camino', []))
        freq = r.get('frecuencia', 1)
        label = f"{caminostr}\nFreq: {freq}"
        nodes.append((label, freq))
    # Función recursiva para insertar nodos en un grafo dirigido
    def build_tree(lst, g, parent=None):
        if not lst:
            return
        mid = len(lst) // 2
        label, _ = lst[mid]
        g.add_node(label)
        if parent:
            g.add_edge(parent, label)
        # construir subárbol izquierdo y derecho
        build_tree(lst[:mid], g, label)
        build_tree(lst[mid+1:], g, label)

    G_avl = nx.DiGraph()
    build_tree(nodes, G_avl)
    if G_avl.nodes:
        fig, ax = plt.subplots(figsize=(6, 6))
        pos = nx.spring_layout(G_avl, seed=42)
        nx.draw(G_avl, pos, with_labels=True, node_size=2000, font_size=8, ax=ax)
        st.pyplot(fig)
    else:
        st.info("AVL vacío, sin rutas registradas.")
