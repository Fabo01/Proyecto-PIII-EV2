from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Dict, Any

class RespuestaPedido(BaseModel):
    """
    DTO de Pedido para respuesta API.
    Todos los campos que referencian a otros objetos (cliente, origen, destino, ruta) deben ser dicts planos serializables o None.
    """
    id_pedido: int
    cliente: str 
    prioridad: str
    status: str
    ruta: Optional[Dict[str, Any]] = None
    peso_total: Optional[float] = None
    origen: int 
    destino: int 
    fecha_creacion: Optional[str] = None
    fecha_entrega: Optional[str] = None
