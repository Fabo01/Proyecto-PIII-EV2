import streamlit as st
import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from functools import lru_cache

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Simulación Drones Correos Chile", layout="wide")
st.title("Simulación Logística de Drones - Correos Chile")

# --- Servicios de API robustos y desacoplados ---
@st.cache_data(ttl=10, show_spinner=False)
def api_get_cached(endpoint, params=None):
    return api_get(endpoint, params)

@st.cache_data(ttl=10, show_spinner=False)
def obtener_estado_simulacion_cache():
    return api_get("/simulacion/estado")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_aristas_cache():
    return api_get("/aristas")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_clientes_cache():
    return api_get("/clientes")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_almacenamientos_cache():
    return api_get("/almacenamientos")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_recargas_cache():
    return api_get("/recargas")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_pedidos_cache():
    return api_get("/pedidos")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_estadisticas_cache():
    return api_get("/estadisticas/")

def api_get(endpoint, params=None):
    try:
        url = API_URL + endpoint
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al consultar la API: {e}")
        return None

def api_post(endpoint, data=None):
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al enviar datos a {endpoint}: {e}")
        return None

def formatear_nombre(tipo, idx, id_vertice):
    return f"{tipo.capitalize()} {idx} (Vértice {id_vertice})"

def formatear_peso(peso):
    return f"{peso:.2f}"

