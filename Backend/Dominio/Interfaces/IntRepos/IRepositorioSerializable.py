"""
Interfaz extendida para repositorios con capacidades de serialización.
Extiende IRepositorio agregando métodos para obtener datos serializables.
"""
from abc import ABC, abstractmethod
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio

class IRepositorioSerializable(IRepositorio):
    @abstractmethod
    def obtener_todos_serializables(self):
        """
        Retorna todos los objetos del repositorio serializados como dict plano.
        Returns:
            Dict con objetos serializados listos para API
        """
        pass

    @abstractmethod
    def obtener_por_tipo(self, tipo_elemento):
        """
        Obtiene objetos filtrados por tipo de elemento.
        Args:
            tipo_elemento: Tipo a filtrar ('cliente', 'almacenamiento', 'recarga')
        Returns:
            Lista de objetos del tipo especificado
        """
        pass

    @abstractmethod
    def serializar_relaciones(self):
        """
        Retorna mapeo de relaciones entre objetos para frontend.
        Returns:
            Dict con estructura de relaciones serializadas
        """
        pass
