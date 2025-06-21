"""
RepositorioAristas: Acceso centralizado y unico a instancias de Arista.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioAristas import IRepositorioAristas

class RepositorioAristas(IRepositorioAristas):
    """
    Repositorio para gestionar instancias unicas de Arista.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._aristas = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_aristas_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, arista, clave=None):
        """
        Agrega una nueva instancia de Arista al repositorio.
        :param arista: Instancia de Arista a agregar.
        :param clave: Clave unica para la arista (por defecto, tupla de IDs de origen y destino).
        """
        if clave is None:
            clave = (getattr(arista.origen.elemento(), 'id_cliente', None) or getattr(arista.origen.elemento(), 'id_almacenamiento', None) or getattr(arista.origen.elemento(), 'id_recarga', None),
                     getattr(arista.destino.elemento(), 'id_cliente', None) or getattr(arista.destino.elemento(), 'id_almacenamiento', None) or getattr(arista.destino.elemento(), 'id_recarga', None))
        self._aristas.insertar(clave, arista)
        self.notificar_observadores('repositorio_aristas_agregada', {'clave': clave, 'arista': arista})

    def obtener(self, clave):
        """
        Obtiene una instancia de Arista por su clave.
        :param clave: Clave unica de la arista.
        :return: Instancia de Arista o None si no existe.
        """
        arista = self._aristas.buscar(clave)
        self.notificar_observadores('repositorio_aristas_obtenida', {'clave': clave, 'arista': arista})
        return arista

    def eliminar(self, clave):
        """
        Elimina una instancia de Arista por su clave.
        :param clave: Clave unica de la arista.
        """
        self._aristas.eliminar(clave)
        self.notificar_observadores('repositorio_aristas_eliminada', {'clave': clave})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Arista.
        :return: Lista de instancias de Arista.
        """
        aristas = list(self._aristas.valores())
        self.notificar_observadores('repositorio_aristas_todos', {'cantidad': len(aristas)})
        return aristas

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Arista.
        """
        self._aristas = HashMap()
        self.notificar_observadores('repositorio_aristas_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de aristas (clave → Objeto Arista) como dict.
        :return: Diccionario de aristas.
        """
        self.notificar_observadores('repositorio_aristas_hashmap', None)
        return dict(self._aristas.items())
