import streamlit as st
from frontend.ui.simulacion import ui_simulacion
from frontend.ui.red import ui_red
from frontend.ui.clientes import ui_clientes
from frontend.ui.rutas import ui_rutas
from frontend.ui.estadisticas import ui_estadisticas
from frontend.utils.errores import mostrar_error

st.set_page_config(page_title="Simulación Drones Correos Chile", layout="wide")
st.title("Simulación Logística de Drones - Correos Chile")

PESTANAS = [
    "Configuración de la Simulación",
    "Explorar Red",
    "Clientes y Pedidos",
    "Análisis de Rutas",
    "Estadísticas Generales"
]

pestana = st.sidebar.radio("Selecciona una pestaña", PESTANAS, key="pestana")

try:
    if pestana == "Configuración de la Simulación":
        ui_simulacion()
    elif pestana == "Explorar Red":
        ui_red()
    elif pestana == "Clientes y Pedidos":
        ui_clientes()
    elif pestana == "Análisis de Rutas":
        ui_rutas()
    elif pestana == "Estadísticas Generales":
        ui_estadisticas()
except Exception as e:
    mostrar_error(e)
