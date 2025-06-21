import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

def visualizar_grafo(vertices, aristas, ruta_resaltada=None):
    """
    Dibuja el grafo de la red de drones usando networkx y matplotlib.
    """
    if not vertices:
        st.warning("No hay vértices para mostrar en la red.")
        return
    if not aristas:
        st.warning("No hay aristas para mostrar en la red.")
        return
    G = nx.DiGraph()
    tipo_color = {'cliente': 'tab:blue', 'almacenamiento': 'tab:orange', 'recarga': 'tab:green'}
    id_to_tipo = {}
    for vertice in vertices:
        tipo = vertice.get('tipo', 'otro')
        G.add_node(vertice['id'], tipo=tipo, nombre=vertice.get('nombre', str(vertice['id'])))
        id_to_tipo[vertice['id']] = tipo
    for arista in aristas:
        G.add_edge(arista['origen'], arista['destino'], peso=arista.get('peso', 1))
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 7))
    colores = [tipo_color.get(id_to_tipo[n], 'tab:gray') for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=600, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['nombre'] for n in G.nodes}, font_size=11, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    if ruta_resaltada:
        path_edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3, ax=ax)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=tipo.capitalize()) for tipo, color in tipo_color.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    plt.axis('off')
    st.pyplot(fig)
