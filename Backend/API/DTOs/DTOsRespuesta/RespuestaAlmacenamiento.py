from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
from .RespuestaVertice import RespuestaVertice

if TYPE_CHECKING:
    from .RespuestaPedido import RespuestaPedido

class RespuestaAlmacenamiento(RespuestaVertice):
    """
    DTO de Almacenamiento para respuesta API.
    Incluye lista de pedidos como objetos completos (RespuestaPedido), no solo IDs.
    Se usa anotación de cadena para evitar ciclos de importación.
    """
    pedidos: Optional[List["RespuestaPedido"]] = None

    class Config:
        from_attributes = True
