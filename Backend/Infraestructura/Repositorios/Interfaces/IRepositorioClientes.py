"""
Interfaz para el repositorio de clientes.
"""
from .IRepositorio import IRepositorio
from abc import abstractmethod

class IRepositorioClientes(IRepositorio):
    @abstractmethod
    def agregar(self, cliente):
        pass

    @abstractmethod
    def obtener(self, id_cliente):
        pass

    @abstractmethod
    def eliminar(self, id_cliente):
        pass

    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass
