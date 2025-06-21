"""
RepositorioPedidos: Acceso centralizado y único a instancias de Pedido.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioPedidos import IRepositorioPedidos

class RepositorioPedidos(IRepositorioPedidos):
    """
    Repositorio para gestionar instancias únicas de Pedido.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._pedidos = HashMap()
        return cls._instancia

    def agregar(self, pedido):
        """
        Agrega una nueva instancia de Pedido al repositorio.

        :param pedido: La instancia de Pedido a agregar.
        """
        self._pedidos.insertar(pedido.id_pedido, pedido)

    def obtener(self, id_pedido):
        """
        Obtiene una instancia de Pedido del repositorio.

        :param id_pedido: El identificador de la instancia de Pedido a obtener.
        :return: La instancia de Pedido correspondiente al identificador, o None si no existe.
        """
        return self._pedidos.buscar(id_pedido)

    def eliminar(self, id_pedido):
        """
        Elimina una instancia de Pedido del repositorio.

        :param id_pedido: El identificador de la instancia de Pedido a eliminar.
        """
        self._pedidos.eliminar(id_pedido)

    def todos(self):
        """
        Obtiene una lista de todas las instancias de Pedido en el repositorio.

        :return: Una lista con todas las instancias de Pedido.
        """
        return list(self._pedidos.valores())

    def limpiar(self):
        """
        Limpia el repositorio, eliminando todas las instancias de Pedido.
        """
        self._pedidos.limpiar()

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de pedidos (ID → Objeto Pedido).
        """
        return dict(self._pedidos.items())
