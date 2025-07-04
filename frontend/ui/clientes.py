import logging
import streamlit as st
import pandas as pd
from frontend.servicios.cache import (
    obtener_clientes_lista, obtener_pedidos_lista, obtener_almacenamientos_lista
)
from frontend.utils.validadores import require_simulation_started

logger = logging.getLogger("frontend.ui.clientes")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def obtener_pedidos_asociados(ids_pedidos, pedidos_hm):
    """
    Devuelve una lista de pedidos válidos asociados a una lista de IDs, manejando IDs válidos incluso siendo 0.
    """
    if pedidos_hm is None:
        logger.info("Lista de pedidos no disponible para asociar.")
        return []
    pedidos = []
    for pid in ids_pedidos or []:
        try:
            pid_int = int(pid)
        except Exception:
            logger.warning(f"ID de pedido inválido: {pid}")
            continue
        pedido = pedidos_hm.get(pid_int)
        if isinstance(pedido, dict):
            pedidos.append(pedido)
        else:
            logger.warning(f"Pedido asociado no encontrado o inválido para ID: {pid_int}")
    if not pedidos:
        logger.info(f"No se encontraron pedidos válidos para los IDs: {ids_pedidos}")
    return pedidos

def ui_clientes():
    """
    Pestaña: Visualización de clientes y pedidos en tablas, con estadísticas.
    Cumple con modularidad, eficiencia y nombres en español.
    """
    # Validar estado de simulación
    @require_simulation_started
    def render_clientes():
        st.header("Clientes y Pedidos")
        logger.info("[UI] Solicitando listas de clientes, pedidos y almacenamientos antes de renderizar pestaña clientes.")
        clientes_list = obtener_clientes_lista() or []
        pedidos_list = obtener_pedidos_lista() or []
        almacenamientos_list = obtener_almacenamientos_lista() or []
        # Convertir listas en diccionarios para acceso por ID
        clientes_hm = {c['id']: c for c in clientes_list if 'id' in c}
        pedidos_hm = {p['id_pedido']: p for p in pedidos_list if 'id_pedido' in p}
        almacenamientos_hm = {a['id']: a for a in almacenamientos_list if 'id' in a}
        logger.info(f"[UI] listas recibidas: clientes={len(clientes_hm)}, pedidos={len(pedidos_hm)}, almacenamientos={len(almacenamientos_hm)}")
        # Mostrar clientes en DataFrame
        st.subheader("Clientes")
        if clientes_hm:
            df_clientes = pd.DataFrame(list(clientes_hm.values()))
            st.dataframe(df_clientes)
            st.info(f"Total de clientes: {len(clientes_hm)}")
        else:
            logger.warning("No hay clientes registrados.")
            st.warning("No hay clientes registrados.")
        # Mostrar pedidos por cliente
        st.subheader("Pedidos por Cliente")
        if not clientes_hm:
            logger.info("No hay clientes para mostrar pedidos.")
            st.info("No hay clientes para mostrar pedidos.")
        else:
            for id_cliente, cliente in clientes_hm.items():
                logger.info(f"[UI] Consultando pedidos asociados para cliente ID: {id_cliente}")
                st.markdown(f"**Cliente:** {cliente.get('nombre', 'Sin nombre')} (ID: {cliente.get('id', id_cliente)})")
                pedidos_cliente = obtener_pedidos_asociados(cliente.get('ids_pedidos', []), pedidos_hm)
                logger.info(f"[UI] Pedidos asociados encontrados: {len(pedidos_cliente)} para cliente ID: {id_cliente}")
                if pedidos_cliente:
                    df_pedidos = pd.DataFrame(pedidos_cliente)
                    st.dataframe(df_pedidos)
                else:
                    logger.info(f"Este cliente (ID: {cliente.get('id', id_cliente)}) no tiene pedidos asociados.")
                    st.info("Este cliente no tiene pedidos asociados.")
        # Mostrar pedidos por almacenamiento
        st.subheader("Pedidos por Almacenamiento")
        if not almacenamientos_hm:
            logger.info("No hay almacenamientos para mostrar pedidos.")
            st.info("No hay almacenamientos para mostrar pedidos.")
        else:
            for id_almacen, almacen in almacenamientos_hm.items():
                logger.info(f"[UI] Consultando pedidos asociados para almacenamiento ID: {id_almacen}")
                st.markdown(f"**Almacenamiento:** {almacen.get('nombre', 'Sin nombre')} (ID: {almacen.get('id', id_almacen)})")
                pedidos_almacen = obtener_pedidos_asociados(almacen.get('ids_pedidos', []), pedidos_hm)
                logger.info(f"[UI] Pedidos asociados encontrados: {len(pedidos_almacen)} para almacenamiento ID: {id_almacen}")
                if pedidos_almacen:
                    df_pedidos = pd.DataFrame(pedidos_almacen)
                    st.dataframe(df_pedidos)
                else:
                    logger.info(f"Este almacenamiento (ID: {almacen.get('id', id_almacen)}) no tiene pedidos asociados.")
                    st.info("Este almacenamiento no tiene pedidos asociados.")
        logger.info("[UI] Renderizado de pestaña clientes finalizado.")
    # Ejecutar renderizado con validación
    render_clientes()
