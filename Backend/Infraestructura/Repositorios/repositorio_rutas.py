"""
RepositorioRutas: Acceso centralizado y unico a instancias de Ruta.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorioRutas import IRepositorioRutas

class RepositorioRutas(IRepositorioRutas):
    """
    Repositorio para gestionar instancias unicas de Ruta.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._rutas = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_rutas_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for observador in self._observadores:
            observador.actualizar(evento, datos)

    def agregar(self, ruta, clave):
        """
        Agrega una nueva instancia de Ruta al repositorio.
        :param ruta: Instancia de Ruta a agregar.
        :param clave: Clave unica para la ruta (por ejemplo, tupla de IDs).
        """
        self._rutas.insertar(clave, ruta)
        self.notificar_observadores('repositorio_rutas_agregada', {'clave': clave, 'ruta': ruta})

    def obtener(self, clave):
        """
        Obtiene una instancia de Ruta por su clave.
        :param clave: Clave unica de la ruta.
        :return: Instancia de Ruta o None si no existe.
        """
        ruta = self._rutas.buscar(clave)
        self.notificar_observadores('repositorio_rutas_obtenida', {'clave': clave, 'ruta': ruta})
        return ruta

    def eliminar(self, clave):
        """
        Elimina una instancia de Ruta por su clave.
        :param clave: Clave unica de la ruta.
        """
        self._rutas.eliminar(clave)
        self.notificar_observadores('repositorio_rutas_eliminada', {'clave': clave})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Ruta.
        :return: Lista de instancias de Ruta.
        """
        rutas = list(self._rutas.valores())
        self.notificar_observadores('repositorio_rutas_todos', {'cantidad': len(rutas)})
        return rutas

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Ruta.
        """
        self._rutas.limpiar()
        self.notificar_observadores('repositorio_rutas_limpiado', None)

    def serializar(self):
        """
        Serializa las rutas en el repositorio a un formato adecuado para almacenamiento o transmisión.
        :return: Datos serializados de las rutas.
        """
        serializado = self._rutas.serializar()
        self.notificar_observadores('repositorio_rutas_serializadas', serializado)
        return serializado

    def items(self):
        """
        Retorna todos los items (clave, valor) en el repositorio de rutas.
        :return: Vista de items en el repositorio.
        """
        items = self._rutas.items()
        self.notificar_observadores('repositorio_rutas_items', None)
        return items

    def __iter__(self):
        """
        Permite la iteración sobre los items del repositorio.
        :return: Iterador de los items en el repositorio.
        """
        return iter(self._rutas.items())

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de rutas (clave → Objeto Ruta) como dict.
        :return: Diccionario de rutas.
        """
        self.notificar_observadores('repositorio_rutas_hashmap', None)
        return dict(self._rutas.items())
