"""
Vista para la pestaña 3: Clientes y Pedidos.
Lista clientes activos y pedidos generados, mostrando atributos relevantes.
Permite marcar pedidos como completados (entregados).
"""

import streamlit as st
from frontendv2.servicios.cache import inicializar_snapshot_datos, limpiar_cache_y_snapshot
from frontendv2.ui.utils import boton_actualizar_datos
from frontendv2.servicios.api import actualizar_estado_pedido, calcular_ruta
import logging

logger = logging.getLogger("frontendv2.ui.vista_clientes_pedidos")

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
            
            # Funciones auxiliares para manejo de estado
            def marcar_pedido_completado(pedido_id, pedido_info):
                """Marca un pedido como completado (entregado)"""
                try:
                    with st.spinner(f"Marcando pedido {pedido_id} como entregado..."):
                        resultado = actualizar_estado_pedido(pedido_id, "entregado")
                        st.success(f"✅ Pedido {pedido_id} marcado como entregado exitosamente")
                        
                        # Limpiar cache y forzar recarga de datos
                        if 'datos_red' in st.session_state:
                            st.session_state.pop('datos_red')
                        limpiar_cache_y_snapshot()
                        
                        # Rerun para actualizar la interfaz
                        st.rerun()
                        
                except Exception as e:
                    logger.error(f"Error al marcar pedido {pedido_id} como entregado: {str(e)}")
                    st.error(f"❌ Error al marcar pedido como entregado: {str(e)}")
            
            def puede_calcular_ruta_pedido(pedido_status):
                """Verifica si se puede calcular ruta para un pedido según su estado"""
                return pedido_status and pedido_status.lower() != 'entregado'
            
            # Tabla de pedidos con información de estado
            pedidos_tabla = []
            for p in pedidos:
                status = p.get("status", "").lower()
                status_display = p.get("status", "pendiente")
                
                # Aplicar colores según el estado
                if status == "entregado":
                    status_emoji = "✅"
                elif status == "en_ruta":
                    status_emoji = "🚛"
                else:
                    status_emoji = "⏳"
                
                pedidos_tabla.append({
                    "ID": p.get("id_pedido") or p.get("id"),
                    "Estado": f"{status_emoji} {status_display}",
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
                    "Prioridad": p.get("prioridad"),
                    "Fecha creación": p.get("fecha_creacion"),
                    "Fecha entrega": p.get("fecha_entrega") or "No entregado",
                    "Costo total": p.get("peso_total") or p.get("costo_total") or "N/A"
                })
            
            st.dataframe(pedidos_tabla, use_container_width=True)
            
            # Acciones sobre pedidos individuales
            st.subheader("Acciones sobre Pedidos")
            
            # Separar pedidos por estado para facilitar la gestión
            pedidos_pendientes = [p for p in pedidos if p.get("status", "").lower() != "entregado"]
            pedidos_entregados = [p for p in pedidos if p.get("status", "").lower() == "entregado"]
            
            if pedidos_pendientes:
                st.write("**Pedidos Pendientes/En Ruta:**")
                
                # Crear columnas para cada pedido pendiente
                for i, pedido in enumerate(pedidos_pendientes):
                    pedido_id = pedido.get("id_pedido") or pedido.get("id")
                    status = pedido.get("status", "pendiente")
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        cliente_nombre = (
                            pedido.get("cliente", {}).get("nombre")
                            if isinstance(pedido.get("cliente"), dict)
                            else pedido.get("cliente", "Cliente desconocido")
                        )
                        st.write(f"**Pedido {pedido_id}** - Cliente: {cliente_nombre} - Estado: {status}")
                    
                    with col2:
                        # Botón para calcular ruta (solo si no está entregado)
                        if puede_calcular_ruta_pedido(status):
                            if st.button(f"📍 Calcular Ruta", key=f"calc_ruta_{pedido_id}"):
                                try:
                                    with st.spinner(f"Calculando ruta para pedido {pedido_id}..."):
                                        resultado = calcular_ruta(pedido_id, "dijkstra")
                                        if resultado:
                                            st.success(f"✅ Ruta calculada para pedido {pedido_id}")
                                            st.json(resultado, expanded=False)
                                        else:
                                            st.warning(f"⚠️ No se pudo calcular ruta para pedido {pedido_id}")
                                except Exception as e:
                                    st.error(f"❌ Error al calcular ruta: {str(e)}")
                        else:
                            st.button(f"🚫 Ruta no disponible", key=f"no_calc_{pedido_id}", disabled=True)
                    
                    with col3:
                        # Botón para marcar como completado
                        if status.lower() != "entregado":
                            if st.button(f"✅ Marcar Entregado", key=f"completar_{pedido_id}"):
                                marcar_pedido_completado(pedido_id, pedido)
                        else:
                            st.button(f"✅ Ya Entregado", key=f"ya_entregado_{pedido_id}", disabled=True)
                    
                    st.divider()
            else:
                st.info("No hay pedidos pendientes.")
            
            if pedidos_entregados:
                st.write("**Pedidos Entregados:**")
                for pedido in pedidos_entregados:
                    pedido_id = pedido.get("id_pedido") or pedido.get("id")
                    cliente_nombre = (
                        pedido.get("cliente", {}).get("nombre")
                        if isinstance(pedido.get("cliente"), dict)
                        else pedido.get("cliente", "Cliente desconocido")
                    )
                    fecha_entrega = pedido.get("fecha_entrega", "Fecha no registrada")
                    st.success(f"✅ **Pedido {pedido_id}** - Cliente: {cliente_nombre} - Entregado: {fecha_entrega}")
            
            # Detalles expandibles de cada pedido
            st.subheader("Detalles de Pedidos")
            for pedido in pedidos:
                pedido_id = pedido.get('id_pedido') or pedido.get('id')
                status = pedido.get('status', 'pendiente')
                status_emoji = "✅" if status.lower() == "entregado" else ("🚛" if status.lower() == "en_ruta" else "⏳")
                
                with st.expander(f"{status_emoji} Detalle Pedido {pedido_id} ({status})"):
                    st.json(pedido, expanded=False)