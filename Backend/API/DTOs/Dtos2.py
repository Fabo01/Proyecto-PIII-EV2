from pydantic import BaseModel
from typing import List, Optional

class NodoBase(BaseModel):
    id: int
    tipo: str
    nombre: str

class PedidoBase(BaseModel):
    id_pedido: int
    id_cliente: int
    id_almacenamiento: int
    prioridad: str
    status: str
    ruta: Optional[List[int]] = None
    peso_total: Optional[float] = None

class RutaBase(BaseModel):
    origen: int
    destino: int
    camino: List[int]
    peso_total: float
    algoritmo: str

class SimulacionConfig(BaseModel):
    n_nodos: int
    m_aristas: int
    n_pedidos: int

class AristaBase(BaseModel):
    origen: int
    destino: int
    peso: float
