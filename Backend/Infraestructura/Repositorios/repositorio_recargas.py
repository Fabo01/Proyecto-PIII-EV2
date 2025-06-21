"""
RepositorioRecargas: Acceso centralizado y unico a instancias de Recarga.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioRecargas import IRepositorioRecargas

class RepositorioRecargas(IRepositorioRecargas):
    """
    Repositorio para gestionar instancias unicas de Recarga.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._recargas = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_recargas_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, recarga):
        """
        Agrega una nueva instancia de Recarga al repositorio.
        :param recarga: Instancia de Recarga a agregar.
        """
        self._recargas.insertar(recarga.id_recarga, recarga)
        self.notificar_observadores('repositorio_recargas_agregado', {'recarga': recarga})

    def obtener(self, id_recarga):
        """
        Obtiene una instancia de Recarga por su ID.
        :param id_recarga: Identificador unico de la recarga.
        :return: Instancia de Recarga o None si no existe.
        """
        recarga = self._recargas.buscar(id_recarga)
        self.notificar_observadores('repositorio_recargas_obtenido', {'id': id_recarga, 'recarga': recarga})
        return recarga

    def eliminar(self, id_recarga):
        """
        Elimina una instancia de Recarga por su ID.
        :param id_recarga: Identificador unico de la recarga.
        """
        self._recargas.eliminar(id_recarga)
        self.notificar_observadores('repositorio_recargas_eliminado', {'id': id_recarga})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Recarga.
        :return: Lista de instancias de Recarga.
        """
        recargas = list(self._recargas.valores())
        self.notificar_observadores('repositorio_recargas_todos', {'cantidad': len(recargas)})
        return recargas

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Recarga.
        """
        self._recargas = HashMap()
        self.notificar_observadores('repositorio_recargas_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de recargas (ID → Objeto Recarga) como dict.
        :return: Diccionario de recargas.
        """
        self.notificar_observadores('repositorio_recargas_hashmap', None)
        return dict(self._recargas.items())
