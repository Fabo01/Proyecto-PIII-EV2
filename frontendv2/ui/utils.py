import streamlit as st
from frontendv2.servicios.cache import limpiar_cache_y_snapshot, inicializar_snapshot_datos
from streamlit.runtime.scriptrunner import RerunException, RerunData

def boton_actualizar_datos(key_suffix: str = ''):
    """
    Botón para actualizar datos de la aplicación desde cualquier vista.
    Limpia el caché, inicializa el snapshot y fuerza un rerun.
    key_suffix: sufijo único para la key del botón.
    """
    if st.button("Actualizar datos de red", key=f"actualizar{key_suffix}"):
        limpiar_cache_y_snapshot()
        inicializar_snapshot_datos()
        raise RerunException(RerunData())
