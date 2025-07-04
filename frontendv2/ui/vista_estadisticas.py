"""
Vista para la visualización de estadísticas generales de la simulación.
Consume endpoints DTO para mostrar métricas y gráficos.
"""

import streamlit as st
from frontendv2.servicios.cache import inicializar_snapshot_datos
from frontendv2.ui.utils import boton_actualizar_datos

def mostrar():
    st.header("Estadísticas de la simulación")
    # Botón para actualizar datos globales
    boton_actualizar_datos(key_suffix="_estadisticas")
    st.info("Visualiza métricas y gráficos de la simulación logística.")
    # Depender de snapshot único de datos
    if 'datos_red' not in st.session_state:
        st.warning("No hay datos disponibles. Inicia la simulación primero.")
        return
    datos = st.session_state['datos_red']
    estadisticas = datos.get('estadisticas', {})
    if not estadisticas:
        st.warning("No hay estadísticas disponibles en la simulación.")
        return
    # Mostrar métricas globales
    st.subheader("Métricas generales")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Clientes", estadisticas.get('total_clientes', 0))
    col2.metric("Almacenamientos", estadisticas.get('total_almacenamientos', 0))
    col3.metric("Recargas", estadisticas.get('total_recargas', 0))
    col4.metric("Vértices totales", estadisticas.get('total_vertices', 0))
    col5.metric("Aristas totales", estadisticas.get('total_aristas', 0))
    col6.metric("Pedidos totales", estadisticas.get('total_pedidos', 0))
    st.write(f"Tiempo de respuesta: {estadisticas.get('tiempo_respuesta', 0.0):.4f}s")
    # Estadísticas adicionales
    col7, col8 = st.columns(2)
    col7.metric("Rutas únicas", estadisticas.get('total_rutas_unicas', 0))
    col8.metric("Promedio pedidos/cliente", f"{estadisticas.get('promedio_pedidos_por_cliente', 0.0):.2f}")

    import pandas as pd
    import matplotlib.pyplot as plt

    # Visitas por tipo de vértice
    st.subheader("Visitas por tipo de vértice")
    visitas = estadisticas.get('vertices_mas_visitados', {})
    vertices = datos.get('vertices', [])
    tipo_map = {v.get('id', None): v.get('tipo', 'desconocido') for v in vertices}
    visitas_tipo = {}
    for vid, cnt in visitas.items():
        tipo = tipo_map.get(vid, 'desconocido')
        visitas_tipo[tipo] = visitas_tipo.get(tipo, 0) + cnt
    if visitas_tipo:
        df_visitas = pd.DataFrame.from_dict(visitas_tipo, orient='index', columns=['Visitas'])
        st.bar_chart(df_visitas)
    else:
        st.info("No hay visitas registradas.")

    # Proporción de vértices por rol
    st.subheader("Proporción de vértices por rol")
    vpt = estadisticas.get('vertices_por_tipo', {})
    if vpt:
        fig, ax = plt.subplots()
        roles = list(vpt.keys())
        valores = list(vpt.values())
        ax.pie(valores, labels=roles, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No hay datos de vértices por tipo.")

    # Pedidos por estado
    st.subheader("Pedidos por estado")
    ppe = estadisticas.get('pedidos_por_estado', {})
    if ppe:
        df_ppe = pd.DataFrame.from_dict(ppe, orient='index', columns=['Cantidad'])
        st.bar_chart(df_ppe)
    else:
        st.info("No hay datos de pedidos por estado.")

    # Pedidos por cliente
    st.subheader("Pedidos por cliente")
    ppc = estadisticas.get('pedidos_por_cliente', {})
    clientes = datos.get('clientes', [])
    nombre_map = {c.get('id_cliente', c.get('id')): c.get('nombre', str(c.get('id')) ) for c in clientes}
    if ppc:
        data = [(nombre_map.get(cid, str(cid)), cnt) for cid, cnt in ppc.items()]
        df_ppc = pd.DataFrame(data, columns=['Cliente', 'Cantidad']).set_index('Cliente')
        st.bar_chart(df_ppc)
    else:
        st.info("No hay datos de pedidos por cliente.")

    # Rutas más frecuentes
    st.subheader("Rutas más frecuentes")
    rutas = estadisticas.get('rutas_mas_frecuentes', [])
    if rutas:
        tabla = [
            {'Camino': ' → '.join(str(n) for n in r.get('camino', [])), 'Frecuencia': r.get('frecuencia', 1)}
            for r in rutas
        ]
        st.table(pd.DataFrame(tabla))
    else:
        st.info("No hay rutas frecuentes registradas.")
