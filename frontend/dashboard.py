import streamlit as st
import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Simulación Drones Correos Chile", layout="wide")
st.title("Simulación Logística de Drones - Correos Chile")

# --- Servicios de API robustos y desacoplados ---
def api_get(endpoint, params=None):
    try:
        resp = requests.get(f"{API_URL}{endpoint}", params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al obtener datos de {endpoint}: {e}")
        return None

def api_post(endpoint, data=None):
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al enviar datos a {endpoint}: {e}")
        return None

# --- Visualización avanzada de grafos ---
def visualizar_grafo(nodos, aristas):
    G = nx.DiGraph()
    colores = []
    tipo_color = {'cliente': 'tab:blue', 'almacenamiento': 'tab:orange', 'recarga': 'tab:green'}
    for nodo in nodos:
        G.add_node(nodo['id'], tipo=nodo['tipo'], nombre=nodo['nombre'])
        colores.append(tipo_color.get(nodo['tipo'], 'tab:gray'))
    for arista in aristas:
        G.add_edge(arista['origen'], arista['destino'], peso=arista['peso'])
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=500, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['nombre'] for n in G.nodes}, font_size=10, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    plt.axis('off')
    st.pyplot(fig)

# --- Visualización avanzada de AVL (frecuencia de rutas) ---
def visualizar_avl(rutas):
    if not rutas:
        st.info("No hay rutas frecuentes registradas.")
        return
    rutas_str = [' → '.join(str(n) for n in ruta['camino']) for ruta in rutas]
    frecuencias = [ruta.get('frecuencia', 1) for ruta in rutas]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(rutas_str, frecuencias, color='tab:purple')
    ax.set_xlabel('Frecuencia')
    ax.set_title('Rutas más frecuentes (AVL)')
    st.pyplot(fig)

# --- UI Modular y desacoplada ---
def ui_simulacion():
    st.header("Configuración de la Simulación")
    n_nodos = st.slider("Número de nodos", 10, 150, 15)
    m_aristas = st.slider("Número de aristas", 10, 300, 20)
    n_pedidos = st.slider("Número de pedidos", 10, 300, 10)
    if st.button("Iniciar Simulación"):
        resp = api_post("/simulacion/iniciar", {
            "n_nodos": n_nodos,
            "m_aristas": m_aristas,
            "n_pedidos": n_pedidos
        })
        if resp:
            st.success("¡Simulación iniciada!")

# --- Estado y exploración de la red ---
def obtener_estado_simulacion():
    estado = api_get("/simulacion/estado")
    if not estado:
        st.warning("Primero debes iniciar una simulación en la pestaña 'Configuración de la Simulación'.")
        st.stop()
    return estado

def ui_explorar_red():
    st.header("Red de Drones")
    estado = obtener_estado_simulacion()
    nodos = estado['clientes'] + estado['almacenamientos'] + estado['recargas']
    aristas = api_get("/aristas")
    if nodos and aristas:
        visualizar_grafo(nodos, aristas)
    else:
        st.info("No hay datos de red para mostrar.")

# --- Clientes y Pedidos ---
def ui_clientes_pedidos():
    st.header("Clientes y Pedidos")
    estado = obtener_estado_simulacion()
    clientes = estado.get('clientes', [])
    pedidos = estado.get('pedidos', [])
    for cliente in clientes:
        st.subheader(f"{cliente['nombre']} (ID: {cliente['id']})")
        pedidos_cliente = [p for p in pedidos if p['destino'] == cliente['id']]
        if pedidos_cliente:
            for pedido in pedidos_cliente:
                st.markdown(f"- Pedido {pedido['id_pedido']}: {pedido['origen']} → {pedido['destino']} (Prioridad: {pedido['prioridad']}, Estado: {pedido['status']})")
        else:
            st.info("Este cliente no tiene pedidos asociados.")

# --- Análisis de rutas y AVL ---
def ui_analisis_rutas():
    st.header("Rutas más frecuentes (AVL)")
    stats = api_get("/estadisticas/")
    rutas = stats.get('rutas_mas_frecuentes', []) if stats else []
    visualizar_avl(rutas)

# --- Estadísticas Generales ---
def ui_estadisticas():
    st.header("Estadísticas Generales")
    stats = api_get("/estadisticas/")
    if not stats:
        st.warning("Primero debes iniciar una simulación en la pestaña 'Configuración de la Simulación'.")
        st.stop()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clientes", stats.get('total_clientes', 0))
    col2.metric("Almacenamientos", stats.get('total_almacenamientos', 0))
    col3.metric("Recargas", stats.get('total_recargas', 0))
    col4.metric("Pedidos", stats.get('total_pedidos', 0))
    st.write(f"Tiempo de respuesta: {stats.get('tiempo_respuesta', 0.0)}s")
    st.write("Rutas más frecuentes:")
    visualizar_avl(stats.get('rutas_mas_frecuentes', []))

# --- Navegación principal desacoplada ---
pestana = st.sidebar.radio("Selecciona una pestaña", [
    "Configuración de la Simulación",
    "Explorar Red",
    "Clientes y Pedidos",
    "Análisis de Rutas",
    "Estadísticas Generales"
])

if pestana == "Configuración de la Simulación":
    ui_simulacion()
elif pestana == "Explorar Red":
    ui_explorar_red()
elif pestana == "Clientes y Pedidos":
    ui_clientes_pedidos()
elif pestana == "Análisis de Rutas":
    ui_analisis_rutas()
elif pestana == "Estadísticas Generales":
    ui_estadisticas()
