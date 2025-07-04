import streamlit as st
from frontendv2.ui.menu import mostrar_menu
from frontendv2.servicios.cache import inicializar_snapshot_datos, limpiar_cache_y_snapshot
from frontendv2.servicios.api import obtener_info_simulacion

def main():
    st.set_page_config(page_title="Simulación Logística Drones", layout="wide")
    # Inicializar o limpiar snapshot según estado de simulación
    mostrar_menu()

if __name__ == "__main__":
    main()