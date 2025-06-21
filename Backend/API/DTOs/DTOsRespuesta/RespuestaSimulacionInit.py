from pydantic import BaseModel
from typing import List

class RespuestaSimulacionInit(BaseModel):
    n_vertices: int
    m_aristas: int
    n_pedidos: int
