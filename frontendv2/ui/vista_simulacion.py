from streamlit.runtime.scriptrunner import RerunException, RerunData
import streamlit as st
from frontendv2.servicios.api import iniciar_simulacion, obtener_info_simulacion
from frontendv2.servicios.cache import inicializar_snapshot_datos, limpiar_cache_y_snapshot
from frontendv2.ui.utils import boton_actualizar_datos
import time

def mostrar():
    st.header("Ejecutar Simulación")
    # Botón para actualizar datos globales
    boton_actualizar_datos(key_suffix="_simulacion")
    st.info("Configura y lanza una nueva simulación logística de drones.")

    # Sliders para parámetros
    n_vertices = st.slider("Número de vértices", min_value=10, max_value=150, value=15)
    m_aristas = st.slider("Número de aristas", min_value=n_vertices-1, max_value=300, value=max(20, n_vertices-1))
    n_pedidos = st.slider("Número de Pedidos", min_value=10, max_value=300, value=10)

    # Info de proporciones
    st.markdown(f"""
    **Distribución esperada:**  
    - Clientes: {int(n_vertices*0.6)}  
    - Almacenamientos: {int(n_vertices*0.2)}  
    - Recargas: {int(n_vertices*0.2)}  
    """)

    if m_aristas < n_vertices - 1:
        st.error(f"El número mínimo de aristas para un grafo conexo con {n_vertices} vértices es {n_vertices-1}.")
        return

    if st.button("Iniciar Simulación"):
        limpiar_cache_y_snapshot()
        respuesta = iniciar_simulacion(n_vertices, m_aristas, n_pedidos)
        st.write("Respuesta iniciar_simulacion:", respuesta)
        info = obtener_info_simulacion()
        if info and info.get("clientes"):
            inicializar_snapshot_datos()
            st.success("Simulación iniciada correctamente.")
            raise RerunException(RerunData())
        st.warning("La simulación fue creada, pero los datos aún no están disponibles. Intenta actualizar en unos segundos.")

    # Mostrar estado actual solo si la simulación está iniciada
    info = obtener_info_simulacion()
    if info and info.get("clientes"):
        st.subheader("Estado actual de la simulación")
        st.json(info, expanded=False)
    else:
        st.warning("No hay simulación activa. Inicia una nueva simulación para ver el estado.")