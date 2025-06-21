"""
Interfaz para el repositorio de recargas.
"""
from .IRepositorio import IRepositorio
from abc import abstractmethod

class IRepositorioRecargas(IRepositorio):
    @abstractmethod
    def agregar(self, recarga):
        pass

    @abstractmethod
    def obtener(self, id_recarga):
        pass

    @abstractmethod
    def eliminar(self, id_recarga):
        pass

    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass
