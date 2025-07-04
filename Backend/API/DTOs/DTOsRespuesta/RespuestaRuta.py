from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class RespuestaRuta(BaseModel):
    id_ruta: str
    id_pedido: Optional[int] = None
    origen: Optional[Dict[str, Any]] = None  # {"id": int, "nombre": str, "tipo": str}
    destino: Optional[Dict[str, Any]] = None  # {"id": int, "nombre": str, "tipo": str}
    aristas_ids: List[str] = []  # IDs de aristas recorridas (formato "ori-dest")
    camino: List[int] = []  # Secuencia de IDs de vértices en el camino
    peso_total: Optional[float] = None
    algoritmo: Optional[str] = None
    tiempo_calculo: float = 0.0
    fecha_creacion: str = ""

class RespuestaMultiplesRutas(BaseModel):
    id_pedido: int
    resultados: Dict[str, RespuestaRuta]  # {algoritmo: RespuestaRuta}
    tiempo_total: float
