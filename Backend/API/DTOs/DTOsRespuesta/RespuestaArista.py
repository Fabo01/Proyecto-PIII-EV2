from pydantic import BaseModel

class RespuestaArista(BaseModel):
    """
    DTO para una arista del grafo.
    """
    origen: int
    destino: int
    peso: float
