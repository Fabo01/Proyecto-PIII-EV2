import streamlit as st
import logging
import pprint
from frontend.servicios.cache import (
    obtener_clientes_lista, obtener_pedidos_lista, obtener_almacenamientos_lista, obtener_recargas_lista,
    obtener_vertices_lista, obtener_aristas_lista, obtener_rutas_lista
)
from frontend.utils.validadores import require_simulation_started

logger = logging.getLogger("frontend.ui.listas")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def mostrar_lista(nombre, lista):
    """
    Muestra un lista en formato pretty print, manejando objetos no serializables y referencias circulares.
    """
    logger.info(f"[UI] Mostrando {nombre} (total: {len(lista) if lista else 0})")
    st.subheader(nombre)
    if lista:
        try:
            # Usar pprint para mostrar objetos y referencias
            st.text(pprint.pformat(lista, depth=3, compact=True, width=120))
        except Exception as e:
            logger.error(f"Error al mostrar lista con pprint: {e}")
            st.error(f"Error al mostrar el lista: {e}")
            st.write(lista)
    else:
        st.info(f"No hay datos para {nombre}.")

@require_simulation_started
def ui_listas():
    """
    Pestaña de depuración: muestra todos los listas de entidades principales.
    Útil para debug y validación de integridad de datos.
    """
    st.header("Debug: HashMaps de Entidades")
    logger.info("[UI] Solicitando todos los listas de entidades antes de renderizar pestaña listas.")
    clientes = obtener_clientes_lista() or {}
    pedidos = obtener_pedidos_lista() or {}
    almacenamientos = obtener_almacenamientos_lista() or {}
    recargas = obtener_recargas_lista() or {}
    vertices = obtener_vertices_lista() or {}
    aristas = obtener_aristas_lista() or {}
    rutas = obtener_rutas_lista() or {}
    mostrar_lista("HashMap de Clientes (ID → Objeto)", clientes)
    mostrar_lista("HashMap de Pedidos (ID → Objeto)", pedidos)
    mostrar_lista("HashMap de Almacenamientos (ID → Objeto)", almacenamientos)
    mostrar_lista("HashMap de Recargas (ID → Objeto)", recargas)
    mostrar_lista("HashMap de Vértices (ID → Objeto)", vertices)
    mostrar_lista("HashMap de Aristas (Clave → Objeto)", aristas)
    mostrar_lista("HashMap de Rutas (Clave → Objeto)", rutas)
    logger.info("[UI] Renderizado de pestaña listas finalizado.")
