"""
Interfaz para el repositorio de aristas.
"""
from .IRepositorio import IRepositorio
from abc import abstractmethod

class IRepositorioAristas(IRepositorio):
    @abstractmethod
    def agregar(self, arista, clave=None):
        pass

    @abstractmethod
    def obtener(self, clave):
        pass

    @abstractmethod
    def eliminar(self, clave):
        pass

    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass
