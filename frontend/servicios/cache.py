import streamlit as st
from frontend.servicios.api import api_get
import logging

# --- CACHÉ DE LISTAS DE ENTIDADES (para tablas, selects, etc) ---
@st.cache_data(ttl=10, show_spinner=False)
def cachear_lista(entidad: str):
    """Lista de entidades: vertices, aristas, clientes, almacenamientos, recargas, pedidos, rutas."""
    return api_get(f"/{entidad}")

# --- CACHÉ DE ALGORITMOS Y SNAPSHOTS ---
@st.cache_data(ttl=10, show_spinner=False)
def cachear_algoritmos():
    """Lista de algoritmos de ruta disponibles."""
    return api_get("/simulacion/algoritmos")

@st.cache_data(ttl=10, show_spinner=False)
def cachear_snapshot(tipo: str):
    """Snapshot serializado del grafo (n-1 para MST/Kruskal, m_aristas para grafo completo)."""
    return api_get("/simulacion/snapshot", params={"tipo": tipo})

@st.cache_data(ttl=10, show_spinner=False)
def cachear_estadisticas():
    """Lista de estadísticas generales del sistema."""
    return api_get("/estadisticas/")

# --- FUNCIONES DE ACCESO ESPECÍFICO PARA UI (SOLID, desacopladas) ---

def obtener_clientes_lista():
    return cachear_lista("clientes") or []

def obtener_pedidos_lista():
    return cachear_lista("pedidos") or []

def obtener_almacenamientos_lista():
    return cachear_lista("almacenamientos") or []

def obtener_recargas_lista():
    return cachear_lista("recargas") or []

def obtener_vertices_lista():
    """Lista de vertices (DTOs planos)"""
    return cachear_lista("vertices") or []

def obtener_aristas_lista():
    """Lista de aristas (DTOs planos)"""
    return cachear_lista("aristas") or []

def obtener_rutas_lista():
    """Lista de rutas (DTOs planos)"""
    return cachear_lista("rutas") or []

# Función para limpiar todos los caches de servicio después de cambios de simulación
def limpiar_cache():
    """
    Limpia todos los caches de datos para forzar la recarga de datos del backend.
    """
    import streamlit as st
    st.cache_data.clear()
