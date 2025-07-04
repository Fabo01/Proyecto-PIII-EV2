import streamlit as st
from frontendv2.ui import (
    vista_simulacion,
    vista_red,
    vista_clientes_pedidos,
    vista_rutas,
    vista_estadisticas,
    vista_debug
)
from frontendv2.servicios.cache import inicializar_snapshot_datos, limpiar_cache_y_snapshot
from streamlit.runtime.scriptrunner import RerunException, RerunData
from frontendv2.servicios.api import obtener_info_simulacion

def mostrar_menu():
    st.sidebar.title("Menú principal")
    pestañas = [
        ("1. Ejecutar Simulación", vista_simulacion.mostrar),
        ("2. Explorar Red", vista_red.mostrar),
        ("3. Clientes y Pedidos", vista_clientes_pedidos.mostrar),
        ("4. Análisis de Rutas", vista_rutas.mostrar),
        ("5. Estadísticas Generales", vista_estadisticas.mostrar),
        ("6. DEBUG: HashMaps (Extra)", vista_debug.mostrar)
    ]
    opciones = [p[0] for p in pestañas]
    seleccion = st.sidebar.radio("Selecciona una pestaña", opciones)
    for nombre, funcion in pestañas:
        if seleccion == nombre:
            funcion()
            break
    # Botón global para refrescar datos en sidebar
    st.sidebar.markdown('---')
    if st.sidebar.button('Actualizar datos de red', key='sidebar_actualizar'):
       info = obtener_info_simulacion()
       if info and info.get('clientes'):
            inicializar_snapshot_datos()
            st.success("Datos actualizados correctamente.")
            raise RerunException(RerunData())
       else:
           st.sidebar.error("No hay simulación activa. Inicia una nueva simulación para actualizar datos.")