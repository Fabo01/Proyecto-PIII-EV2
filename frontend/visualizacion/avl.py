import streamlit as st
import matplotlib.pyplot as plt

def visualizar_avl(rutas):
    """
    Dibuja un gráfico de barras horizontal con las rutas más frecuentes (AVL).
    """
    if not rutas:
        st.info("No hay rutas frecuentes registradas.")
        return
    rutas_str = [' → '.join(str(n) for n in ruta['camino']) for ruta in rutas]
    frecuencias = [ruta.get('frecuencia', 1) for ruta in rutas]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(rutas_str, frecuencias, color='tab:purple')
    ax.set_xlabel('Frecuencia')
    ax.set_title('Rutas más frecuentes (AVL)')
    st.pyplot(fig)
