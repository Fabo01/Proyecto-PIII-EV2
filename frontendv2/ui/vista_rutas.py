"""
Pestaña 4: Análisis de Rutas
Visualización avanzada y análisis profundo de rutas, algoritmos y estadísticas.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from frontendv2.servicios.cache import (
    inicializar_snapshot_datos, limpiar_cache_y_snapshot,
    cachear_estadisticas, cachear_rutas
)
from frontendv2.ui.utils import boton_actualizar_datos

def mostrar():
    st.header("Análisis de Rutas")
    boton_actualizar_datos(key_suffix="_rutas")
    if 'datos_red' not in st.session_state:
        st.warning("No hay datos disponibles. Inicia la simulación primero.")
        return
    datos = st.session_state['datos_red']
    rutas = datos.get('rutas', [])
    estadisticas = datos.get('estadisticas', {})

    if not rutas:
        st.warning("No hay rutas disponibles en la simulación.")
        return

    tabs = st.tabs([
        "AVL de Frecuencias", 
        "Comparativa de Algoritmos", 
        "Rutas Extremas", 
        "Gráficos y Tiempos", 
        "Detalles Avanzados"
    ])

    # TAB 1: AVL de Frecuencias
    with tabs[0]:
        st.subheader("Árbol AVL de Frecuencias de Rutas")
        rutas_ordenadas = sorted(rutas, key=lambda r: r.get('frecuencia', 0), reverse=True)
        
        def procesar_camino(camino):
            """Procesa el camino de manera segura, manejando aristas o vértices"""
            if not camino:
                return "Sin camino"
            
            try:
                # Si es una lista de aristas (objetos con origen y destino)
                if isinstance(camino, list) and len(camino) > 0:
                    if isinstance(camino[0], dict) and 'origen' in camino[0] and 'destino' in camino[0]:
                        # Es una lista de aristas
                        vertices = []
                        for i, arista in enumerate(camino):
                            if i == 0:
                                # Agregar origen de la primera arista
                                origen = arista.get('origen', {})
                                origen_nombre = origen.get('nombre') if isinstance(origen, dict) else str(origen)
                                vertices.append(origen_nombre)
                            
                            # Agregar destino de cada arista
                            destino = arista.get('destino', {})
                            destino_nombre = destino.get('nombre') if isinstance(destino, dict) else str(destino)
                            vertices.append(destino_nombre)
                        
                        return " -> ".join(vertices)
                    
                    elif isinstance(camino[0], dict) and ('nombre' in camino[0] or 'id' in camino[0]):
                        # Es una lista de vértices
                        return " -> ".join([v.get("nombre", str(v.get("id", v))) for v in camino])
                    
                    elif isinstance(camino[0], (int, str)):
                        # Es una lista de IDs simples
                        return " -> ".join([str(v) for v in camino])
                    
                    else:
                        # Fallback para otros tipos
                        return f"Camino ({len(camino)} elementos)"
                
                return str(camino)
            
            except Exception as e:
                return f"Error procesando camino: {str(e)[:30]}..."
        
        def obtener_nombre_seguro(elemento, prefijo=""):
            """Obtiene el nombre de manera segura de un elemento origen/destino"""
            if not elemento:
                return f"{prefijo}Sin_datos"
            
            if isinstance(elemento, dict):
                return elemento.get("nombre", elemento.get("id", f"{prefijo}elemento_{hash(str(elemento)) % 1000}"))
            elif hasattr(elemento, 'nombre'):
                return elemento.nombre
            elif hasattr(elemento, 'id_vertice'):
                return f"{prefijo}V_{elemento.id_vertice}"
            else:
                return f"{prefijo}{str(elemento)}"
        
        tabla = [
            {
                "ID": r.get("id", "-"),
                "Origen": obtener_nombre_seguro(r.get("origen"), "Origen_"),
                "Destino": obtener_nombre_seguro(r.get("destino"), "Destino_"),
                "Frecuencia": r.get("frecuencia", "-"),
                "Distancia total": r.get("distancia_total", r.get("peso_total", "-")),
                "Camino": procesar_camino(r.get("camino", []))
            }
            for r in rutas_ordenadas
        ]
        st.dataframe(tabla, use_container_width=True)
        # AVL visual (si tienes función de visualización)
        if hasattr(st, "avl_plot"):
            st.avl_plot(rutas_ordenadas)
        st.caption("Las rutas se ordenan por frecuencia de uso.")

    # TAB 2: Comparativa de Algoritmos
    with tabs[1]:
        st.subheader("Comparativa de Algoritmos de Ruteo")
        if "comparativa_algoritmos" in estadisticas:
            df = pd.DataFrame(estadisticas["comparativa_algoritmos"])
            st.dataframe(df)
            st.bar_chart(df.set_index("algoritmo")["tiempo_promedio"])
        else:
            st.info("No hay datos comparativos de algoritmos disponibles.")

    # TAB 3: Rutas Extremas
    with tabs[2]:
        st.subheader("Ruta más corta y más larga")
        if rutas_ordenadas:
            def obtener_distancia_segura(ruta):
                """Obtiene la distancia/peso de manera segura"""
                return ruta.get('distancia_total', ruta.get('peso_total', 0))
            
            # Filtrar rutas que tengan distancia válida
            rutas_con_distancia = [r for r in rutas_ordenadas if obtener_distancia_segura(r) > 0]
            
            if rutas_con_distancia:
                ruta_corta = min(rutas_con_distancia, key=obtener_distancia_segura)
                ruta_larga = max(rutas_con_distancia, key=obtener_distancia_segura)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎯 Ruta más corta:**")
                    st.write(f"**ID:** {ruta_corta.get('id', '-')}")
                    st.write(f"**Origen:** {obtener_nombre_seguro(ruta_corta.get('origen'))}")
                    st.write(f"**Destino:** {obtener_nombre_seguro(ruta_corta.get('destino'))}")
                    st.write(f"**Distancia:** {obtener_distancia_segura(ruta_corta)}")
                    st.write(f"**Algoritmo:** {ruta_corta.get('algoritmo', '-')}")
                    st.write(f"**Camino:** {procesar_camino(ruta_corta.get('camino', []))}")
                
                with col2:
                    st.markdown("**🛣️ Ruta más larga:**")
                    st.write(f"**ID:** {ruta_larga.get('id', '-')}")
                    st.write(f"**Origen:** {obtener_nombre_seguro(ruta_larga.get('origen'))}")
                    st.write(f"**Destino:** {obtener_nombre_seguro(ruta_larga.get('destino'))}")
                    st.write(f"**Distancia:** {obtener_distancia_segura(ruta_larga)}")
                    st.write(f"**Algoritmo:** {ruta_larga.get('algoritmo', '-')}")
                    st.write(f"**Camino:** {procesar_camino(ruta_larga.get('camino', []))}")
                
                # Mostrar detalles completos en expandibles
                with st.expander("Ver detalles completos de ruta más corta"):
                    st.json(ruta_corta, expanded=False)
                
                with st.expander("Ver detalles completos de ruta más larga"):
                    st.json(ruta_larga, expanded=False)
                    
            else:
                st.info("No hay rutas con distancias válidas para comparar.")
        else:
            st.info("No hay rutas extremas para mostrar.")

    # TAB 4: Gráficos y Tiempos
    with tabs[3]:
        st.subheader("Gráficos de Tiempos y Frecuencias")
        
        # Gráfico de tiempos por algoritmo
        if "tiempos_algoritmos" in estadisticas and estadisticas["tiempos_algoritmos"]:
            try:
                tiempos = estadisticas["tiempos_algoritmos"]
                if tiempos:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    algoritmos = list(tiempos.keys())
                    valores = list(tiempos.values())
                    
                    bars = ax.bar(algoritmos, valores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
                    ax.set_ylabel("Tiempo promedio (s)")
                    ax.set_xlabel("Algoritmo")
                    ax.set_title("Tiempos promedio por algoritmo")
                    
                    # Agregar valores en las barras
                    for bar, valor in zip(bars, valores):
                        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                               f'{valor:.3f}s', ha='center', va='bottom')
                    
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.info("No hay datos de tiempos de algoritmos.")
            except Exception as e:
                st.error(f"Error generando gráfico de tiempos: {e}")
        
        # Gráfico de frecuencias de rutas
        if rutas_ordenadas:
            try:
                st.markdown("### 📈 Frecuencias de Rutas")
                
                # Preparar datos de frecuencias
                frecuencias_data = []
                for i, ruta in enumerate(rutas_ordenadas[:10]):  # Top 10 rutas
                    origen = obtener_nombre_seguro(ruta.get('origen'))
                    destino = obtener_nombre_seguro(ruta.get('destino'))
                    frecuencia = ruta.get('frecuencia', 0)
                    ruta_nombre = f"{origen} → {destino}"
                    frecuencias_data.append({"Ruta": ruta_nombre, "Frecuencia": frecuencia})
                
                if frecuencias_data:
                    df_freq = pd.DataFrame(frecuencias_data)
                    
                    # Gráfico de barras horizontales para mejor legibilidad
                    fig, ax = plt.subplots(figsize=(12, 8))
                    y_pos = range(len(df_freq))
                    bars = ax.barh(y_pos, df_freq['Frecuencia'], color='skyblue')
                    
                    ax.set_yticks(y_pos)
                    ax.set_yticklabels(df_freq['Ruta'])
                    ax.set_xlabel('Frecuencia de Uso')
                    ax.set_title('Top 10 Rutas Más Utilizadas')
                    
                    # Agregar valores en las barras
                    for i, (bar, freq) in enumerate(zip(bars, df_freq['Frecuencia'])):
                        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                               str(freq), ha='left', va='center')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Mostrar también como tabla
                    st.dataframe(df_freq, use_container_width=True)
                else:
                    st.info("No hay datos de frecuencias para graficar.")
                    
            except Exception as e:
                st.error(f"Error generando gráfico de frecuencias: {e}")
        
        # Gráfico de distribución por algoritmos
        if rutas_ordenadas:
            try:
                st.markdown("### 🥧 Distribución por Algoritmos")
                
                algoritmos_count = {}
                for ruta in rutas_ordenadas:
                    algoritmo = ruta.get('algoritmo', 'Desconocido')
                    algoritmos_count[algoritmo] = algoritmos_count.get(algoritmo, 0) + 1
                
                if algoritmos_count:
                    fig, ax = plt.subplots(figsize=(8, 8))
                    labels = list(algoritmos_count.keys())
                    sizes = list(algoritmos_count.values())
                    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
                    
                    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                                     colors=colors[:len(labels)], startangle=90)
                    ax.set_title('Distribución de Rutas por Algoritmo')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.info("No hay datos de algoritmos para el gráfico circular.")
                    
            except Exception as e:
                st.error(f"Error generando gráfico de distribución: {e}")
        
        # Información adicional si hay estadísticas de frecuencias
        if "frecuencias" in estadisticas and estadisticas["frecuencias"]:
            try:
                st.markdown("### 📊 Tendencias de Frecuencias")
                st.line_chart(estadisticas["frecuencias"])
            except Exception as e:
                st.error(f"Error mostrando tendencias: {e}")
        
        if not estadisticas and not rutas_ordenadas:
            st.info("No hay datos de tiempos o frecuencias disponibles.")

    # TAB 5: Detalles Avanzados
    with tabs[4]:
        st.subheader("Detalles Avanzados de Rutas")
        
        if rutas_ordenadas:
            # Mostrar resumen general
            st.markdown("### 📊 Resumen General")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Rutas", len(rutas_ordenadas))
            
            with col2:
                algoritmos_unicos = len(set(r.get('algoritmo', 'Desconocido') for r in rutas_ordenadas))
                st.metric("Algoritmos Usados", algoritmos_unicos)
            
            with col3:
                distancia_promedio = sum(r.get('distancia_total', r.get('peso_total', 0)) for r in rutas_ordenadas) / len(rutas_ordenadas) if rutas_ordenadas else 0
                st.metric("Distancia Promedio", f"{distancia_promedio:.2f}")
            
            with col4:
                frecuencia_total = sum(r.get('frecuencia', 0) for r in rutas_ordenadas)
                st.metric("Frecuencia Total", frecuencia_total)
            
            st.markdown("### 🔍 Detalles por Ruta")
            
            # Mostrar cada ruta con información organizada
            for i, ruta in enumerate(rutas_ordenadas):
                origen_nombre = obtener_nombre_seguro(ruta.get('origen'))
                destino_nombre = obtener_nombre_seguro(ruta.get('destino'))
                algoritmo = ruta.get('algoritmo', 'Desconocido')
                frecuencia = ruta.get('frecuencia', 0)
                distancia = ruta.get('distancia_total', ruta.get('peso_total', 0))
                
                with st.expander(f"🔗 Ruta #{i+1}: {origen_nombre} → {destino_nombre} | {algoritmo} | Freq: {frecuencia} | Dist: {distancia}", expanded=False):
                    
                    # Información principal en columnas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Información Básica:**")
                        st.write(f"• **ID Ruta:** {ruta.get('id', 'N/A')}")
                        st.write(f"• **Origen:** {origen_nombre}")
                        st.write(f"• **Destino:** {destino_nombre}")
                        st.write(f"• **Algoritmo:** {algoritmo}")
                        st.write(f"• **Frecuencia:** {frecuencia}")
                        
                    with col2:
                        st.markdown("**Métricas:**")
                        st.write(f"• **Distancia Total:** {distancia}")
                        st.write(f"• **ID Pedido:** {ruta.get('id_pedido', 'N/A')}")
                        st.write(f"• **Tiempo Cálculo:** {ruta.get('tiempo_calculo', 'N/A')}")
                        st.write(f"• **Fecha Creación:** {ruta.get('fecha_creacion', 'N/A')}")
                    
                    # Camino detallado
                    st.markdown("**Camino Recorrido:**")
                    camino_procesado = procesar_camino(ruta.get('camino', []))
                    st.write(camino_procesado)
                    
                    # Datos raw en JSON (colapsado por defecto)
                    with st.expander("Ver datos raw (JSON)", expanded=False):
                        st.json(ruta, expanded=False)
        else:
            st.info("No hay rutas disponibles para mostrar detalles.")
            
        st.caption("Incluye todos los detalles de cada ruta registrada en el sistema.")

    st.caption("Esta sección permite un análisis profundo de las rutas, algoritmos y estadísticas del sistema logístico de drones.")
