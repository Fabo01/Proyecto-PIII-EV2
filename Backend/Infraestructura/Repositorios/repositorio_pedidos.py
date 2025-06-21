"""
RepositorioPedidos: Acceso centralizado y unico a instancias de Pedido.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioPedidos import IRepositorioPedidos

class RepositorioPedidos(IRepositorioPedidos):
    """
    Repositorio para gestionar instancias unicas de Pedido.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._pedidos = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_pedidos_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, pedido):
        """
        Agrega una nueva instancia de Pedido al repositorio.
        :param pedido: Instancia de Pedido a agregar.
        """
        self._pedidos.insertar(pedido.id_pedido, pedido)
        self.notificar_observadores('repositorio_pedidos_agregado', {'pedido': pedido})

    def obtener(self, id_pedido):
        """
        Obtiene una instancia de Pedido por su ID.
        :param id_pedido: Identificador unico del pedido.
        :return: Instancia de Pedido o None si no existe.
        """
        pedido = self._pedidos.buscar(id_pedido)
        self.notificar_observadores('repositorio_pedidos_obtenido', {'id': id_pedido, 'pedido': pedido})
        return pedido

    def eliminar(self, id_pedido):
        """
        Elimina una instancia de Pedido por su ID.
        :param id_pedido: Identificador unico del pedido.
        """
        self._pedidos.eliminar(id_pedido)
        self.notificar_observadores('repositorio_pedidos_eliminado', {'id': id_pedido})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Pedido.
        :return: Lista de instancias de Pedido.
        """
        pedidos = list(self._pedidos.valores())
        self.notificar_observadores('repositorio_pedidos_todos', {'cantidad': len(pedidos)})
        return pedidos

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Pedido.
        """
        self._pedidos = HashMap()
        self.notificar_observadores('repositorio_pedidos_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de pedidos (ID → Objeto Pedido) como dict.
        :return: Diccionario de pedidos.
        """
        self.notificar_observadores('repositorio_pedidos_hashmap', None)
        return dict(self._pedidos.items())
