import streamlit as st
from functools import wraps

# Decoradores para validaciones de estado y permisos en UI

def require_simulation_started(func):
    """
    Decorador que verifica que la simulación esté iniciada antes de ejecutar la función de UI.
    Si no está iniciada, muestra una advertencia y detiene la ejecución.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('simulacion_iniciada', False):
            st.warning("Primero debes iniciar una simulación en la pestaña 'Configuración de la Simulación'.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
