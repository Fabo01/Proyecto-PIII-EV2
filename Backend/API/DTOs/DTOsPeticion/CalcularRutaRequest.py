from pydantic import BaseModel
from typing import Optional

class CalcularRutaRequest(BaseModel):
    """
    DTO de petición para calcular ruta de un pedido.
    id_pedido: Identificador del pedido a procesar.
    algoritmo: Algoritmo de cálculo ('bfs', 'dfs', 'dijkstra', etc.) o 'todos' para ejecutar todos.
    """
    id_pedido: int
    algoritmo: Optional[str] = "bfs"
