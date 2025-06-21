import streamlit as st
from frontend.servicios.api import api_get
from frontend.visualizacion.grafo import visualizar_grafo

def ui_red():
    """
    Pestaña 2: Visualización y exploración de la red de drones.
    """
    st.header("Red de Drones")
    vertices = api_get("/vertices") or []
    aristas = api_get("/aristas") or []
    if not vertices or not aristas:
        st.warning("No hay datos suficientes para mostrar la red.")
        return
    visualizar_grafo(vertices, aristas)
    # Aquí se agregan selectores y lógica de rutas según requisitos
