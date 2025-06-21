from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .RespuestaCliente import RespuestaCliente
    from .RespuestaAlmacenamiento import RespuestaAlmacenamiento
    from .RespuestaRecarga import RespuestaRecarga
    from .RespuestaPedido import RespuestaPedido
    from .RespuestaRuta import RespuestaRuta

class RespuestaSimulacionEstado(BaseModel):
    """
    DTO de estado de simulación para respuesta API.
    Incluye listas completas de clientes, almacenamientos, recargas, pedidos y rutas como objetos DTO anidados.
    Se usan anotaciones de cadena para evitar ciclos de importación.
    """
    clientes: List["RespuestaCliente"]
    almacenamientos: List["RespuestaAlmacenamiento"]
    recargas: List["RespuestaRecarga"]
    pedidos: List["RespuestaPedido"]
    rutas: List["RespuestaRuta"]
    estado: str
    mensaje: Optional[str] = None

    class Config:
        from_attributes = True

