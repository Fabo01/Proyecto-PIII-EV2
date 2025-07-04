import streamlit as st
from frontendv2.servicios.api import (
    obtener_clientes_dto,
    obtener_pedidos_dto,
    obtener_almacenamientos_dto,
    obtener_recargas_dto,
    obtener_vertices_dto,
    obtener_aristas_dto,
    obtener_rutas_dto,
    obtener_estadisticas_dto
)

@st.cache_data(ttl=10, show_spinner=False)
def cachear_clientes():
    return obtener_clientes_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_pedidos():
    return obtener_pedidos_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_almacenamientos():
    return obtener_almacenamientos_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_recargas():
    return obtener_recargas_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_vertices():
    return obtener_vertices_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_aristas():
    return obtener_aristas_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_rutas():
    return obtener_rutas_dto()

@st.cache_data(ttl=10, show_spinner=False)
def cachear_estadisticas():
    return obtener_estadisticas_dto()

def inicializar_snapshot_datos():
    """
    Inicializa el snapshot de datos de red en st.session_state['datos_red'].
    Carga todos los datos relevantes y los almacena para acceso global en la app.
    """
    datos = {
        'clientes': cachear_clientes(),
        'pedidos': cachear_pedidos(),
        'almacenamientos': cachear_almacenamientos(),
        'recargas': cachear_recargas(),
        'vertices': cachear_vertices(),
        'aristas': cachear_aristas(),
        'rutas': cachear_rutas(),
        'estadisticas': cachear_estadisticas(),
    }
    st.session_state['datos_red'] = datos
    return datos


def limpiar_cache_y_snapshot():
    """
    Limpia el snapshot de datos y todos los caches DTO relevantes.
    Llamar esta función cada vez que se requiera refrescar los datos en toda la app.
    """
    st.session_state.pop('datos_red', None)
    cachear_clientes.clear()
    cachear_pedidos.clear()
    cachear_almacenamientos.clear()
    cachear_recargas.clear()
    cachear_vertices.clear()
    cachear_aristas.clear()
    cachear_rutas.clear()
    cachear_estadisticas.clear()