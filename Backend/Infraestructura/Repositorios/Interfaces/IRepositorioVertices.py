"""
Interfaz para el repositorio de vértices.
"""
from .IRepositorio import IRepositorio
from abc import abstractmethod

class IRepositorioVertices(IRepositorio):
    @abstractmethod
    def agregar(self, vertice, id_elemento):
        pass

    @abstractmethod
    def obtener(self, id_elemento):
        pass

    @abstractmethod
    def eliminar(self, id_elemento):
        pass

    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass
