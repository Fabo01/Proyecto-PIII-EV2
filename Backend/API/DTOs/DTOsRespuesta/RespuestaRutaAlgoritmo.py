from pydantic import BaseModel
from typing import List

class RespuestaRutaAlgoritmo(BaseModel):
    # Definir campos según uso real
    def __init__(self, **data):
        super().__init__(**data)
        if hasattr(self, 'notificar_observadores'):
            self.notificar_observadores('dto_ruta_algoritmo_serializado', data)
