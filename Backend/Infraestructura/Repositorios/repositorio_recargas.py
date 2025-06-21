"""
RepositorioRecargas: Acceso centralizado y único a instancias de Recarga.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioRecargas import IRepositorioRecargas

class RepositorioRecargas(IRepositorioRecargas):
    """
    Repositorio para gestionar instancias únicas de Recarga.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._recargas = HashMap()
        return cls._instancia

    def agregar(self, recarga):
        """
        Agrega una nueva recarga al repositorio.

        :param recarga: La recarga a agregar.
        """
        self._recargas.insertar(recarga.id_recarga, recarga)

    def obtener(self, id_recarga):
        """
        Obtiene una recarga del repositorio por su ID.

        :param id_recarga: El ID de la recarga a obtener.
        :return: La recarga correspondiente al ID, o None si no existe.
        """
        return self._recargas.buscar(id_recarga)

    def eliminar(self, id_recarga):
        """
        Elimina una recarga del repositorio por su ID.

        :param id_recarga: El ID de la recarga a eliminar.
        """
        self._recargas.eliminar(id_recarga)

    def todos(self):
        """
        Obtiene una lista de todas las recargas en el repositorio.

        :return: Lista de todas las recargas.
        """
        return list(self._recargas.valores())

    def limpiar(self):
        """
        Limpia el repositorio, eliminando todas las recargas.
        """
        self._recargas.limpiar()

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de recargas (ID → Objeto Recarga).
        """
        return dict(self._recargas.items())
