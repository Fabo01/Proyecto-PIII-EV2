from pydantic import BaseModel
from typing import List

class BaseVertice(BaseModel):
    id: int
    tipo: str
    nombre: str
