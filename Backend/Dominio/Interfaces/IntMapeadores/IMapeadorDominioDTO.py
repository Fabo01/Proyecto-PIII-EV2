"""
Interfaz base para mapeadores de dominio a DTOs de respuesta.
"""
from abc import ABC, abstractmethod

class IMapeadorDominioDTO(ABC):
    @staticmethod
    @abstractmethod
    def a_dto(objeto_dominio):
        """
        Convierte un objeto de dominio a su DTO de respuesta correspondiente.
        """
        pass
