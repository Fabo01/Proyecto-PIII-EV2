import streamlit as st
from frontend.servicios.cache import cachear_estadisticas
from frontend.visualizacion.charts import mostrar_estadisticas_generales
from frontend.utils.validadores import require_simulation_started

@require_simulation_started
def ui_estadisticas():
    """
    Pestaña 5: Estadísticas generales del sistema.
    Cumple con modularidad, robustez y nombres en español.
    """
    st.header("Estadísticas Generales")
    stats = cachear_estadisticas()
    if not stats:
        st.warning("No hay estadísticas disponibles. Asegúrate de que la simulación esté iniciada.")
        st.stop()
    mostrar_estadisticas_generales(stats)
