"""
Módulo de servicios para consumo de la API desde el nuevo frontend modular.
Incluye funciones para obtener datos DTO y HashMap según la vista.
"""

import requests

API_URL = "http://localhost:8000"  # Ajustar si es necesario

# --- DTOs ---
def obtener_clientes_dto():
    resp = requests.get(f"{API_URL}/clientes/")
    return resp.json() if resp.status_code == 200 else []

def obtener_pedidos_dto():
    resp = requests.get(f"{API_URL}/pedidos/")
    return resp.json() if resp.status_code == 200 else []

def obtener_almacenamientos_dto():
    resp = requests.get(f"{API_URL}/almacenamientos/")
    return resp.json() if resp.status_code == 200 else []

def obtener_recargas_dto():
    resp = requests.get(f"{API_URL}/recargas/")
    return resp.json() if resp.status_code == 200 else []

def obtener_vertices_dto():
    resp = requests.get(f"{API_URL}/vertices/")
    return resp.json() if resp.status_code == 200 else []

def obtener_aristas_dto():
    resp = requests.get(f"{API_URL}/aristas/")
    return resp.json() if resp.status_code == 200 else []

def obtener_rutas_dto():
    resp = requests.get(f"{API_URL}/rutas/")
    return resp.json() if resp.status_code == 200 else []

def obtener_estadisticas_dto():
    resp = requests.get(f"{API_URL}/estadisticas/")
    return resp.json() if resp.status_code == 200 else {}

# --- HashMap (debug) ---
def obtener_clientes_hashmap():
    resp = requests.get(f"{API_URL}/clientes/hashmap/")
    return resp.json() if resp.status_code == 200 else {}

def obtener_pedidos_hashmap():
    resp = requests.get(f"{API_URL}/pedidos/hashmap/")
    return resp.json() if resp.status_code == 200 else {}

def obtener_almacenamientos_hashmap():
    resp = requests.get(f"{API_URL}/almacenamientos/hashmap/")
    return resp.json() if resp.status_code == 200 else {}

def obtener_recargas_hashmap():
    resp = requests.get(f"{API_URL}/recargas/hashmap/")
    return resp.json() if resp.status_code == 200 else {}

def obtener_vertices_hashmap():
    resp = requests.get(f"{API_URL}/vertices/hashmap/")
    return resp.json() if resp.status_code == 200 else {}

def obtener_aristas_hashmap():
    resp = requests.get(f"{API_URL}/aristas/hashmap/")
    return resp.json() if resp.status_code == 200 else {}

def obtener_rutas_hashmap():
    resp = requests.get(f"{API_URL}/rutas/hashmap/")
    return resp.json() if resp.status_code == 200 else {}
