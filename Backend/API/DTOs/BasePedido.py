from pydantic import BaseModel
from typing import List, Optional

class BasePedido(BaseModel):
    id_pedido: int
    id_cliente: int
    id_almacenamiento: int
    prioridad: str
    status: str
    ruta: Optional[List[int]] = None
    peso_total: Optional[float] = None
