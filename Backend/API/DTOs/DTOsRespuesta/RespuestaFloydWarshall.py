from pydantic import BaseModel
from typing import Dict, List

class RespuestaFloydWarshall(BaseModel):
    distancias: Dict[int, Dict[int, float]]
    caminos: Dict[int, Dict[int, List[int]]]
    mensaje: str = ''
