"""
Clase Arista para representar una conexión entre vertices en el grafo.
Basado en Docs/edge.py
"""

class Arista:
    """
    Representa una arista (conexion) entre dos vertices en el grafo.
    Notifica a observadores en operaciones CRUD y mapeo.
    """
    __slots__ = ['_origen', '_destino', '_peso', '_observadores']

    def __init__(self, origen, destino, peso):
        """
        Inicializa una arista entre los vértices origen y destino, con un peso asociado (peso/coste).
        """
        self._origen = origen
        self._destino = destino
        self._peso = peso
        self._observadores = set()
        self.notificar_observadores('arista_creada', {'origen': origen, 'destino': destino, 'peso': peso})

    @property
    def origen(self):
        """
        Retorna el vértice de origen de la arista.
        """
        return self._origen

    @property
    def destino(self):
        """
        Retorna el vértice de destino de la arista.
        """
        return self._destino

    @property
    def peso(self):
        """
        Retorna el peso de la arista.
        """
        return self._peso

    def set_extremos(self, nuevo_origen, nuevo_destino):
        self._origen = nuevo_origen
        self._destino = nuevo_destino
        self.notificar_observadores('arista_actualizada', {'origen': nuevo_origen, 'destino': nuevo_destino})

    def set_peso(self, nuevo_peso):
        self._peso = nuevo_peso
        self.notificar_observadores('peso_actualizado', {'peso': nuevo_peso})

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for observador in self._observadores:
            observador.actualizar(evento, self, datos)

    def serializar(self):
        """
        Serializa la arista usando los IDs reales de los elementos de los vértices de origen y destino.
        Devuelve un diccionario plano con 'origen', 'destino' y 'peso'.
        """
        def obtener_id_elemento(vertice):
            elemento = getattr(vertice, 'elemento', None)
            if elemento is None:
                return None
            if hasattr(elemento, 'id_cliente'):
                return elemento.id_cliente
            elif hasattr(elemento, 'id_almacenamiento'):
                return elemento.id_almacenamiento
            elif hasattr(elemento, 'id_recarga'):
                return elemento.id_recarga
            else:
                return None
        return {
            'origen': obtener_id_elemento(self._origen),
            'destino': obtener_id_elemento(self._destino),
            'peso': self._peso
        }

    def __hash__(self):
        return hash((self._origen, self._destino, self._peso))

    def __eq__(self, other):
        if not isinstance(other, Arista):
            return False
        return (self._origen == other._origen and self._destino == other._destino and self._peso == other._peso)

    def __str__(self):
        return f"Arista({self._origen} -> {self._destino}, peso={self._peso})"

    def __repr__(self):
        return str(self)
