"""
RepositorioVertices: Acceso centralizado y unico a instancias de Vertice.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio

class RepositorioVertices(IRepositorio):
    """
    Repositorio para gestionar instancias unicas de Vertice.
    Garantiza unicidad y acceso O(1) mediante HashMap.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._vertices = HashMap()
            cls._instancia._observadores = set()
            cls._instancia.notificar_observadores('repositorio_vertices_creado', None)
        return cls._instancia

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def agregar(self, vertice, id_elemento):
        """
        Agrega un vertice al repositorio asegurando unicidad.
        Si ya existe un vertice con el mismo id_elemento, retorna la instancia existente.
        :param vertice: Instancia de Vertice a agregar.
        :param id_elemento: Identificador único del elemento.
        :return: Instancia existente o nueva de Vertice.
        """
        existente = self._vertices.buscar(id_elemento)
        if existente:
            self.notificar_observadores('repositorio_vertices_agregado_duplicado', {'id_elemento': id_elemento, 'vertice': existente})
            return existente
        self._vertices.insertar(id_elemento, vertice)
        self.notificar_observadores('repositorio_vertices_agregado', {'id_elemento': id_elemento, 'vertice': vertice})
        return vertice

    def obtener(self, id_elemento):
        """
        Obtiene un vertice del repositorio por su ID.
        :param id_elemento: Identificador unico del elemento.
        :return: Instancia de Vertice o None si no existe.
        """
        vertice = self._vertices.buscar(id_elemento)
        self.notificar_observadores('repositorio_vertices_obtenido', {'id_elemento': id_elemento, 'vertice': vertice})
        return vertice

    def eliminar(self, id_elemento):
        """
        Elimina un vertice del repositorio por su ID.
        :param id_elemento: Identificador unico del elemento.
        """
        self._vertices.eliminar(id_elemento)
        self.notificar_observadores('repositorio_vertices_eliminado', {'id_elemento': id_elemento})

    def todos(self):
        """
        Retorna una lista de todas las instancias de Vertice.
        :return: Lista de instancias de Vertice.
        """
        vertices = list(self._vertices.valores())
        self.notificar_observadores('repositorio_vertices_todos', {'cantidad': len(vertices)})
        return vertices

    def limpiar(self):
        """
        Reinicializa el repositorio, eliminando todas las instancias de Vertice.
        """
        self._vertices = HashMap()
        self.notificar_observadores('repositorio_vertices_limpiado', None)

    def obtener_hashmap(self):
        """
        Retorna el hashmap interno de vertices (ID → Objeto Vertice) como dict.
        :return: Diccionario de vertices.
        """
        self.notificar_observadores('repositorio_vertices_hashmap', None)
        return dict(self._vertices.items())

    def obtener_hashmap_serializable(self):
        """
        Retorna el hashmap de vertices serializado como dict plano usando MapeadorVertice.
        :return: Diccionario de vertices serializados.
        """
        try:
            from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice
            resultado = {}
            for id_el, vert in self._vertices.items():
                resultado[str(id_el)] = MapeadorVertice.a_hashmap(vert)
            self.notificar_observadores('repositorio_vertices_hashmap_serializable', {'total': len(resultado)})
            return resultado
        except Exception as e:
            import logging
            logging.getLogger("RepositorioVertices").error(f"Error generando hashmap serializable: {e}")
            return {}
