import streamlit as st
from frontend.servicios.api import api_get
from frontend.visualizacion.charts import mostrar_estadisticas_generales

def ui_estadisticas():
    """
    Pestaña 5: Estadísticas generales del sistema.
    Cumple con modularidad, robustez y nombres en español.
    """
    st.header("Estadísticas Generales")
    stats = api_get("/estadisticas/")
    if not stats:
        st.warning("Primero debes iniciar una simulación en la pestaña 'Configuración de la Simulación'.")
        st.stop()
    mostrar_estadisticas_generales(stats)
