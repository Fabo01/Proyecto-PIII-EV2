from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .RespuestaCliente import RespuestaCliente
    from .RespuestaRuta import RespuestaRuta
    from .RespuestaVertice import RespuestaVertice

class RespuestaPedido(BaseModel):
    """
    DTO de Pedido para respuesta API.
    Referencia a cliente como objeto completo (no solo ID), usando anotaciones de cadena.
    Origen y destino pueden ser vertices de cualquier tipo.
    """
    id_pedido: int
    cliente: Optional["RespuestaCliente"] = None
    prioridad: str
    status: str
    ruta: Optional["RespuestaRuta"] = None
    peso_total: Optional[float] = None
    origen: Optional["RespuestaVertice"] = None
    destino: Optional["RespuestaVertice"] = None
    fecha_creacion: Optional[str] = None
    fecha_entrega: Optional[str] = None
