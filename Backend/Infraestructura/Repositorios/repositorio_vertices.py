"""
RepositorioVertices: Acceso centralizado y único a instancias de Vertice.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Infraestructura.Repositorios.RepoInterfaces.IRepositorioVertices import IRepositorioVertices

class RepositorioVertices(IRepositorioVertices):
    """
    Repositorio para gestionar instancias únicas de Vertice.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._vertices = HashMap()
        return cls._instancia

    def agregar(self, vertice, id_elemento):
        """
        Agrega un vértice al repositorio.

        :param vertice: La instancia del vértice a agregar.
        :param id_elemento: El identificador único del elemento.
        """
        self._vertices.insertar(id_elemento, vertice)

    def obtener(self, id_elemento):
        """
        Obtiene un vértice del repositorio.

        :param id_elemento: El identificador único del elemento a obtener.
        :return: La instancia del vértice correspondiente al identificador,
                 o None si no existe.
        """
        return self._vertices.buscar(id_elemento)

    def eliminar(self, id_elemento):
        """
        Elimina un vértice del repositorio.

        :param id_elemento: El identificador único del elemento a eliminar.
        """
        self._vertices.eliminar(id_elemento)

    def todos(self):
        """
        Obtiene una lista de todos los vértices en el repositorio.

        :return: Lista de instancias de vértices.
        """
        return list(self._vertices.valores())

    def limpiar(self):
        """
        Limpia el repositorio, eliminando todos los vértices.
        """
        self._vertices.limpiar()

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de vértices (ID → Objeto Vertice).
        """
        return dict(self._vertices.items())
