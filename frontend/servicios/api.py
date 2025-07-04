import requests
from frontend.utils.errores import mostrar_error

API_URL = "http://localhost:8000"

def api_get(endpoint, params=None):
    try:
        url = API_URL + endpoint
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        mostrar_error(e)
        return None

def api_post(endpoint, data=None):
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        mostrar_error(e)
        return None
