"""
RepositorioAristas: Acceso centralizado y unico a instancias de Arista.
Utiliza HashMap para acceso O(1) y garantiza instanciacion unica.
"""
from Backend.Infraestructura.TDA.TDA_Hash_map import HashMap
from Backend.Dominio.Interfaces.IntRepos.IRepositorio import IRepositorio

class RepositorioAristas(IRepositorio):
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
            cls._instancia._aristas_por_origen = HashMap()
            cls._instancia._aristas_por_destino = HashMap()
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

    def _obtener_id_tipo(self, vertice):
        """
        Retorna el ID y tipo real del elemento asociado a un vertice.
        """
        elemento = getattr(vertice, 'elemento', None)
        if elemento is None:
            return None, None
        if hasattr(elemento, 'id_cliente'):
            return elemento.id_cliente, 'cliente'
        if hasattr(elemento, 'id_almacenamiento'):
            return elemento.id_almacenamiento, 'almacenamiento'
        if hasattr(elemento, 'id_recarga'):
            return elemento.id_recarga, 'recarga'
        return None, None

    def _clave_arista(self, arista):
        """
        Genera la clave unica 'origenID-destinoID' para la arista usando los IDs reales de los elementos.
        """
        id_origen, _ = self._obtener_id_tipo(arista.origen)
        id_destino, _ = self._obtener_id_tipo(arista.destino)
        return f"{id_origen}-{id_destino}"

    def agregar(self, arista, clave=None):
        """
        Agrega una instancia única de Arista.
        Si ya existe devuelve la existente y fusiona lógica necesaria.
        """
        # Calcular clave si no viene
        if clave is None:
            clave = self._clave_arista(arista)
        existente = self._aristas.buscar(clave)
        if existente:
            self.notificar_observadores('repositorio_aristas_agregada_duplicada', {'clave': clave, 'arista': existente})
            return existente
        # Insertar arista real
        self._aristas.insertar(clave, arista)
        # Índice por origen
        id_origen, _ = self._obtener_id_tipo(arista.origen)
        lista_ori = self._aristas_por_origen.buscar(id_origen) or []
        lista_ori.append(arista)
        self._aristas_por_origen.insertar(id_origen, lista_ori)
        # Índice por destino
        id_destino, _ = self._obtener_id_tipo(arista.destino)
        lista_dest = self._aristas_por_destino.buscar(id_destino) or []
        lista_dest.append(arista)
        self._aristas_por_destino.insertar(id_destino, lista_dest)
        self.notificar_observadores('repositorio_aristas_agregada', {'clave': clave, 'arista': arista})
        return arista

    def obtener(self, clave):
        """
        Retorna objeto Arista real por clave.
        """
        arista = self._aristas.buscar(clave)
        self.notificar_observadores('repositorio_aristas_obtenida', {'clave': clave, 'arista': arista})
        return arista

    def eliminar(self, clave):
        """
        Elimina la arista y sus referencias en índices secundarios.
        """
        arista = self._aristas.buscar(clave)
        if not arista:
            return
        id_origen, _ = self._obtener_id_tipo(arista.origen)
        ori_list = [a for a in (self._aristas_por_origen.buscar(id_origen) or []) if self._clave_arista(a) != clave]
        self._aristas_por_origen.insertar(id_origen, ori_list)
        id_destino, _ = self._obtener_id_tipo(arista.destino)
        dest_list = [a for a in (self._aristas_por_destino.buscar(id_destino) or []) if self._clave_arista(a) != clave]
        self._aristas_por_destino.insertar(id_destino, dest_list)
        self._aristas.eliminar(clave)
        self.notificar_observadores('repositorio_aristas_eliminada', {'clave': clave})

    def todos(self):
        """
        Lista de todas las aristas reales.
        """
        todas = list(self._aristas.valores())
        self.notificar_observadores('repositorio_aristas_todas', {'cantidad': len(todas)})
        return todas

    def limpiar(self):
        """
        Elimina todas las instancias de Arista.
        """
        self._aristas = HashMap()
        self._aristas_por_origen = HashMap()
        self._aristas_por_destino = HashMap()
        self.notificar_observadores('repositorio_aristas_limpiado', None)

    def buscar_por_origen(self, id_origen):
        """
        Lista de aristas con origen matching.
        """
        return list(self._aristas_por_origen.buscar(id_origen) or [])

    def buscar_por_destino(self, id_destino):
        """
        Lista de aristas con destino matching.
        """
        return list(self._aristas_por_destino.buscar(id_destino) or [])

    def buscar_por_origen_destino(self, id_origen, id_destino):
        """
        Arista que conecta id_origen -> id_destino.
        """
        return [a for a in self.buscar_por_origen(id_origen) if self._clave_arista(a) == f"{id_origen}-{id_destino}"]

    def obtener_hashmap(self):
        """
        HashMap real de aristas.
        """
        self.notificar_observadores('repositorio_aristas_hashmap', None)
        return dict(self._aristas.items())

    def obtener_hashmap_serializable(self):
        """
        Retorna el hashmap de aristas serializado como dict plano usando MapeadorArista.
        :return: Dict con aristas serializadas para API.
        """
        try:
            from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
            resultado = {}
            for clave, arista in self._aristas.items():
                resultado[str(clave)] = MapeadorArista.a_hashmap(arista)
            self.notificar_observadores('repositorio_aristas_hashmap_serializable', {'total': len(resultado)})
            return resultado
        except Exception as e:
            import logging
            logging.getLogger('RepositorioAristas').error(f"Error generando hashmap serializable: {e}")
            return {}

    def buscar_por_origen(self, id_origen):
        """
        Retorna lista de Arista cuya arista.origen.elemento.id == id_origen
        """
        return list(self._aristas_por_origen.buscar(id_origen) or [])

    def buscar_por_destino(self, id_destino):
        """
        Retorna una lista de aristas donde el destino coincide con id_destino.
        """
        return list(self._aristas_por_destino.buscar(id_destino) or [])

    def buscar_por_origen_destino(self, id_origen, id_destino):
        """
        Retorna la arista que conecta id_origen → id_destino, o None.
        """
        return [a for a in self.buscar_por_origen(id_origen) if self._obtener_id_tipo(a.destino)[0] == id_destino]

    def buscar_por_id_elemento(self, id_elemento):
        """
        Retorna todas las aristas donde id_elemento es origen o destino.
        """
        return self.buscar_por_origen(id_elemento) + self.buscar_por_destino(id_elemento)

    def relaciones(self):
        """
        Retorna una lista de relaciones planas: cada una es un dict con ids, tipos y peso, para análisis o frontend.
        """
        relaciones = {}
        for clave, arista in self._aristas.items():
            id_origen, tipo_origen = self._obtener_id_tipo(arista.origen)
            id_destino, tipo_destino = self._obtener_id_tipo(arista.destino)
            relaciones[clave] = {
                'origen_id': id_origen,
                'destino_id': id_destino,
                'tipo_origen': tipo_origen,
                'tipo_destino': tipo_destino,
                'peso': arista.peso
            }
        return relaciones
