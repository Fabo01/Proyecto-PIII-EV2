import streamlit as st
from frontend.servicios.api import api_post
from frontend.servicios.cache import cachear_estado_simulacion

def ui_simulacion():
    """
    Pestaña 1: Configuración e inicio de la simulación.
    """
    st.header("Configuración de la Simulación")
    n_vertices = st.slider("Número de vértices", 10, 150, 15, key="n_vertices")
    m_aristas = st.slider("Número de aristas", 10, 300, 20, key="m_aristas")
    n_pedidos = st.slider("Número de pedidos", 10, 300, 10, key="n_pedidos")
    st.info(f"Clientes: {int(n_vertices*0.6)} | Almacenamientos: {int(n_vertices*0.2)} | Recargas: {int(n_vertices*0.2)}")
    if st.button("Iniciar Simulación"):
        if m_aristas < n_vertices - 1:
            st.error("El número de aristas debe ser al menos n_vertices - 1 para asegurar conectividad.")
            return
        # Mostrar los parámetros antes de enviar la petición
        st.write("Parámetros enviados a la API:", {
            "n_vertices": n_vertices,
            "m_aristas": m_aristas,
            "n_pedidos": n_pedidos
        })
        resp = api_post("/simulacion/iniciar", {
            "n_vertices": n_vertices,
            "m_aristas": m_aristas,
            "n_pedidos": n_pedidos
        })
        if resp:
            st.success("¡Simulación iniciada!")
            st.session_state['simulacion_iniciada'] = True
            st.rerun()
        else:
            st.error("No se pudo iniciar la simulación. Revisa los parámetros o el backend.")
