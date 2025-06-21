from pydantic import BaseModel

class BaseSimulacionConfig(BaseModel):
    n_vertices: int
    m_aristas: int
    n_pedidos: int
