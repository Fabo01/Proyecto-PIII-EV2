from __future__ import annotations
from typing import List, Optional, Dict, Any
from .RespuestaVertice import RespuestaVertice

class RespuestaCliente(RespuestaVertice):
    """
    DTO de Cliente para respuesta API.
    Incluye lista de pedidos como dicts planos serializables, nunca objetos de dominio ni referencias circulares.
    """
    pedidos: Optional[List[int]] = None
