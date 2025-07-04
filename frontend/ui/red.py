from frontend.servicios.cache import (
    obtener_vertices_lista, obtener_aristas_lista, cachear_snapshot, cachear_algoritmos,
    obtener_almacenamientos_lista, obtener_pedidos_lista, obtener_clientes_lista
)
from frontend.utils.validadores import require_simulation_started
import streamlit as st
import logging
import traceback

# Configuración de logger para la pestaña Red
logger = logging.getLogger("frontend.ui.red")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

from frontend.visualizacion.grafo import visualizar_grafo
from frontend.servicios.api import api_post, api_get

def obtener_objetos_por_ids(ids, lista):
    """
    Devuelve una lista de objetos válidos asociados a una lista de IDs.
    """
    if not ids or not lista:
        return []
    resultados = []
    for ident in ids:
        for obj in lista:
            if obj.get('id') == ident or obj.get('id_pedido') == ident:
                resultados.append(obj)
                break
    return resultados

@require_simulation_started
def ui_red():
    """
    Pestaña 2: Visualización y exploración de la red de drones.
    Cumple con modularidad, robustez y nombres en español.
    """
    st.header("Red de Drones")
    logger.info("[UI] Solicitando listas de red antes de renderizar pestaña red.")
    # Cargar datos en session_state una sola vez para esta pestaña
    if 'red_datos' not in st.session_state:
        st.session_state['red_datos'] = {
            'vertices': obtener_vertices_lista() or [],
            'aristas': obtener_aristas_lista() or [],
            'snapshot_n1': cachear_snapshot('n-1') or {},
            'algoritmos': cachear_algoritmos() or [],
            'almacenes': obtener_almacenamientos_lista() or [],
            'pedidos': obtener_pedidos_lista() or [],
            'clientes': obtener_clientes_lista() or []
        }
    # Inicializar lista de pedidos completados
    if 'pedidos_completados' not in st.session_state:
        st.session_state['pedidos_completados'] = []
    datos = st.session_state['red_datos']
    logger.info(f"[UI] Listas recibidas: vertices={len(datos['vertices'])}, aristas={len(datos['aristas'])}, almacenes={len(datos['almacenes'])}, pedidos={len(datos['pedidos'])}, clientes={len(datos['clientes'])}")
    vertices_list = datos['vertices']
    aristas_list = datos['aristas']
    # Visualización del grafo completo
    if not vertices_list or not aristas_list:
        logger.warning("No hay vértices o aristas válidas para mostrar en la red.")
        st.warning("No hay datos de red disponibles.")
        st.stop()
    st.subheader("Grafo completo de la red")
    visualizar_grafo(vertices_list, aristas_list)
    # Visualización del árbol de Kruskal (MST)
    st.subheader("Árbol de expansión mínimo (Kruskal)")
    snapshot_mst = datos['snapshot_n1']
    try:
        if snapshot_mst and isinstance(snapshot_mst, dict) and snapshot_mst.get('vertices') and snapshot_mst.get('aristas'):
            logger.info(f"[UI] Mostrando MST con {len(snapshot_mst['vertices'])} vértices y {len(snapshot_mst['aristas'])} aristas")
            visualizar_grafo(snapshot_mst['vertices'], snapshot_mst['aristas'])
        else:
            logger.warning("No hay árbol MST disponible para mostrar.")
            st.info("No hay árbol MST disponible para mostrar.")
    except Exception as e:
        logger.error(f"[UI] Error al visualizar MST: {e}")
        st.error(f"Error al mostrar el árbol MST: {e}")
        st.text(traceback.format_exc())
    # Sección de cálculo de rutas
    st.sidebar.subheader("Calcular ruta de pedido")
    # Usar listas DTO directamente
    almacenes = datos['almacenes'] or []
    pedidos = [p for p in (datos['pedidos'] or []) if p and p.get('id_pedido') not in st.session_state['pedidos_completados']]
    clientes = datos['clientes'] or []
    # Selección de almacén
    if not almacenes:
        logger.warning("No hay almacenamientos disponibles para calcular rutas.")
        st.sidebar.info("No hay almacenamientos disponibles para calcular rutas.")
        return
    seleccion_almacen = st.sidebar.selectbox(
        "Selecciona Almacen", almacenes, format_func=lambda x: x.get('nombre', f"Almacen #{x.get('id')}") if x else "-"
    )
    # Filtrar clientes asociados a ese almacén (por pedidos)
    clientes_filtrados = []
    if seleccion_almacen:
        ids_pedidos_almacen = seleccion_almacen.get('ids_pedidos', [])
        pedidos_almacen = obtener_objetos_por_ids(ids_pedidos_almacen, datos['pedidos'])
        clientes_ids = set(p.get('destino_id') for p in pedidos_almacen if p and p.get('destino_id'))
        clientes_filtrados = [c for c in clientes if c.get('id') in clientes_ids]
    if not clientes_filtrados:
        logger.info(f"No hay clientes con pedidos asociados a este almacenamiento (ID: {seleccion_almacen.get('id') if seleccion_almacen else 'N/A'}).")
        st.sidebar.info("No hay clientes con pedidos asociados a este almacenamiento.")
        return
    seleccion_cliente = st.sidebar.selectbox(
        "Selecciona Cliente", clientes_filtrados, format_func=lambda x: x.get('nombre', f"Cliente #{x.get('id')}") if x else "-"
    )
    # Filtrar pedidos de ese cliente y almacén
    pedidos_filtrados = []
    if seleccion_almacen and seleccion_cliente:
        ids_pedidos_almacen = seleccion_almacen.get('ids_pedidos', [])
        pedidos_almacen = obtener_objetos_por_ids(ids_pedidos_almacen, datos['pedidos'])
        pedidos_filtrados = [p for p in pedidos_almacen if p.get('destino_id') == seleccion_cliente.get('id')]
    if not pedidos_filtrados:
        logger.info(f"No hay pedidos entre el almacenamiento (ID: {seleccion_almacen.get('id')}) y el cliente (ID: {seleccion_cliente.get('id')}).")
        st.sidebar.info("No hay pedidos entre este almacenamiento y cliente.")
        return
    seleccion_pedido = st.sidebar.selectbox(
        "Selecciona Pedido", pedidos_filtrados, format_func=lambda x: f"Pedido #{x.get('id_pedido')} (Prioridad: {x.get('prioridad')})" if x else "-"
    )
    # Selección de algoritmo
    algoritmos = datos['algoritmos']
    if not algoritmos:
        logger.warning("No hay algoritmos de ruta disponibles.")
        st.sidebar.info("No hay algoritmos de ruta disponibles.")
        return
    seleccion_algoritmo = st.sidebar.radio("Algoritmo de ruta", algoritmos, index=0)
    # Botón para calcular ruta y marcar pedido completado
    def _callback_calcular(id_pedido, algoritmo):
        try:
            logger.info(f"[UI] Calculando ruta para pedido {id_pedido} con algoritmo {algoritmo}")
            resp = api_get("/rutas/calcular", params={"id_pedido": id_pedido, "algoritmo": algoritmo})
            if resp:
                ruta = resp.get('ruta')
                if ruta:
                    logger.info(f"[UI] Ruta calculada exitosamente: {ruta}")
                    st.session_state['ruta_calculada'] = ruta
                    st.session_state['algoritmo_usado'] = algoritmo
                    st.session_state['pedidos_completados'].append(id_pedido)
                    st.experimental_rerun()
                else:
                    logger.warning(f"[UI] Respuesta sin ruta: {resp}")
                    st.error(f"No se pudo calcular la ruta. Respuesta: {resp}")
            else:
                logger.error(f"[UI] No se recibió respuesta del backend")
                st.error("No se recibió respuesta del backend para el cálculo de ruta")
        except Exception as e:
            logger.error(f"[UI] Error al calcular ruta: {e}")
            st.error(f"Error al calcular ruta: {e}")
            st.text(traceback.format_exc())
    if seleccion_pedido and seleccion_algoritmo:
        st.sidebar.button("Calcular Ruta", on_click=_callback_calcular,
                           args=(seleccion_pedido.get('id_pedido'), seleccion_algoritmo))
    # Mostrar resultado si ya ha sido calculado
    if 'ruta_calculada' in st.session_state and st.session_state['ruta_calculada']:
        ruta = st.session_state['ruta_calculada']
        algoritmo_usado = st.session_state.get('algoritmo_usado', 'desconocido')
        st.success(f"Ruta calculada con {algoritmo_usado}: {ruta}")
        # Mostrar grafo con ruta resaltada
        try:
            logger.info(f"[UI] Mostrando grafo con ruta resaltada: {ruta}")
            visualizar_grafo(vertices_list, aristas_list, ruta_resaltada=ruta)
        except Exception as e:
            logger.error(f"[UI] Error al mostrar grafo con ruta: {e}")
            st.error(f"Error al mostrar el grafo con la ruta: {e}")
        
        # Botón para limpiar la ruta calculada
        if st.sidebar.button("Limpiar Ruta"):
            del st.session_state['ruta_calculada']
            if 'algoritmo_usado' in st.session_state:
                del st.session_state['algoritmo_usado']
            st.experimental_rerun()
    logger.info("[UI] Renderizado de pestaña red finalizado.")
