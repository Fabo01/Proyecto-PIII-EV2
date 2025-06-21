import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def mostrar_estadisticas_generales(stats):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clientes", stats.get('total_clientes', 0))
    col2.metric("Almacenamientos", stats.get('total_almacenamientos', 0))
    col3.metric("Recargas", stats.get('total_recargas', 0))
    col4.metric("Pedidos", stats.get('total_pedidos', 0))
    st.write(f"Tiempo de respuesta: {stats.get('tiempo_respuesta', 0.0)}s")
    st.subheader("Vertices más visitados")
    vertices_visitados = stats.get('vertices_mas_visitados', {})
    if vertices_visitados:
        df_vertices = pd.DataFrame(list(vertices_visitados.items()), columns=['vertice', 'Visitas'])
        st.bar_chart(df_vertices.set_index('vertice'))
    st.subheader("Proporción de vertices por rol")
    roles = ['clientes', 'almacenamientos', 'recargas']
    valores = [stats.get(f'total_{r}', 0) for r in roles]
    fig, ax = plt.subplots()
    ax.pie(valores, labels=roles, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
