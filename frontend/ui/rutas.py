import streamlit as st
from frontend.servicios.api import api_get
from frontend.visualizacion.avl import visualizar_avl

def ui_rutas():
    """
    Pestaña 4: Análisis de rutas más frecuentes (AVL).
    """
    st.header("Rutas más frecuentes (AVL)")
    stats = api_get("/estadisticas/")
    rutas = stats.get('rutas_mas_frecuentes', []) if stats else []
    visualizar_avl(rutas)
