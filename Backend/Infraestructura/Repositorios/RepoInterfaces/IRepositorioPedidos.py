"""
Interfaz para el repositorio de pedidos.
"""
from .IRepositorio import IRepositorio
from abc import abstractmethod

class IRepositorioPedidos(IRepositorio):
    @abstractmethod
    def agregar(self, pedido):
        pass

    @abstractmethod
    def obtener(self, id_pedido):
        pass

    @abstractmethod
    def eliminar(self, id_pedido):
        pass

    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass
