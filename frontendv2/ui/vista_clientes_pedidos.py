"""
Vista para la pestaña 3: Clientes y Pedidos.
Lista clientes activos y pedidos generados, mostrando atributos relevantes.
"""

import streamlit as st
from frontendv2.servicios.cache import inicializar_snapshot_datos, limpiar_cache_y_snapshot
from frontendv2.ui.utils import boton_actualizar_datos

def mostrar():
    st.header("Clientes y Pedidos")
    # Botón para actualizar datos globales
    boton_actualizar_datos(key_suffix="_clientes_pedidos")
    st.info("Lista los clientes activos y los pedidos generados.")
    # Verificar simulación iniciada y snapshot
    if 'datos_red' not in st.session_state:
        st.warning("No hay datos disponibles. Inicia la simulación primero.")
        return
    datos = st.session_state['datos_red']
    clientes = datos['clientes']
    pedidos = datos['pedidos']

    tab_clientes, tab_pedidos = st.tabs(["Clientes", "Pedidos"])

    with tab_clientes:
        if not clientes:
            st.warning("No hay clientes disponibles o error al cargar datos.")
        else:
            st.subheader("Clientes")
            clientes_tabla = [
                {
                    "ID": c.get("id_cliente") or c.get("id"),
                    "Nombre": c.get("nombre"),
                    "Tipo": c.get("tipo"),
                    "Total pedidos": len(c.get("pedidos", []) or [])
                }
                for c in clientes
            ]
            st.dataframe(clientes_tabla, use_container_width=True)
            for cliente in clientes:
                if cliente.get('pedidos'):
                    with st.expander(f"Pedidos de {cliente.get('nombre')} (Total: {len(cliente['pedidos'])})"):
                        for pedido_id in cliente['pedidos']:
                            pedido_obj = next((p for p in pedidos if p.get('id_pedido') == pedido_id or p.get('id') == pedido_id), None)
                            if pedido_obj:
                                st.json(pedido_obj, expanded=False)
                            else:
                                st.warning(f"Pedido {pedido_id} no encontrado.")
    with tab_pedidos:
        if not pedidos:
            st.warning("No hay pedidos disponibles o error al cargar datos.")
        else:
            st.subheader("Pedidos")
            pedidos_tabla = [
                {
                    "ID": p.get("id_pedido") or p.get("id"),
                    "Cliente": (
                        p.get("cliente", {}).get("nombre")
                        if isinstance(p.get("cliente"), dict)
                        else p.get("cliente")
                    ),
                    "Origen": (
                        p.get("origen", {}).get("nombre")
                        if isinstance(p.get("origen"), dict)
                        else p.get("origen")
                    ),
                    "Destino": (
                        p.get("destino", {}).get("nombre")
                        if isinstance(p.get("destino"), dict)
                        else p.get("destino")
                    ),
                    "Status": p.get("status"),
                    "Prioridad": p.get("prioridad"),
                    "Fecha creación": p.get("fecha_creacion"),
                    "Fecha entrega": p.get("fecha_entrega"),
                    "Costo total": p.get("peso_total") or p.get("costo_total")
                }
                for p in pedidos
            ]
            st.dataframe(pedidos_tabla, use_container_width=True)
            for pedido in pedidos:
                with st.expander(f"Detalle Pedido {pedido.get('id_pedido') or pedido.get('id')}"):
                    st.json(pedido, expanded=False)