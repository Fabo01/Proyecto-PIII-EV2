import logging
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch

logger = logging.getLogger("frontend.visualizacion.grafo")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def visualizar_grafo(vertices, aristas, ruta_resaltada=None):
    """
    Dibuja el grafo de la red de drones usando networkx y matplotlib.
    Cumple con requisitos de robustez, validación y escalabilidad.
    """
    if not vertices or not isinstance(vertices, list):
        logger.warning("No hay vértices para mostrar en la red.")
        st.warning("No hay vértices para mostrar en la red.")
        return
    if not aristas or not isinstance(aristas, list):
        logger.warning("No hay aristas para mostrar en la red.")
        st.warning("No hay aristas para mostrar en la red.")
        return
    # Validar estructura de los vértices
    vertices_validos = []
    tipo_color = {'cliente': 'tab:blue', 'almacenamiento': 'tab:orange', 'recarga': 'tab:green'}
    id_to_tipo = {}
    id_to_nombre = {}
    for vertice in vertices:
        vid = vertice.get('id')
        tipo = vertice.get('tipo', 'otro')
        nombre = vertice.get('nombre', str(vid))
        if vid is None or tipo not in tipo_color:
            logger.warning(f"Vértice inválido detectado: {vertice}")
            continue
        vertices_validos.append(vid)
        id_to_tipo[vid] = tipo
        id_to_nombre[vid] = nombre
    if not vertices_validos:
        logger.warning("No hay vértices válidos para mostrar (clientes, almacenes o recargas).")
        st.warning("No hay vértices válidos para mostrar (clientes, almacenes o recargas).")
        return
    G = nx.DiGraph()
    for vid in vertices_validos:
        G.add_node(vid, tipo=id_to_tipo[vid], nombre=id_to_nombre[vid])
    # Validar aristas: solo entre vertices válidos
    aristas_validas = []
    for arista in aristas:
        origen = arista.get('origen')
        destino = arista.get('destino')
        peso = arista.get('peso', 1)
        if origen in vertices_validos and destino in vertices_validos:
            aristas_validas.append((origen, destino, peso))
        else:
            logger.warning(f"Arista inválida detectada: {arista}")
    if not aristas_validas:
        logger.warning("No hay aristas válidas para mostrar en la red.")
        st.warning("No hay aristas válidas para mostrar en la red.")
        return
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 7))
    colores = [tipo_color.get(id_to_tipo[n], 'tab:gray') for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=600, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['nombre'] for n in G.nodes}, font_size=11, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    if ruta_resaltada:
        path_edges = [(ruta_resaltada[i], ruta_resaltada[i+1]) for i in range(len(ruta_resaltada)-1)
                      if ruta_resaltada[i] in G.nodes and ruta_resaltada[i+1] in G.nodes]
        if path_edges:
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3, ax=ax)
    legend_elements = [Patch(facecolor=color, label=tipo.capitalize()) for tipo, color in tipo_color.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    plt.axis('off')
    st.pyplot(fig)
    # Mensaje de ayuda si faltan tipos
    tipos_presentes = set(id_to_tipo.values())
    for tipo, color in tipo_color.items():
        if tipo not in tipos_presentes:
            st.info(f"No hay vértices de tipo '{tipo}' en la red actual.")
