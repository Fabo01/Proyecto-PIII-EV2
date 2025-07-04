import streamlit as st
import logging
import networkx as nx
from pyvis.network import Network
from frontend.servicios.cache import (
    obtener_vertices_lista, obtener_aristas_lista, obtener_pedidos_lista, obtener_clientes_lista, obtener_almacenamientos_lista
)

def construir_grafo_pyvis(vertices, aristas):
    """
    Construye un grafo interactivo usando Pyvis a partir de los vértices y aristas del sistema.
    Garantiza colores y etiquetas coherentes con la lógica de dominio.
    Audita y loguea aristas inválidas.
    """
    logger = logging.getLogger("frontend.ui.red_interactiva")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    G = nx.Graph()
    vertices_ids = {v['id'] for v in vertices}
    for v in vertices:
        G.add_node(v['id'], label=v.get('nombre', str(v['id'])), tipo=v.get('tipo', ''))
    aristas_validas = 0
    for a in aristas:
        # Extraer IDs de origen y destino de arista en keys comunes
        origen = a.get('origen') or a.get('id_origen') or a.get('origen_id')
        destino = a.get('destino') or a.get('id_destino') or a.get('destino_id')
        if not isinstance(origen, int) or not isinstance(destino, int):
            logger.warning(f"Arista inválida o con IDs no enteros: {a}")
            st.warning(f"Arista inválida detectada y omitida: {a}")
            continue
        if origen not in vertices_ids or destino not in vertices_ids:
            logger.warning(f"Arista con IDs que no existen en vertices: {a}")
            st.warning(f"Arista con IDs inexistentes en vertices: {a}")
            continue
        peso = a.get('peso') or a.get('weight') or 1
        try:
            peso = float(peso)
        except Exception:
            peso = 1
        G.add_edge(origen, destino, weight=peso)
        aristas_validas += 1
    if aristas_validas == 0:
        logger.error("No se pudo construir ninguna arista válida para el grafo interactivo. Revisa la estructura de los datos de aristas en el backend/API.")
    net = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')
    net.from_nx(G)
    for node in net.nodes:
        tipo = node.get('tipo', '')
        if tipo == 'cliente':
            node['color'] = '#1f77b4'
        elif tipo == 'almacenamiento':
            node['color'] = '#2ca02c'
        elif tipo == 'recarga':
            node['color'] = '#ff7f0e'
        else:
            node['color'] = '#cccccc'
    return net

def resolver_asociaciones_pedido(pedido, clientes_hm, almacenamientos_hm):
    """
    Dado un pedido y los listas, retorna (cliente_obj, almacen_obj) asociados.
    Si no existen, retorna None y loguea advertencia.
    """
    logger = logging.getLogger("frontend.ui.red_interactiva")
    # Extraer IDs de pedido en distintos formatos
    # Buscar id correcto, considerar 0 como valor válido
    id_cliente = pedido.get('id_cliente', pedido.get('cliente_id', pedido.get('destino_id', pedido.get('cliente', None))))
    id_almacen = pedido.get('id_almacenamiento', pedido.get('origen_id', pedido.get('origen', None)))
    # Validar id_cliente
    if id_cliente is None:
        logger.warning(f"[Asociacion] Pedido {pedido.get('id_pedido')} sin 'id_cliente'.")
    elif not isinstance(id_cliente, int):
        logger.warning(f"[Asociacion] Pedido {pedido.get('id_pedido')} id_cliente no entero: {id_cliente}")
    elif id_cliente not in clientes_hm:
        logger.warning(f"[Asociacion] Pedido {pedido.get('id_pedido')} cliente no encontrado. id_cliente={id_cliente}")
    # Validar id_almacenamiento
    if id_almacen is None:
        logger.warning(f"[Asociacion] Pedido {pedido.get('id_pedido')} sin 'id_almacenamiento'.")
    elif not isinstance(id_almacen, int):
        logger.warning(f"[Asociacion] Pedido {pedido.get('id_pedido')} id_almacen no entero: {id_almacen}")
    elif id_almacen not in almacenamientos_hm:
        logger.warning(f"[Asociacion] Pedido {pedido.get('id_pedido')} almacen no encontrado. id_almacenamiento={id_almacen}")
    # Obtener objetos
    cliente = clientes_hm.get(id_cliente)
    almacen = almacenamientos_hm.get(id_almacen)
    return cliente, almacen

