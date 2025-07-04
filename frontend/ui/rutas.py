import streamlit as st
from frontend.servicios.cache import cachear_estadisticas
from frontend.visualizacion.avl import visualizar_avl
from frontend.utils.validadores import require_simulation_started

@require_simulation_started
def ui_rutas():
    """
    Pestaña 4: Análisis de rutas más frecuentes (AVL).
    Cumple con modularidad, robustez y nombres en español.
    """
    st.header("Rutas más frecuentes (AVL)")
    # Obtener estadísticas cacheadas
    stats = cachear_estadisticas() or {}
    rutas = stats.get('rutas_mas_frecuentes', []) if stats else []
    visualizar_avl(rutas)
