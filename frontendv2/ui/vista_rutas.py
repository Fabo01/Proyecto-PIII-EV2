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
        tabla = [
            {
                "ID": r.get("id"),
                "Origen": r.get("origen", {}).get("nombre", r.get("origen")),
                "Destino": r.get("destino", {}).get("nombre", r.get("destino")),
                "Frecuencia": r.get("frecuencia", "-"),
                "Distancia total": r.get("distancia_total", r.get("peso_total", "-")),
                "Camino": " -> ".join([v.get("nombre", str(v.get("id"))) for v in r.get("camino", [])])
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
            ruta_corta = min(rutas_ordenadas, key=lambda r: r.get('distancia_total', float('inf')))
            ruta_larga = max(rutas_ordenadas, key=lambda r: r.get('distancia_total', float('-inf')))
            st.markdown("**Ruta más corta:**")
            st.json(ruta_corta)
            st.markdown("**Ruta más larga:**")
            st.json(ruta_larga)
        else:
            st.info("No hay rutas extremas para mostrar.")

    # TAB 4: Gráficos y Tiempos
    with tabs[3]:
        st.subheader("Gráficos de Tiempos y Frecuencias")
        if "tiempos_algoritmos" in estadisticas:
            tiempos = estadisticas["tiempos_algoritmos"]
            fig, ax = plt.subplots()
            ax.bar(tiempos.keys(), tiempos.values())
            ax.set_ylabel("Tiempo promedio (s)")
            ax.set_xlabel("Algoritmo")
            ax.set_title("Tiempos promedio por algoritmo")
            st.pyplot(fig)
        if "frecuencias" in estadisticas:
            st.line_chart(estadisticas["frecuencias"])
        else:
            st.info("No hay datos de tiempos o frecuencias.")

    # TAB 5: Detalles Avanzados
    with tabs[4]:
        st.subheader("Detalles Avanzados de Rutas")
        for ruta in rutas_ordenadas:
            with st.expander(f"Ruta {ruta.get('id')} | Frecuencia: {ruta.get('frecuencia', '-')}, Algoritmo: {ruta.get('algoritmo', '-')}", expanded=False):
                st.json(ruta, expanded=False)
        st.caption("Incluye todos los detalles de cada ruta registrada en el sistema.")

    st.caption("Esta sección permite un análisis profundo de las rutas, algoritmos y estadísticas del sistema logístico de drones.")
