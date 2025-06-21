"""
Clase Arista para representar una conexión entre vertices en el grafo.
Basado en Docs/edge.py
"""

class Arista:
    """
    Representa una arista (conexión) entre dos vértices en el grafo.
    El atributo 'peso' almacena el peso/coste de la arista.
    No contiene lógica de negocio, solo estructura de datos.
    """
    __slots__ = ['_origen', '_destino', '_peso']

    def __init__(self, origen, destino, peso):
        """
        Inicializa una arista entre los vértices origen y destino, con un peso asociado (peso/coste).
        """
        self._origen = origen
        self._destino = destino
        self._peso = peso

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

    def extremos(self):
        """
        Retorna una tupla (origen, destino) de los vértices conectados.
        """
        return (self._origen, self._destino)

    def opuesto(self, vertice):
        """
        Retorna el vértice opuesto al dado en esta arista.
        """
        return self._destino if vertice is self._origen else self._origen

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
        if not isinstance(other, Arista):
            return False
        return (
            self._origen == other._origen
            and self._destino == other._destino
            and self._peso == other._peso
        )

    def __str__(self):
        return f"Arista({self._origen} -> {self._destino}, peso={self._peso})"

    def __repr__(self):
        return self.__str__()
