import streamlit as st
from frontend.servicios.api import api_get

def ui_clientes():
    """
    Pestaña 3: Visualización de clientes, pedidos y hashmaps de entidades.
    Cumple con modularidad, robustez y nombres en español.
    """
    st.header("Clientes y Pedidos")
    clientes = api_get("/clientes/hashmap") or {}
    pedidos = api_get("/pedidos/hashmap") or {}
    st.subheader("HashMap de Clientes (ID → Objeto)")
    st.json(clientes)
    st.subheader("HashMap de Pedidos (ID → Objeto)")
    st.json(pedidos)
    # Visualización de todos los hashmaps existentes
    st.subheader("HashMap de Almacenamientos (ID → Objeto)")
    almacenamientos = api_get("/almacenamientos/hashmap") or {}
    st.json(almacenamientos)
    st.subheader("HashMap de Recargas (ID → Objeto)")
    recargas = api_get("/recargas/hashmap") or {}
    st.json(recargas)
    st.subheader("HashMap de Vértices (ID → Objeto)")
    vertices = api_get("/vertices/hashmap") or {}
    st.json(vertices)
    st.subheader("HashMap de Aristas (Clave → Objeto)")
    aristas = api_get("/aristas/hashmap") or {}
    st.json(aristas)
    st.subheader("HashMap de Rutas (Clave → Objeto)")
    rutas = api_get("/rutas/hashmap") or {}
    st.json(rutas)
