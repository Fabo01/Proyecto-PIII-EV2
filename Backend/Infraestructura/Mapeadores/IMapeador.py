"""
IMapeador: interfaz común para todos los mapeadores de DTOs.
Define el método esencial a_dto para mapear entidad de dominio a DTO.
"""
from abc import ABC, abstractmethod
from typing import Any

class IMapeador(ABC):
    @abstractmethod
    def a_dto(self, entidad: Any) -> Any:
        """
        Convierte una entidad de dominio en su DTO de respuesta.
        """
        pass
