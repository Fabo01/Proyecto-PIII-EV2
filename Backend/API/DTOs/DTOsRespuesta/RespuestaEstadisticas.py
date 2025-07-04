from pydantic import BaseModel
from typing import Dict, Any

from typing import List, Dict, Any

class RespuestaEstadisticas(BaseModel):
    rutas_mas_frecuentes: List[Dict[str, Any]]
    vertices_mas_visitados: Dict[str, int]
    pedidos_por_estado: Dict[str, int]
    pedidos_por_cliente: Dict[str, int]
    vertices_por_tipo: Dict[str, int]
    # Totales por categoría
    total_clientes: int
    total_almacenamientos: int
    total_recargas: int
    total_vertices: int
    total_aristas: int
    total_pedidos: int
    # Tiempo de respuesta de la consulta (en segundos)
    tiempo_respuesta: float
    # Estadísticas adicionales
    total_rutas_unicas: int
    promedio_pedidos_por_cliente: float
