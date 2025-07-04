"""
RepositorioRutas: Acceso centralizado y unico a instancias de Ruta.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio

class RepositorioRutas(IRepositorio):
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
            observador.actualizar(evento, self, datos)

    def _clave_ruta(self, ruta):
        """
        Genera clave única para la ruta basada en IDs reales y algoritmo.
        """
        ori = getattr(ruta.origen.elemento, 'id_almacenamiento', getattr(ruta.origen.elemento, 'id_cliente', getattr(ruta.origen.elemento, 'id_recarga', None)))
        dst = getattr(ruta.destino.elemento, 'id_almacenamiento', getattr(ruta.destino.elemento, 'id_cliente', getattr(ruta.destino.elemento, 'id_recarga', None)))
        return f"{ori}-{dst}-{ruta.algoritmo}"

    def agregar(self, ruta, clave=None):
        """
        Agrega instancia de Ruta manteniendo unicidad.
        Calcula clave si no se suministra.
        :param ruta: Objeto Ruta.
        :param clave: Clave única opcional.
        """
        if clave is None:
            clave = self._clave_ruta(ruta)
        existente = self._rutas.buscar(clave)
        if existente:
            self.notificar_observadores('repositorio_rutas_agregada_duplicada', {'clave': clave, 'ruta': existente})
            return existente
        self._rutas.insertar(clave, ruta)
        self.notificar_observadores('repositorio_rutas_agregada', {'clave': clave, 'ruta': ruta})
        return ruta

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
        Retorna un dict serializable de todas las rutas.
        """
        serializado = self._rutas.serializar()
        self.notificar_observadores('repositorio_rutas_serializadas', serializado)
        return serializado

    def items(self):
        """Retorna lista de tuplas (clave, ruta) del HashMap."""
        items = self._rutas.items()
        self.notificar_observadores('repositorio_rutas_items', None)
        return items

    def __iter__(self):
        """Permite iterar sobre las instancias de Ruta."""
        return iter(self._rutas.valores())

    def obtener_hashmap(self):
        """Retorna lista de instancias de Ruta para debug."""
        self.notificar_observadores('repositorio_rutas_hashmap', None)
        return dict(self._rutas.items())

    def asociar_vertices_a_ruta(self, clave, origen, destino):
        """Asocia nuevos vértices de origen y destino a una ruta existente."""
        ruta = self.obtener(clave)
        if ruta:
            ruta.origen = origen
            ruta.destino = destino
            self._rutas.insertar(clave, ruta)
            self.notificar_observadores('repositorio_rutas_vertices_asociados', {'clave': clave, 'origen': origen, 'destino': destino})
        return ruta

    def asociar_camino_a_ruta(self, clave, camino):
        """Asocia una nueva lista de vértices/aristas al camino de la ruta."""
        ruta = self.obtener(clave)
        if ruta:
            ruta.camino = camino
            self._rutas.insertar(clave, ruta)
            self.notificar_observadores('repositorio_rutas_camino_asociado', {'clave': clave, 'camino': camino})
        return ruta

    def obtener_hashmap_serializable(self):
        """
        Retorna el hashmap de rutas serializado como dict plano usando MapeadorRuta.
        :return: Dict con rutas serializadas para API.
        """
        try:
            from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
            resultado = {}
            for clave, ruta in self._rutas.items():
                resultado[str(clave)] = MapeadorRuta.a_hashmap(ruta)
            self.notificar_observadores('repositorio_rutas_hashmap_serializable', {'total': len(resultado)})
            return resultado
        except Exception as e:
            import logging
            logging.getLogger("RepositorioRutas").error(f"Error generando hashmap serializable: {e}")
            return {}
