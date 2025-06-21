import streamlit as st
from frontend.servicios.api import api_get

@st.cache_data(ttl=10, show_spinner=False)
def cachear_estado_simulacion():
    return api_get("/simulacion/estado")
