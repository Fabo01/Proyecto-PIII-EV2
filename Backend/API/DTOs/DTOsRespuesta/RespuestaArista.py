from pydantic import BaseModel

class RespuestaArista(BaseModel):
    """
    DTO para una arista del grafo.
    """
    id: str
    origen: int
    destino: int
    peso: float
    tipo: str = "arista"