def auditar_asociaciones_pedidos(pedidos, clientes_hm, almacenamientos_hm):
    """
    Audita y muestra advertencias si algún pedido no está correctamente asociado a cliente u origen.
    Además, muestra los datos completos si existen.
    """
    logger = logging.getLogger("frontend.ui.red_interactiva")
    # Auditoria detallada de cada asociacion
    for pedido in pedidos:
        # Extraer ids consistentemente
        id_cliente = pedido.get('id_cliente', pedido.get('cliente_id', pedido.get('destino_id', pedido.get('cliente', None))))
        id_almacen = pedido.get('id_almacenamiento', pedido.get('origen_id', pedido.get('origen', None)))
        cliente = clientes_hm.get(id_cliente)
        almacen = almacenamientos_hm.get(id_almacen)
        # Validaciones y mensajes con prioridad y estado
        if id_cliente is None:
            msg = f"[Audit] Pedido {pedido.get('id_pedido')} sin id_cliente. Prioridad={pedido.get('prioridad')} Status={pedido.get('status')}"
            st.warning(msg)
            logger.warning(msg)
        elif not cliente:
            msg = f"[Audit] Pedido {pedido.get('id_pedido')} cliente no encontrado: id_cliente={id_cliente} Prioridad={pedido.get('prioridad')} Status={pedido.get('status')}"
            st.warning(msg)
            logger.warning(msg)
        if id_almacen is None:
            msg = f"[Audit] Pedido {pedido.get('id_pedido')} sin id_almacenamiento. Prioridad={pedido.get('prioridad')} Status={pedido.get('status')}"
            st.warning(msg)
            logger.warning(msg)
        elif not almacen:
            msg = f"[Audit] Pedido {pedido.get('id_pedido')} almacen no encontrado: id_almacenamiento={id_almacen} Prioridad={pedido.get('prioridad')} Status={pedido.get('status')}"
            st.warning(msg)
            logger.warning(msg)
        # Asociacion correcta
        if cliente and almacen:
            st.success(
                f"Pedido {pedido.get('id_pedido')} asociado correctamente:\n"
                f"• Cliente: [{id_cliente}] {cliente.get('nombre')}\n"
                f"• Almacen: [{id_almacen}] {almacen.get('nombre')}\n"
                f"Prioridad: {pedido.get('prioridad')} | Status: {pedido.get('status')}"
            )

def normalizar_aristas(aristas_hm):
    """
    Convierte el dict de aristas {clave: arista} en una lista de aristas planas.
    Soporta tanto dict plano como lista.
    """
    if isinstance(aristas_hm, dict):
        aristas = []
        for v in aristas_hm.values():
            if isinstance(v, dict) and 'origen' in v and 'destino' in v:
                aristas.append(v)
            elif isinstance(v, dict):
                # Si es un dict anidado (ej: {'(0,6)': {...}})
                for sub_v in v.values():
                    if isinstance(sub_v, dict) and 'origen' in sub_v and 'destino' in sub_v:
                        aristas.append(sub_v)
        return aristas
    elif isinstance(aristas_hm, list):
        return aristas_hm
    return []

def ui_red_interactiva():
    """
    Pestaña: Red Interactiva (Pyvis)
    Visualiza el grafo logístico con interactividad avanzada, manteniendo coherencia con la arquitectura y lógica del sistema.
    """
    st.header("Red Interactiva (Pyvis)")
    st.markdown("Esta visualización utiliza Pyvis (vis.js) para una experiencia interactiva avanzada. Puedes arrastrar, hacer zoom y explorar la red de drones.")
    vertices_hm = obtener_vertices_lista() or {}
    aristas_hm = obtener_aristas_lista() or {}
    pedidos_hm = obtener_pedidos_lista() or {}
    clientes_hm = obtener_clientes_lista() or {}
    almacenamientos_hm = obtener_almacenamientos_lista() or {}
    # Convertir claves de listas a enteros para garantizar búsquedas correctas por ID
    try:
        vertices_hm = {int(k): v for k, v in vertices_hm.items()}
        aristas_hm = {int(k): v for k, v in aristas_hm.items()}
        pedidos_hm = {int(k): v for k, v in pedidos_hm.items()}
        clientes_hm = {int(k): v for k, v in clientes_hm.items()}
        almacenamientos_hm = {int(k): v for k, v in almacenamientos_hm.items()}
    except Exception:
        pass
    vertices = list(vertices_hm.values())
    aristas = normalizar_aristas(aristas_hm)
    if not vertices or not aristas:
        st.warning("No hay datos de red disponibles para grafo interactivo.")
        return
    net = construir_grafo_pyvis(vertices, aristas)
    if len(net.edges) == 0:
        st.error("No se pudo construir ninguna arista válida para el grafo interactivo. Revisa la estructura de los datos de aristas en el backend/API.")
    st.info(f"Vertices: {len(net.nodes)} | Aristas: {len(net.edges)}")
    # Auditoría de asociaciones de pedidos
    pedidos = list(pedidos_hm.values())
    auditar_asociaciones_pedidos(pedidos, clientes_hm, almacenamientos_hm)
    st.caption("Colores: Azul=Cliente, Verde=Almacenamiento, Naranja=Recarga")
