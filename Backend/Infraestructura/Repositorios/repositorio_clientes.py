"""
RepositorioClientes: Acceso centralizado y unico a instancias de Cliente.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioClientes import IRepositorioClientes

class RepositorioClientes(IRepositorioClientes):
    """
    Repositorio para gestionar instancias unicas de Cliente.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._clientes = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_clientes_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, cliente):
        """
        Agrega una nueva instancia de Cliente al repositorio.
        :param cliente: Instancia de Cliente a agregar.
        """
        self._clientes.insertar(cliente.id_cliente, cliente)
        self.notificar_observadores('repositorio_clientes_agregado', {'cliente': cliente})

    def obtener(self, id_cliente):
        """
        Obtiene una instancia de Cliente por su ID.
        :param id_cliente: Identificador unico del cliente.
        :return: Instancia de Cliente o None si no existe.
        """
        cliente = self._clientes.buscar(id_cliente)
        self.notificar_observadores('repositorio_clientes_obtenido', {'id': id_cliente, 'cliente': cliente})
        return cliente

    def eliminar(self, id_cliente):
        """
        Elimina una instancia de Cliente por su ID.
        :param id_cliente: Identificador unico del cliente.
        """
        self._clientes.eliminar(id_cliente)
        self.notificar_observadores('repositorio_clientes_eliminado', {'id': id_cliente})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Cliente.
        :return: Lista de instancias de Cliente.
        """
        clientes = list(self._clientes.valores())
        self.notificar_observadores('repositorio_clientes_todos', {'cantidad': len(clientes)})
        return clientes

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Cliente.
        """
        self._clientes = HashMap()
        self.notificar_observadores('repositorio_clientes_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de clientes (ID → Objeto Cliente) como dict.
        :return: Diccionario de clientes.
        """
        self.notificar_observadores('repositorio_clientes_hashmap', None)
        return dict(self._clientes.items())
