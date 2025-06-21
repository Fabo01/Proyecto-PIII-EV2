import requests
import streamlit as st

API_URL = "http://localhost:8000"

def api_get(endpoint, params=None):
    try:
        url = API_URL + endpoint
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al consultar la API: {e}")
        return None

def api_post(endpoint, data=None):
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al enviar datos a {endpoint}: {e}")
        return None
