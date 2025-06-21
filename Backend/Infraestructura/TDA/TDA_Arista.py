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
        Retorna el peso (costo) asociado a la arista.
        """
        return self._peso

    def set_extremos(self, nuevo_origen, nuevo_destino):
        """
        Actualiza los vértices de origen y destino de la arista.
        """
        self._origen = nuevo_origen
        self._destino = nuevo_destino
        self.notificar_observadores('arista_extremos_actualizados', {'origen': nuevo_origen, 'destino': nuevo_destino})

    def set_peso(self, nuevo_peso):
        """
        Actualiza el peso de la arista.
        """
        self._peso = nuevo_peso
        self.notificar_observadores('arista_peso_actualizado', {'peso': nuevo_peso})

    def agregar_observador(self, observador):
        self._observadores.add(observador)

    def quitar_observador(self, observador):
        self._observadores.discard(observador)

    def notificar_observadores(self, evento, datos=None):
        for obs in self._observadores:
            obs.actualizar(evento, self, datos)

    def serializar(self):
        """
        Serializa la arista notificando a los observadores.
        """
        self.notificar_observadores('arista_serializada', {'origen': self._origen, 'destino': self._destino, 'peso': self._peso})
        return {'origen': str(self._origen), 'destino': str(self._destino), 'peso': self._peso}

    def extremos(self):
        """
        Retorna una tupla (origen, destino) de los vértices conectados.
        """
        return (self._origen, self._destino)

    def opuesto(self, vertice):
        """
        Retorna el vértice opuesto al dado en esta arista.
        """
        if vertice == self._origen:
            return self._destino
        elif vertice == self._destino:
            return self._origen
        else:
            raise ValueError('El vertice no es extremo de esta arista')

    def es_conexion(self, tipo_origen, tipo_destino):
        """
        Retorna True si la arista conecta los tipos de vértices dados.
        """
        return self._origen.es_tipo(tipo_origen) and self._destino.es_tipo(tipo_destino)

    def __hash__(self):
        # Incluir peso en hash para consistencia con __eq__
        return hash((self._origen, self._destino, self._peso))

    def __eq__(self, other):
        """
        Dos aristas son iguales si conectan los mismos vértices en el mismo orden y tienen el mismo peso.
        """
        return isinstance(other, Arista) and self._origen == other._origen and self._destino == other._destino and self._peso == other._peso

    def __str__(self):
        return f"Arista({self._origen} -> {self._destino}, peso={self._peso})"

    def __repr__(self):
        return str(self)
