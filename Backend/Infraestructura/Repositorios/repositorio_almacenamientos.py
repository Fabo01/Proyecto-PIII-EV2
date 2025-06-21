"""
RepositorioAlmacenamientos: Acceso centralizado y unico a instancias de Almacenamiento.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioAlmacenamientos import IRepositorioAlmacenamientos

class RepositorioAlmacenamientos(IRepositorioAlmacenamientos):
    """
    Repositorio para gestionar instancias unicas de Almacenamiento.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._almacenamientos = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_almacenamientos_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, almacen):
        """
        Agrega una nueva instancia de Almacenamiento al repositorio.
        :param almacen: Instancia de Almacenamiento a agregar.
        """
        self._almacenamientos.insertar(almacen.id_almacenamiento, almacen)
        self.notificar_observadores('repositorio_almacenamientos_agregado', {'almacen': almacen})

    def obtener(self, id_almacenamiento):
        """
        Obtiene una instancia de Almacenamiento por su ID.
        :param id_almacenamiento: Identificador unico del almacenamiento.
        :return: Instancia de Almacenamiento o None si no existe.
        """
        almacen = self._almacenamientos.buscar(id_almacenamiento)
        self.notificar_observadores('repositorio_almacenamientos_obtenido', {'id': id_almacenamiento, 'almacen': almacen})
        return almacen

    def eliminar(self, id_almacenamiento):
        """
        Elimina una instancia de Almacenamiento por su ID.
        :param id_almacenamiento: Identificador unico del almacenamiento.
        """
        self._almacenamientos.eliminar(id_almacenamiento)
        self.notificar_observadores('repositorio_almacenamientos_eliminado', {'id': id_almacenamiento})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Almacenamiento.
        :return: Lista de instancias de Almacenamiento.
        """
        almacenamientos = list(self._almacenamientos.valores())
        self.notificar_observadores('repositorio_almacenamientos_todos', {'cantidad': len(almacenamientos)})
        return almacenamientos

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Almacenamiento.
        """
        self._almacenamientos = HashMap()
        self.notificar_observadores('repositorio_almacenamientos_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de almacenamientos (ID → Objeto Almacenamiento) como dict.
        :return: Diccionario de almacenamientos.
        """
        self.notificar_observadores('repositorio_almacenamientos_hashmap', None)
        return dict(self._almacenamientos.items())
