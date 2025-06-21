from typing import List, Optional
from pydantic import BaseModel
from .RespuestaVertice import RespuestaVertice

class RespuestaRuta(BaseModel):
    """
    DTO de Ruta para respuesta API.
    Origen y destino son vertices (Cliente, Almacenamiento o Recarga).
    Camino es una lista de vertices.
    """
    origen: RespuestaVertice
    destino: RespuestaVertice
    camino: List[RespuestaVertice]
    peso_total: float
    algoritmo: str
    tiempo_calculo: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('dto_ruta_serializado', {'origen': self.origen, 'destino': self.destino, 'camino': self.camino, 'peso_total': self.peso_total, 'algoritmo': self.algoritmo, 'tiempo_calculo': self.tiempo_calculo})
