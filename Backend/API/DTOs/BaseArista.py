from pydantic import BaseModel

class BaseArista(BaseModel):
    origen: int
    destino: int
    peso: float
