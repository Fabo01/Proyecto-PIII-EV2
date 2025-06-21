import streamlit as st
import traceback

def mostrar_error(e):
    st.error(f"Ocurrió un error: {e}")
    st.text(traceback.format_exc())
