import streamlit as st
from frontendv2.ui.utils import boton_actualizar_datos

def mostrar():
    st.header("DEBUG: Inspección de Datos Planos (DTOs)")
    st.info("Inspección avanzada de los datos planos serializables (DTOs) de cada entidad. Solo para depuración y análisis de integridad de datos.")
    boton_actualizar_datos(key_suffix="_debug")

    if 'datos_red' not in st.session_state:
        st.warning("No hay datos disponibles. Inicia la simulación primero.")
        return

    datos = st.session_state['datos_red']
    tab_clientes, tab_pedidos, tab_almacenamientos, tab_recargas, tab_vertices, tab_aristas, tab_rutas = st.tabs([
        "Clientes", "Pedidos", "Almacenamientos", "Recargas", "Vértices", "Aristas", "Rutas"
    ])

    with tab_clientes:
        clientes = datos.get('clientes', [])
        if not clientes:
            st.warning("No hay clientes disponibles.")
        else:
            st.subheader("Clientes (DTO)")
            st.dataframe(clientes, use_container_width=True)
            for cliente in clientes:
                with st.expander(f"Detalle Cliente {cliente.get('id_cliente') or cliente.get('id')}"):
                    st.json(cliente, expanded=False)

    with tab_pedidos:
        pedidos = datos.get('pedidos', [])
        if not pedidos:
            st.warning("No hay pedidos disponibles.")
        else:
            st.subheader("Pedidos (DTO)")
            st.dataframe(pedidos, use_container_width=True)
            for pedido in pedidos:
                with st.expander(f"Detalle Pedido {pedido.get('id_pedido') or pedido.get('id')}"):
                    st.json(pedido, expanded=False)

    with tab_almacenamientos:
        almacenamientos = datos.get('almacenamientos', [])
        if not almacenamientos:
            st.warning("No hay almacenamientos disponibles.")
        else:
            st.subheader("Almacenamientos (DTO)")
            st.dataframe(almacenamientos, use_container_width=True)
            for almacen in almacenamientos:
                with st.expander(f"Detalle Almacenamiento {almacen.get('id_almacenamiento') or almacen.get('id')}"):
                    st.json(almacen, expanded=False)

    with tab_recargas:
        recargas = datos.get('recargas', [])
        if not recargas:
            st.warning("No hay recargas disponibles.")
        else:
            st.subheader("Recargas (DTO)")
            st.dataframe(recargas, use_container_width=True)
            for recarga in recargas:
                with st.expander(f"Detalle Recarga {recarga.get('id_recarga') or recarga.get('id')}"):
                    st.json(recarga, expanded=False)

    with tab_vertices:
        vertices = datos.get('vertices', [])
        if not vertices:
            st.warning("No hay vértices disponibles.")
        else:
            st.subheader("Vértices (DTO)")
            st.dataframe(vertices, use_container_width=True)
            for vertice in vertices:
                with st.expander(f"Detalle Vértice {vertice.get('id')}"):
                    st.json(vertice, expanded=False)

    with tab_aristas:
        aristas = datos.get('aristas', [])
        if not aristas:
            st.warning("No hay aristas disponibles.")
        else:
            st.subheader("Aristas (DTO)")
            st.dataframe(aristas, use_container_width=True)
            for arista in aristas:
                with st.expander(f"Detalle Arista {arista.get('id') if 'id' in arista else arista}"):
                    st.json(arista, expanded=False)

    with tab_rutas:
        rutas = datos.get('rutas', [])
        if not rutas:
            st.warning("No hay rutas disponibles.")
        else:
            st.subheader("Rutas (DTO)")
            st.dataframe(rutas, use_container_width=True)
            for ruta in rutas:
                with st.expander(f"Detalle Ruta {ruta.get('id_ruta') if 'id_ruta' in ruta else ruta}"):
                    st.json(ruta, expanded=False)