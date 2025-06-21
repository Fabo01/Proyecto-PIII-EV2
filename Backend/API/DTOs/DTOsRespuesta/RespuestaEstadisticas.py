from pydantic import BaseModel
from typing import Dict, Any

class RespuestaEstadisticas(BaseModel):
    rutas_mas_frecuentes: Dict[str, int]
    vertices_mas_visitados: Dict[str, int]
    tiempo_respuesta: float
