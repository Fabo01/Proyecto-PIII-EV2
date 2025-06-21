"""
RepositorioClientes: Acceso centralizado y único a instancias de Cliente.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioClientes import IRepositorioClientes

class RepositorioClientes(IRepositorioClientes):
    """
    Repositorio para gestionar instancias únicas de Cliente.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._clientes = HashMap()
        return cls._instancia

    def agregar(self, cliente):
        """
        Agrega una instancia de Cliente al repositorio.

        :param cliente: La instancia de Cliente a agregar.
        """
        self._clientes.insertar(cliente.id_cliente, cliente)

    def obtener(self, id_cliente):
        """
        Obtiene una instancia de Cliente del repositorio.

        :param id_cliente: El ID del cliente a obtener.
        :return: La instancia de Cliente correspondiente al ID, o None si no existe.
        """
        return self._clientes.buscar(id_cliente)

    def eliminar(self, id_cliente):
        """
        Elimina una instancia de Cliente del repositorio.

        :param id_cliente: El ID del cliente a eliminar.
        """
        self._clientes.eliminar(id_cliente)

    def todos(self):
        """
        Obtiene una lista de todas las instancias de Cliente en el repositorio.

        :return: Lista de todas las instancias de Cliente.
        """
        return list(self._clientes.valores())

    def limpiar(self):
        """
        Limpia el repositorio, eliminando todas las instancias de Cliente.
        """
        self._clientes.limpiar()

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de clientes (ID → Objeto Cliente).
        """
        return dict(self._clientes.items())
