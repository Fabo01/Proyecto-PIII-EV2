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

def despachar_pestana(nombre):
    """
    Despacha la función de UI correspondiente a la pestaña seleccionada.
    Permite fácil extensión y escalabilidad.
    """
    if nombre == "Configuración de la Simulación":
        ui_simulacion()
    elif nombre == "Explorar Red":
        ui_red()
    elif nombre == "Clientes y Pedidos":
        ui_clientes()
    elif nombre == "Análisis de Rutas":
        ui_rutas()
    elif nombre == "Estadísticas Generales":
        ui_estadisticas()
    else:
        st.warning(f"Pestaña no implementada: {nombre}")

try:
    despachar_pestana(pestana)
except Exception as e:
    mostrar_error(e)
