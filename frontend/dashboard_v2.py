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
    return f"{tipo.capitalize()} {idx} (Nodo {id_vertice})"

def formatear_peso(peso):
    return f"{peso:.2f}"

# --- Visualización avanzada de grafos ---
def visualizar_grafo(nodos, aristas, ruta_resaltada=None):
    G = nx.DiGraph()
    colores = []
    tipo_color = {'cliente': 'tab:blue', 'almacenamiento': 'tab:orange', 'recarga': 'tab:green'}
    tipo_indices = {'cliente': 0, 'almacenamiento': 0, 'recarga': 0}
    id_to_nombre = {}
    for nodo in nodos:
        tipo = nodo['tipo']
        idx = tipo_indices[tipo] + 1
        tipo_indices[tipo] += 1
        nombre = formatear_nombre(tipo, idx, nodo['id'])
        id_to_nombre[nodo['id']] = nombre
        G.add_node(nodo['id'], tipo=tipo, nombre=nombre)
        colores.append(tipo_color.get(tipo, 'tab:gray'))
    for arista in aristas:
        G.add_edge(arista['origen'], arista['destino'], peso=formatear_peso(arista['peso']))
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 7))
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=600, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['nombre'] for n in G.nodes}, font_size=11, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    if ruta_resaltada:
        path_edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3, ax=ax)
    plt.axis('off')
    st.pyplot(fig)
    st.markdown("""
    <style>
    .element-container svg g text { font-family: 'Segoe UI', Arial, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

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

# --- Cache robusto de datos base ---
@st.cache_data(ttl=10, show_spinner=False)
def obtener_nodos_cache():
    return api_get("/nodos")

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
    st.header("Configuración de la Simulación")
    n_nodos = st.slider("Número de nodos", 10, 150, 15, key="n_nodos")
    m_aristas = st.slider("Número de aristas", 10, 300, 20, key="m_aristas")
    n_pedidos = st.slider("Número de pedidos", 10, 300, 10, key="n_pedidos")
    st.info(f"Clientes: {int(n_nodos*0.6)} | Almacenamientos: {int(n_nodos*0.2)} | Recargas: {int(n_nodos*0.2)}")
    if st.button("Iniciar Simulación"):
        if m_aristas < n_nodos - 1:
            st.error("El número de aristas debe ser al menos n_nodos - 1 para asegurar conectividad.")
            return
        resp = api_post("/simulacion/iniciar", {
            "n_nodos": n_nodos,
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
    st.header("Red de Drones")
    nodos = obtener_nodos_cache() or []
    aristas = obtener_aristas_cache() or []
    almacenamientos = obtener_almacenamientos_cache() or []
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
    # Clientes reactivos según almacén
    clientes_filtrados = api_get(f"/clientes/con_pedidos/{origen['id']}") or []
    if not clientes_filtrados:
        st.info("No hay clientes con pedidos en este almacén.")
        visualizar_grafo(nodos, aristas)
        return
    destino_idx = st.selectbox(
        "Selecciona Cliente Destino",
        options=range(len(clientes_filtrados)),
        format_func=lambda i: f"{clientes_filtrados[i]['nombre']} (ID {clientes_filtrados[i]['id']})",
        key=f"select_cliente_destino_{origen['id']}"
    )
    destino = clientes_filtrados[destino_idx]
    # Pedidos reactivos según cliente y almacén
    pedidos_cliente = api_get(f"/clientes/{destino['id']}/pedidos_en_almacen/{origen['id']}") or []
    if not pedidos_cliente:
        st.info("No hay pedidos de este cliente en el almacén seleccionado.")
        visualizar_grafo(nodos, aristas)
        return
    pedido_idx = st.selectbox(
        "Selecciona Pedido",
        options=range(len(pedidos_cliente)),
        format_func=lambda i: f"Pedido {pedidos_cliente[i]['id_pedido']} (Prioridad {pedidos_cliente[i].get('prioridad', '-')})",
        key=f"select_pedido_{origen['id']}_{destino['id']}"
    )
    pedido = pedidos_cliente[pedido_idx]
    algoritmos = ["bfs", "dfs", "topological", "dijkstra", "floyd_warshall"]
    algoritmo = st.selectbox("Algoritmo", algoritmos, key="select_algoritmo")
    ruta = None
    costo = None
    tiempo = None
    if st.button("Calcular Ruta para Pedido"):
        params = {"origen": origen['id'], "destino": destino['id'], "algoritmo": algoritmo, "id_pedido": pedido['id_pedido']}
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
                st.error("No existe una ruta posible para el pedido seleccionado o error en el cálculo.")
    visualizar_grafo(nodos, aristas, ruta_resaltada=ruta)

# --- Clientes y Pedidos ---
def ui_clientes_pedidos():
    st.header("Clientes, Almacenamientos, Recargas y Pedidos")
    clientes = obtener_clientes_cache() or []
    almacenamientos = obtener_almacenamientos_cache() or []
    recargas = obtener_recargas_cache() or []
    pedidos = obtener_pedidos_cache() or []
    rutas = api_get("/rutas") or []
    aristas = obtener_aristas_cache() or []
    # Formatear nombres
    for idx, c in enumerate(clientes, 1):
        c['nombre'] = formatear_nombre('cliente', idx, c['id'])
    for idx, a in enumerate(almacenamientos, 1):
        a['nombre'] = formatear_nombre('almacenamiento', idx, a['id'])
    for idx, r in enumerate(recargas, 1):
        r['nombre'] = formatear_nombre('recarga', idx, r['id'])
    # --- Errores de pedidos ---
    st.subheader("Errores de Creación de Pedidos (Fábrica)")
    errores = api_get("/pedidos/errores") or []
    if errores:
        df_errores = pd.DataFrame(errores)
        # Mostrar solo columnas relevantes si existen
        columnas_errores = [c for c in ['id_pedido', 'error', 'motivo', 'cliente', 'almacen', 'fecha', 'prioridad'] if c in df_errores.columns]
        st.dataframe(df_errores[columnas_errores] if columnas_errores else df_errores)
    else:
        st.info("No hay errores de creación de pedidos registrados.")
    # --- Clientes ---
    st.subheader("Lista de Clientes")
    df_clientes = pd.DataFrame(clientes)
    if not df_clientes.empty:
        st.dataframe(df_clientes[['id', 'nombre', 'tipo']] if all(x in df_clientes.columns for x in ['id', 'nombre', 'tipo']) else df_clientes)
    else:
        st.info("No hay clientes registrados.")
    # --- Almacenamientos ---
    st.subheader("Lista de Almacenamientos")
    df_almacenamientos = pd.DataFrame(almacenamientos)
    if not df_almacenamientos.empty:
        st.dataframe(df_almacenamientos[['id', 'nombre', 'tipo']] if all(x in df_almacenamientos.columns for x in ['id', 'nombre', 'tipo']) else df_almacenamientos)
    else:
        st.info("No hay almacenamientos registrados.")
    # --- Recargas ---
    st.subheader("Lista de Recargas")
    df_recargas = pd.DataFrame(recargas)
    if not df_recargas.empty:
        st.dataframe(df_recargas[['id', 'nombre', 'tipo']] if all(x in df_recargas.columns for x in ['id', 'nombre', 'tipo']) else df_recargas)
    else:
        st.info("No hay estaciones de recarga registradas.")
    # --- Pedidos ---
    st.subheader("Lista de Pedidos")
    df_pedidos = pd.DataFrame(pedidos)
    # Forzar presencia de columnas clave aunque estén vacías
    columnas_clave = [
        'id_pedido', 'origen', 'origen_nombre', 'destino', 'destino_nombre',
        'prioridad', 'status', 'fecha_creacion', 'fecha_entrega', 'peso_total', 'ruta'
    ]
    for col in columnas_clave:
        if col not in df_pedidos.columns:
            df_pedidos[col] = None
    if not df_pedidos.empty:
        # Mapeo de IDs a nombres para origen y destino
        id_to_nombre = {v['id']: v['nombre'] for v in clientes + almacenamientos + recargas if 'id' in v and 'nombre' in v}
        df_pedidos['origen_nombre'] = df_pedidos['origen'].map(id_to_nombre).fillna(df_pedidos['origen'])
        df_pedidos['destino_nombre'] = df_pedidos['destino'].map(id_to_nombre).fillna(df_pedidos['destino'])
        # Formatear fechas para visualización
        df_pedidos['fecha_creacion'] = pd.to_datetime(df_pedidos['fecha_creacion'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        df_pedidos['fecha_entrega'] = pd.to_datetime(df_pedidos['fecha_entrega'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        # Formatear ruta como string legible
        if 'ruta' in df_pedidos.columns:
            df_pedidos['ruta'] = df_pedidos['ruta'].apply(lambda x: ' → '.join(map(str, x)) if isinstance(x, list) else (str(x) if x is not None else ''))
        # Mostrar advertencia visual si hay campos nulos o inconsistentes
        inconsistentes = df_pedidos[df_pedidos[['origen', 'destino', 'fecha_creacion']].isnull().any(axis=1)]
        if not inconsistentes.empty:
            st.warning(f"Pedidos con datos incompletos: {inconsistentes[['id_pedido','origen','destino','fecha_creacion']].to_dict('records')}")
        st.dataframe(df_pedidos[columnas_clave])
    else:
        st.dataframe(df_pedidos[columnas_clave])
        st.info("No hay pedidos registrados.")
    # --- Rutas creadas ---
    st.subheader("Rutas Creadas")
    df_rutas = pd.DataFrame(rutas)
    if not df_rutas.empty:
        columnas_rutas = [c for c in ['origen', 'destino', 'camino', 'peso_total', 'algoritmo', 'tiempo_respuesta'] if c in df_rutas.columns]
        st.dataframe(df_rutas[columnas_rutas] if columnas_rutas else df_rutas)
    else:
        st.info("No hay rutas creadas aún.")
    # --- Aristas detalladas ---
    st.subheader("Lista de Aristas")
    if aristas:
        df_aristas = pd.DataFrame(aristas)
        if not df_aristas.empty:
            df_aristas['nombre'] = df_aristas.apply(lambda row: f"Arista {row.name+1}: {row['origen']} → {row['destino']}", axis=1)
            columnas_aristas = [c for c in ['nombre', 'origen', 'destino', 'peso'] if c in df_aristas.columns]
            st.dataframe(df_aristas[columnas_aristas] if columnas_aristas else df_aristas)
        else:
            st.info("No hay aristas registradas.")
    else:
        st.info("No hay aristas registradas.")

# --- Análisis de rutas y AVL ---
def ui_analisis_rutas():
    st.header("Rutas más frecuentes (AVL)")
    stats = obtener_estadisticas_cache()
    rutas = stats.get('rutas_mas_frecuentes', []) if stats else []
    visualizar_avl(rutas)

# --- Estadísticas Generales ---
def ui_estadisticas():
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
    # Gráfico de barras de nodos más visitados
    st.subheader("Nodos más visitados")
    nodos_visitados = stats.get('nodos_mas_visitados', {})
    if nodos_visitados:
        df_nodos = pd.DataFrame(list(nodos_visitados.items()), columns=['Nodo', 'Visitas'])
        st.bar_chart(df_nodos.set_index('Nodo'))
    # Gráfico de torta de proporción de nodos
    st.subheader("Proporción de nodos por rol")
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
