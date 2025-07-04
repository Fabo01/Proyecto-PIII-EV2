"""
Interfaz base para mapeadores de dominio a DTOs de respuesta.
Define métodos estándar para mapeo seguro y serialización.
"""
from abc import ABC, abstractmethod

class IMapeadorDominioDTO(ABC):
    @staticmethod
    @abstractmethod
    def a_dto(objeto_dominio, **kwargs):
        """
        Convierte un objeto de dominio a su DTO de respuesta correspondiente.
        Args:
            objeto_dominio: Objeto de entidad de dominio
            **kwargs: Flags opcionales como incluir_pedidos, incluir_cliente, etc.
        Returns:
            DTO serializable para API
        """
        pass

    @staticmethod
    @abstractmethod  
    def a_hashmap(objeto_dominio):
        """
        Convierte un objeto de dominio a dict plano serializable para JSON.
        Args:
            objeto_dominio: Objeto de entidad de dominio
        Returns:
            Dict plano con atributos serializables
        """
        pass

    @staticmethod
    @abstractmethod
    def lista_a_hashmap(lista_objetos):
        """
        Convierte lista de objetos de dominio a lista de dicts planos.
        Args:
            lista_objetos: Lista de objetos de dominio
        Returns:
            Lista de dicts serializables
        """
        pass
