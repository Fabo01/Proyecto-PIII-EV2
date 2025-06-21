"""
Interfaz para el repositorio de almacenamientos.
"""
from .IRepositorio import IRepositorio
from abc import abstractmethod

class IRepositorioAlmacenamientos(IRepositorio):
    @abstractmethod
    def agregar(self, almacen):
        pass

    @abstractmethod
    def obtener(self, id_almacenamiento):
        pass

    @abstractmethod
    def eliminar(self, id_almacenamiento):
        pass

    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass
