"""
RepositorioAlmacenamientos: Acceso centralizado y único a instancias de Almacenamiento.
Utiliza HashMap para acceso O(1) y garantiza instanciación única.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Infraestructura.Repositorios.RepoInterfaces.IRepositorioAlmacenamientos import IRepositorioAlmacenamientos

class RepositorioAlmacenamientos(IRepositorioAlmacenamientos):
    """
    Repositorio para gestionar instancias únicas de Almacenamiento.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._almacenamientos = HashMap()
        return cls._instancia

    def agregar(self, almacen):
        """
        Agrega una nueva instancia de almacenamiento al repositorio.

        :param almacen: La instancia de almacenamiento a agregar.
        """
        self._almacenamientos.insertar(almacen.id_almacenamiento, almacen)

    def obtener(self, id_almacenamiento):
        """
        Obtiene una instancia de almacenamiento del repositorio.

        :param id_almacenamiento: El ID de la instancia de almacenamiento a obtener.
        :return: La instancia de almacenamiento correspondiente al ID dado, o None si no existe.
        """
        return self._almacenamientos.buscar(id_almacenamiento)

    def eliminar(self, id_almacenamiento):
        """
        Elimina una instancia de almacenamiento del repositorio.

        :param id_almacenamiento: El ID de la instancia de almacenamiento a eliminar.
        """
        self._almacenamientos.eliminar(id_almacenamiento)

    def todos(self):
        """
        Obtiene una lista de todas las instancias de almacenamiento en el repositorio.

        :return: Una lista con todas las instancias de almacenamiento.
        """
        return list(self._almacenamientos.valores())

    def limpiar(self):
        """
        Limpia el repositorio, eliminando todas las instancias de almacenamiento.
        """
        self._almacenamientos.limpiar()

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de almacenamientos (ID → Objeto Almacenamiento).
        """
        return dict(self._almacenamientos.items())
