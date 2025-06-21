from pydantic import BaseModel
from typing import List
import logging

class RespuestaRutaAlgoritmo(BaseModel):
    # Definir campos según uso real
    def __init__(self, **data):
        super().__init__(**data)
        logger = logging.getLogger("DTO.RutaAlgoritmo")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[RespuestaRutaAlgoritmo] Creada: {data}")
