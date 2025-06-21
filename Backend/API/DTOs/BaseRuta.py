from pydantic import BaseModel
from typing import List

class BaseRuta(BaseModel):
    origen: int
    destino: int
    camino: List[int]
    peso_total: float
    algoritmo: str
