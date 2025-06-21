from typing import List, Optional
from pydantic import BaseModel
from .RespuestaVertice import RespuestaVertice
import logging

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
        logger = logging.getLogger("DTO.Ruta")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[RespuestaRuta] Creada: origen={self.origen}, destino={self.destino}, camino={self.camino}, peso_total={self.peso_total}, algoritmo={self.algoritmo}, tiempo_calculo={self.tiempo_calculo}")