# --- Visualización avanzada de grafos ---
def visualizar_grafo(vertices, aristas, ruta_resaltada=None):
    """
    Dibuja el grafo de la red de drones usando networkx y matplotlib.
    Los vértices se colorean según su tipo y la leyenda es por tipo, no por vértice individual.
    Robustece: solo grafica si existen vértices y aristas, muestra advertencias claras si faltan datos.
    """
    if not vertices:
        st.warning("No hay vértices para mostrar en la red. Asegúrate de haber iniciado la simulación y que existan vértices.")
        return
    if not aristas:
        st.warning("No hay aristas para mostrar en la red. Asegúrate de haber iniciado la simulación y que existan conexiones entre vértices.")
        return
    G = nx.DiGraph()
    tipo_color = {'cliente': 'tab:blue', 'almacenamiento': 'tab:orange', 'recarga': 'tab:green'}
    id_to_tipo = {}
    for vertice in vertices:
        tipo = vertice['tipo']
        G.add_node(vertice['id'], tipo=tipo, nombre=vertice['nombre'])
        id_to_tipo[vertice['id']] = tipo
    for arista in aristas:
        G.add_edge(arista['origen'], arista['destino'], peso=formatear_peso(arista['peso']))
    if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
        st.warning("No hay suficientes datos para graficar la red (faltan vértices o aristas válidas).")
        return
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 7))
    # Colores por tipo
    colores = [tipo_color.get(id_to_tipo[n], 'tab:gray') for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=600, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['nombre'] for n in G.nodes}, font_size=11, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    if ruta_resaltada:
        path_edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3, ax=ax)
    # Leyenda por tipo
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=tipo.capitalize()) for tipo, color in tipo_color.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    plt.axis('off')
    st.pyplot(fig)
    st.markdown("""
    <style>
    .element-container svg g text { font-family: 'Segoe UI', Arial, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- Visualización avanzada de AVL (frecuencia de rutas) ---
def visualizar_avl(rutas):
    """
    Dibuja un gráfico de barras horizontal con las rutas más frecuentes (AVL).
    """
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

# --- Cache robusto de datos base ---
@st.cache_data(ttl=10, show_spinner=False)
def obtener_vertices_cache():
    return api_get("/vertices")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_aristas_cache():
    return api_get("/aristas")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_pedidos_cache():
    return api_get("/pedidos")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_clientes_cache():
    return api_get("/clientes")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_almacenamientos_cache():
    return api_get("/almacenamientos")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_recargas_cache():
    return api_get("/recargas")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_estadisticas_cache():
    return api_get("/estadisticas/")

# --- Estado y exploración de la red ---
def obtener_estado_simulacion():
    estado = api_get("/simulacion/estado")
    if not estado or 'clientes' not in estado:
        st.warning("Primero debes iniciar una simulación en la pestaña 'Configuración de la Simulación'.")
        st.stop()
    return estado

# --- UI Modular y desacoplada ---
def ui_simulacion():
    """
    Pestaña 1: Configuración e inicio de la simulación.
    Permite seleccionar parámetros y lanzar la simulación vía API.
    """
    st.header("Configuración de la Simulación")
    n_vertices = st.slider("Número de vertices", 10, 150, 15, key="n_vertices")
    m_aristas = st.slider("Número de aristas", 10, 300, 20, key="m_aristas")
    n_pedidos = st.slider("Número de pedidos", 10, 300, 10, key="n_pedidos")
    st.info(f"Clientes: {int(n_vertices*0.6)} | Almacenamientos: {int(n_vertices*0.2)} | Recargas: {int(n_vertices*0.2)}")
    if st.button("Iniciar Simulación"):
        if m_aristas < n_vertices - 1:
            st.error("El número de aristas debe ser al menos n_vertices - 1 para asegurar conectividad.")
            return
        resp = api_post("/simulacion/iniciar", {
            "n_vertices": n_vertices,
            "m_aristas": m_aristas,
            "n_pedidos": n_pedidos
        })
        if resp:
            st.success("¡Simulación iniciada!")
            st.session_state['simulacion_iniciada'] = True
            st.rerun()
        else:
            st.error("No se pudo iniciar la simulación. Revisa los parámetros o el backend.")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_estado_simulacion_cache():
    return api_get("/simulacion/estado")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_aristas_cache():
    return api_get("/aristas")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_clientes_cache():
    return api_get("/clientes")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_almacenamientos_cache():
    return api_get("/almacenamientos")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_recargas_cache():
    return api_get("/recargas")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_pedidos_cache():
    return api_get("/pedidos")

@st.cache_data(ttl=10, show_spinner=False)
def obtener_estadisticas_cache():
    return api_get("/estadisticas/")

# --- Estado y exploración de la red ---
def ui_explorar_red():
    """
    Pestaña 2: Visualización de la red y cálculo de rutas entre vertices.
    Permite seleccionar origen, destino y algoritmo, y muestra la ruta calculada.
    Además, permite visualizar el Árbol de Expansión Mínima (Kruskal).
    """
    st.header("Red de Drones")
    vertices = obtener_vertices_cache() or []
    aristas = obtener_aristas_cache() or []
    almacenamientos = obtener_almacenamientos_cache() or []
    clientes = obtener_clientes_cache() or []
    pedidos = obtener_pedidos_cache() or []
    # --- Obtener el hashmap de vértices para validación robusta ---
    hashmap_vertices = api_get("/vertices/hashmap") or {}
    if not (almacenamientos and aristas):
        st.warning("No hay datos suficientes para mostrar la red.")
        return
    # Selección reactiva de almacén
    origen_idx = st.selectbox(
        "Selecciona Almacen Origen",
        options=range(len(almacenamientos)),
        format_func=lambda i: f"{almacenamientos[i]['nombre']} (ID {almacenamientos[i]['id']})",
        key="select_almacen_origen"
    )
    origen = almacenamientos[origen_idx]
    # Clientes reactivos según almacén (filtrados por pedidos asociados a ese almacén)
    clientes_con_pedidos = [c for c in clientes if any(
        p['origen'] and (p['origen']['id'] if isinstance(p['origen'], dict) else None) == origen['id'] for p in pedidos if p.get('cliente', {}).get('id', None) == c['id'])]
    if not clientes_con_pedidos:
        st.info("No hay clientes con pedidos en este almacén.")
        visualizar_grafo(vertices, aristas)
        return
    destino_idx = st.selectbox(
        "Selecciona Cliente Destino",
        options=range(len(clientes_con_pedidos)),
        format_func=lambda i: f"{clientes_con_pedidos[i]['nombre']} (ID {clientes_con_pedidos[i]['id']})",
        key=f"select_cliente_destino_{origen['id']}"
    )
    destino = clientes_con_pedidos[destino_idx]
    # Pedidos reactivos según cliente y almacén
    pedidos_cliente = [p for p in pedidos if p.get('cliente', {}).get('id', None) == destino['id'] and (p['origen']['id'] if isinstance(p['origen'], dict) else None) == origen['id']]
    if not pedidos_cliente:
        st.info("No hay pedidos de este cliente en el almacén seleccionado.")
        visualizar_grafo(vertices, aristas)
        return
    pedido_idx = st.selectbox(
        "Selecciona Pedido",
        options=range(len(pedidos_cliente)),
        format_func=lambda i: f"Pedido {pedidos_cliente[i]['id_pedido']} (Prioridad {pedidos_cliente[i].get('prioridad', '-')})",
        key=f"select_pedido_{origen['id']}_{destino['id']}"
    )
    pedido = pedidos_cliente[pedido_idx]
    algoritmos = ["bfs", "dfs", "topological_sort", "dijkstra", "floyd_warshall"]
    algoritmo = st.selectbox("Algoritmo", algoritmos, key="select_algoritmo")
    ruta = None
    costo = None
    tiempo = None
    # --- Botón para calcular camino arbitrario entre vertices (opcional, para exploración de red) ---
    if st.button("Calcular Camino entre vertices"):
        # Validación robusta antes de enviar
        st.info(f"[DEBUG] Objeto origen: {origen}, tipo: {type(origen)}")
        st.info(f"[DEBUG] Objeto destino: {destino}, tipo: {type(destino)}")
        if not isinstance(origen, dict) or not isinstance(destino, dict):
            st.error(f"[ERROR] Origen o destino no son objetos válidos: origen={origen} ({type(origen)}), destino={destino} ({type(destino)})")
        elif 'id' not in origen or 'id' not in destino:
            st.error(f"[ERROR] Origen o destino no tienen campo 'id': origen={origen}, destino={destino}")
        elif not isinstance(origen['id'], int) or not isinstance(destino['id'], int):
            st.error(f"[ERROR] El id de origen o destino no es entero: origen['id']={origen['id']} ({type(origen['id'])}), destino['id']={destino['id']} ({type(destino['id'])})")
        elif str(origen['id']) not in hashmap_vertices or str(destino['id']) not in hashmap_vertices:
            st.error(f"[ERROR] El id de origen o destino no existe en el HashMap de vértices: origen['id']={origen['id']}, destino['id']={destino['id']}")
        else:
            st.success(f"[OK] Los objetos origen y destino son referencias válidas y únicas en el HashMap de vértices.")
            st.info(f"[LOG] Enviando a /rutas/camino: origen={origen['id']} (type: {type(origen['id'])}), destino={destino['id']} (type: {type(destino['id'])}), algoritmo={algoritmo} (type: {type(algoritmo)})")
            params = {"origen": origen['id'], "destino": destino['id'], "algoritmo": algoritmo}
            resultado = api_get("/rutas/camino", params=params)
            if resultado and resultado.get('camino'):
                ruta = resultado['camino']
                costo = resultado['peso_total']
                tiempo = resultado.get('tiempo_respuesta', None)
                st.success(f"Ruta: {ruta}\nCosto: {costo}\nTiempo de cálculo: {tiempo} segundos")
            else:
                detalle = resultado.get('detail') if resultado else None
                if detalle:
                    st.error(f"Error: {detalle}")
                else:
                    st.error("No existe una ruta posible para los vertices seleccionados o error en el cálculo.")
    # --- Botón para calcular ruta óptima de un pedido ---
    if st.button("Calcular Ruta para Pedido"):
        # Log de parámetros antes de enviar
        st.info(f"[LOG] Enviando a /rutas/calcular: id_pedido={pedido['id_pedido']}, algoritmo={algoritmo}")
        params = {"id_pedido": pedido['id_pedido'], "algoritmo": algoritmo}
        resultado = api_get("/rutas/calcular", params=params)
        if resultado and resultado.get('camino'):
            ruta = resultado['camino']
            costo = resultado['peso_total']
            tiempo = resultado.get('tiempo_calculo', None)
            st.success(f"Ruta: {ruta}\nCosto: {costo}\nTiempo de cálculo: {tiempo} segundos")
        else:
            detalle = resultado.get('detail') if resultado else None
            if detalle:
                st.error(f"Error: {detalle}")
            else:
                st.error("No existe una ruta posible para el pedido seleccionado o error en el cálculo.")
    # --- Validación robusta antes de visualizar el grafo ---
    if not vertices or not aristas:
        st.warning("No se puede visualizar la red: faltan vértices o aristas. Asegúrate de que la simulación esté correctamente inicializada y que existan datos válidos.")
        return
    visualizar_grafo(vertices, aristas, ruta_resaltada=ruta)
    # --- Sección diferenciada para Árbol de Expansión Mínima (Kruskal) ---
    st.subheader("Árbol de Expansión Mínima (Kruskal)")
    if st.button("Calcular Árbol de Expansión Mínima"):
        mst_result = api_get("/rutas/arbol_expansion_minima")
        if mst_result and 'mst' in mst_result:
            mst = mst_result['mst']
            peso_total = mst_result.get('peso_total', 0)
            st.info(f"Peso total del árbol: {peso_total:.2f}")
            # Visualizar el árbol MST sobre el grafo
            vertices_mst = set()
            aristas_mst = []
            for arista in mst:
                vertices_mst.add(arista['origen'])
                vertices_mst.add(arista['destino'])
                aristas_mst.append((arista['origen'], arista['destino']))
            G = nx.DiGraph()
            for vertice in vertices:
                G.add_node(vertice['id'])
            for arista in aristas:
                G.add_edge(arista['origen'], arista['destino'])
            pos = nx.spring_layout(G, seed=42)
            fig, ax = plt.subplots(figsize=(12, 7))
            nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=600, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='lightgray', ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=aristas_mst, edge_color='crimson', width=3, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=11, ax=ax)
            plt.axis('off')
            st.pyplot(fig)
        else:
            st.error("No se pudo calcular el árbol de expansión mínima.")

# --- Clientes y Pedidos ---
def ui_clientes_pedidos():
    """
    Pestaña 3: Visualización de hashmaps de clientes, pedidos, almacenamientos, recargas, vértices, aristas y rutas.
    Solo aquí se muestran los hashmaps reales, garantizando unicidad y referencias correctas.
    """
    st.header("HashMap de Objetos Persistentes (Clientes, Pedidos, Almacenamientos, Recargas, Vértices, Aristas, Rutas)")
    # --- HashMap de Clientes ---
    clientes_hashmap = api_get("/clientes/hashmap") or {}
    st.subheader("HashMap de Clientes (ID → Objeto)")
    st.json(clientes_hashmap)
    # --- HashMap de Pedidos ---
    pedidos_hashmap = api_get("/pedidos/hashmap") or {}
    st.subheader("HashMap de Pedidos (ID → Objeto)")
    st.json(pedidos_hashmap)
    # --- HashMap de Almacenamientos ---
    almacenamientos_hashmap = api_get("/almacenamientos/hashmap") or {}
    st.subheader("HashMap de Almacenamientos (ID → Objeto)")
    st.json(almacenamientos_hashmap)
    # --- HashMap de Recargas ---
    recargas_hashmap = api_get("/recargas/hashmap") or {}
    st.subheader("HashMap de Recargas (ID → Objeto)")
    st.json(recargas_hashmap)
    # --- HashMap de Vértices ---
    vertices_hashmap = api_get("/vertices/hashmap") or {}
    st.subheader("HashMap de Vértices (ID → Objeto)")
    st.json(vertices_hashmap)
    # --- HashMap de Aristas ---
    aristas_hashmap = api_get("/aristas/hashmap") or {}
    st.subheader("HashMap de Aristas (Clave → Objeto)")
    st.json(aristas_hashmap)
    # --- HashMap de Rutas ---
    rutas_hashmap = api_get("/rutas/hashmap") or {}
    st.subheader("HashMap de Rutas (Clave → Objeto)")
    st.json(rutas_hashmap)
    st.info("Se muestran solo los hashmaps reales de persistencia, garantizando unicidad y referencias correctas. No se muestran listas ni tablas en esta pestaña.")

# --- Análisis de rutas y AVL ---
def ui_analisis_rutas():
    """
    Pestaña 4: Visualización de rutas más frecuentes (AVL).
    """
    st.header("Rutas más frecuentes (AVL)")
    stats = obtener_estadisticas_cache()
    rutas = stats.get('rutas_mas_frecuentes', []) if stats else []
    visualizar_avl(rutas)

# --- Estadísticas Generales ---
def ui_estadisticas():
    """
    Pestaña 5: Estadísticas generales del sistema y gráficos de vertices.
    """
    st.header("Estadísticas Generales")
    stats = obtener_estadisticas_cache()
    if not stats:
        st.warning("Primero debes iniciar una simulación en la pestaña 'Configuración de la Simulación'.")
        st.stop()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clientes", stats.get('total_clientes', 0))
    col2.metric("Almacenamientos", stats.get('total_almacenamientos', 0))
    col3.metric("Recargas", stats.get('total_recargas', 0))
    col4.metric("Pedidos", stats.get('total_pedidos', 0))
    st.write(f"Tiempo de respuesta: {stats.get('tiempo_respuesta', 0.0)}s")
    # Gráfico de barras de vertices más visitados
    st.subheader("vertices más visitados")
    vertices_visitados = stats.get('vertices_mas_visitados', {})
    if vertices_visitados:
        df_vertices = pd.DataFrame(list(vertices_visitados.items()), columns=['vertice', 'Visitas'])
        st.bar_chart(df_vertices.set_index('vertice'))
    # Gráfico de torta de proporción de vertices
    st.subheader("Proporción de vertices por rol")
    roles = ['clientes', 'almacenamientos', 'recargas']
    valores = [stats.get(f'total_{r}', 0) for r in roles]
    fig, ax = plt.subplots()
    ax.pie(valores, labels=roles, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    st.write("Rutas más frecuentes:")
    visualizar_avl(stats.get('rutas_mas_frecuentes', []))

# --- Navegación principal desacoplada ---
pestana = st.sidebar.radio("Selecciona una pestaña", [
    "Configuración de la Simulación",
    "Explorar Red",
    "Clientes y Pedidos",
    "Análisis de Rutas",
    "Estadísticas Generales"
], key="pestana")

if pestana == "Configuración de la Simulación":
    ui_simulacion()
elif pestana == "Explorar Red":
    if st.session_state.get('simulacion_iniciada'):
        ui_explorar_red()
    else:
        st.info("Primero debes iniciar una simulación.")
elif pestana == "Clientes y Pedidos":
    if st.session_state.get('simulacion_iniciada'):
        ui_clientes_pedidos()
    else:
        st.info("Primero debes iniciar una simulación.")
elif pestana == "Análisis de Rutas":
    if st.session_state.get('simulacion_iniciada'):
        ui_analisis_rutas()
    else:
        st.info("Primero debes iniciar una simulación.")
elif pestana == "Estadísticas Generales":
    if st.session_state.get('simulacion_iniciada'):
        ui_estadisticas()
    else:
        st.info("Primero debes iniciar una simulación.")
