from __future__ import annotations
from typing import List, Optional, Dict, Any
from .RespuestaVertice import RespuestaVertice

class RespuestaAlmacenamiento(RespuestaVertice):
    """
    DTO de Almacenamiento para respuesta API.
    Incluye lista de pedidos como dicts planos serializables, nunca objetos de dominio ni referencias circulares.
    """
    pedidos: Optional[List[int]] = None

    class Config:
        from_attributes = True
