"""
Interfaz base para todos los repositorios de acceso centralizado a entidades.
Define los métodos estándar para acceso, inserción, eliminación y limpieza.
"""
from abc import ABC, abstractmethod

class IRepositorio(ABC):
    @abstractmethod
    def agregar(self, entidad):
        """Agrega una entidad al repositorio."""
        pass

    @abstractmethod
    def obtener(self, id_entidad):
        """Obtiene una entidad por su identificador."""
        pass

    @abstractmethod
    def eliminar(self, id_entidad):
        """Elimina una entidad por su identificador."""
        pass

    @abstractmethod
    def todos(self):
        """Retorna una lista de todas las entidades almacenadas."""
        pass

    @abstractmethod
    def limpiar(self):
        """Elimina todas las entidades del repositorio."""
        pass
