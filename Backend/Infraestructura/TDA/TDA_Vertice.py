"""
Clase Vertice para representar un vertice en el grafo.
Basado en Docs/vertex.py
"""

class Vertice:
    """
    Representa un vertice en el grafo. Solo almacena el elemento asociado (Cliente, Almacenamiento o Recarga).
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    __slots__ = ['_elemento', '_observadores']

    def __init__(self, elemento):
        """
        Inicializa un vertice con el elemento asociado.
        """
        self._elemento = elemento
        self._observadores = set()
        self.notificar_observadores('vertice_creado', {'elemento': elemento})

    @property
    def elemento(self):
        """
        Retorna el elemento asociado a este vertice.
        """
        return self._elemento

    def set_elemento(self, nuevo_elemento):
        """
        Actualiza el elemento asociado a este vertice y notifica a los observadores.
        """
        self._elemento = nuevo_elemento
        self.notificar_observadores('vertice_elemento_actualizado', {'elemento': nuevo_elemento})

    def agregar_observador(self, observador):
        """
        Agrega un observador para recibir notificaciones de este vertice.
        """
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        """
        Quita un observador para dejar de recibir notificaciones de este vertice.
        """
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores registrados sobre un evento.
        """
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def serializar(self):
        """
        Serializa el vertice y notifica a los observadores sobre la serializacion.
        """
        self.notificar_observadores('vertice_serializado', {'elemento': self._elemento})
        return {'elemento': str(self._elemento)}

    def __hash__(self):
        return hash(self._elemento)

    def __eq__(self, other):
        return isinstance(other, Vertice) and self._elemento == other._elemento

    def __str__(self):
        return str(self._elemento)

    def __repr__(self):
        return f"Vertice({repr(self._elemento)})"

    def __lt__(self, other):
        return str(self._elemento) < str(other._elemento)

    def es_tipo(self, tipo):
        """
        Retorna True si el elemento asociado es del tipo especificado.
        """
        return getattr(self._elemento, 'tipo_elemento', None) == tipo

    def id_elemento(self):
        """
        Retorna el identificador unico del elemento asociado.
        """
        if hasattr(self._elemento, 'id_cliente'):
            return self._elemento.id_cliente
        if hasattr(self._elemento, 'id_almacenamiento'):
            return self._elemento.id_almacenamiento
        if hasattr(self._elemento, 'id_recarga'):
            return self._elemento.id_recarga
        return None
