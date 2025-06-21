from __future__ import annotations
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .RespuestaVertice import RespuestaVertice

class RespuestaVertice(BaseModel):
    """
    DTO base para vertices (Cliente, Almacenamiento, Recarga).
    Se utiliza como base para herencia y referencia en otros DTOs.
    """
    id: int
    tipo: str
    nombre: str
