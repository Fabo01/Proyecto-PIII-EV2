import requests

API_URL = "http://localhost:8000"

def iniciar_simulacion(n_vertices, m_aristas, n_pedidos):
    resp = requests.post(f"{API_URL}/simulacion/iniciar", json={
        "n_vertices": n_vertices,
        "m_aristas": m_aristas,
        "n_pedidos": n_pedidos
    })
    return resp.json()

def calcular_ruta(id_pedido: int, algoritmo: str):
    resp = requests.post(f"{API_URL}/rutas/calcular/{id_pedido}/{algoritmo}")
    resp.raise_for_status()
    return resp.json()

def calcular_rutas_todos(id_pedido: int):
    resp = requests.post(f"{API_URL}/rutas/calcular/{id_pedido}/todos")
    resp.raise_for_status()
    return resp.json()

def calcular_rutas_algoritmos():
    resp = requests.post(f"{API_URL}/rutas/calcular/masivo/todos")
    resp.raise_for_status()
    return resp.json()

def floydwarshall_para_todos_los_pedidos():
    resp = requests.post(f"{API_URL}/rutas/floydwarshall_pedidos")
    resp.raise_for_status()
    return resp.json()

def entregar_pedido(id_pedido: int):
    resp = requests.post(f"{API_URL}/rutas/entregar/{id_pedido}")
    resp.raise_for_status()
    return resp.json()

def rutas_por_pedido(id_pedido: int):
    resp = requests.get(f"{API_URL}/rutas/por_pedido/{id_pedido}")
    resp.raise_for_status()
    return resp.json()

def rutas_por_algoritmo(algoritmo: str):
    resp = requests.get(f"{API_URL}/rutas/por_algoritmo/{algoritmo}")
    resp.raise_for_status()
    return resp.json()

def obtener_info_simulacion():
    resp = requests.get(f"{API_URL}/simulacion/info")
    return resp.json() if resp.ok else None

def obtener_clientes_dto():
    resp = requests.get(f"{API_URL}/clientes/")
    return resp.json() if resp.ok else []

def obtener_pedidos_dto():
    resp = requests.get(f"{API_URL}/pedidos/")
    return resp.json() if resp.ok else []

def obtener_almacenamientos_dto():
    resp = requests.get(f"{API_URL}/almacenamientos/")
    return resp.json() if resp.ok else []

def obtener_recargas_dto():
    resp = requests.get(f"{API_URL}/recargas/")
    return resp.json() if resp.ok else []

def obtener_vertices_dto():
    resp = requests.get(f"{API_URL}/vertices/")
    return resp.json() if resp.ok else []

def obtener_aristas_dto():
    resp = requests.get(f"{API_URL}/aristas/")
    return resp.json() if resp.ok else []

def obtener_rutas_dto():
    resp = requests.get(f"{API_URL}/rutas/")
    return resp.json() if resp.ok else []

def obtener_estadisticas_dto():
    resp = requests.get(f"{API_URL}/estadisticas/")
    return resp.json() if resp.ok else None

def obtener_snapshot(tipo: str = 'todo'):
    """
    Obtiene un snapshot completo de la simulación desde el backend.
    """
    resp = requests.get(f"{API_URL}/simulacion/snapshot", params={'tipo': tipo})
    return resp.json() if resp.ok else {}

def calcular_mst_kruskal():
    """
    Calcula el Árbol de Expansión Mínima (MST) usando el algoritmo de Kruskal.
    Retorna las aristas del MST y el peso total.
    """
    resp = requests.get(f"{API_URL}/rutas/mst/kruskal")
    resp.raise_for_status()
    return resp.json()