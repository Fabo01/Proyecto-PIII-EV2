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

def mostrar_lista(nombre, hashmap):
    """
    Muestra un hashmap en formato JSON para debug o pretty print de objetos reales.
    """
    logger.info(f"[UI] Mostrando {nombre} (total: {len(hashmap) if hashmap else 0})")
    st.subheader(nombre)
    if hashmap:
        # Usar pretty print para mostrar objetos y referencias de forma legible
        texto_pretty = pprint.pformat(hashmap, indent=2, width=120)
        st.code(texto_pretty, language='python')
    else:
        st.info(f"No hay datos para {nombre}.")

@require_simulation_started
def ui_listas():
    """
    Pestaña de depuración: muestra todos los listas de entidades principales.
    Útil para debug y validación de integridad de datos.
    """
    st.header("Debug: Listas de Entidades")
    logger.info("[UI] Solicitando todos los listas de entidades antes de renderizar pestaña listas.")
    clientes = obtener_clientes_lista() or {}
    pedidos = obtener_pedidos_lista() or {}
    almacenamientos = obtener_almacenamientos_lista() or {}
    recargas = obtener_recargas_lista() or {}
    vertices = obtener_vertices_lista() or {}
    aristas = obtener_aristas_lista() or {}
    rutas = obtener_rutas_lista() or {}
    mostrar_lista("Lista de Clientes (ID → Objeto)", clientes)
    mostrar_lista("Lista de Pedidos (ID → Objeto)", pedidos)
    mostrar_lista("Lista de Almacenamientos (ID → Objeto)", almacenamientos)
    mostrar_lista("Lista de Recargas (ID → Objeto)", recargas)
    mostrar_lista("Lista de Vértices (ID → Objeto)", vertices)
    mostrar_lista("Lista de Aristas (Clave → Objeto)", aristas)
    mostrar_lista("Lista de Rutas (Clave → Objeto)", rutas)
    logger.info("[UI] Renderizado de pestaña listas finalizado.")
