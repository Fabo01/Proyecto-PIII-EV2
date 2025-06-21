"""
Clase Vertice para representar un vertice en el grafo.
Basado en Docs/vertex.py
"""

class Vertice:
    """
    Representa un vértice (vertice) en el grafo. Solo almacena el elemento asociado (Cliente, Almacenamiento o Recarga).
    No contiene lógica de cliente, pedido ni almacenamiento.
    """
    __slots__ = ['_elemento']

    def __init__(self, elemento):
        """
        Inicializa un vértice con el elemento asociado.
        """
        self._elemento = elemento

    def elemento(self):
        """
        Retorna el elemento asociado a este vértice.
        """
        return self._elemento

    def __hash__(self):
        # Usar el id único del elemento para el hash, evitando instancias duplicadas
        elemento_id = self.id_elemento()
        return hash((type(self._elemento), elemento_id)) if elemento_id is not None else super().__hash__()

    def __eq__(self, other):
        """
        Dos vértices son iguales si son de la misma clase, mismo tipo de elemento y mismo id de elemento.
        """
        if not isinstance(other, Vertice):
            return False
        id_self = self.id_elemento()
        id_other = other.id_elemento()
        return (
            type(self._elemento) == type(other._elemento)
            and id_self is not None
            and id_self == id_other
        )

    def __str__(self):
        return str(self._elemento)

    def __repr__(self):
        return f"Vertice({self._elemento})"

    def __lt__(self, other):
        # Ordenar por id de elemento si es posible
        return self.id_elemento() < other.id_elemento()

    def es_tipo(self, tipo):
        """
        Retorna True si el elemento asociado es del tipo indicado (str).
        """
        return hasattr(self._elemento, 'tipo_elemento') and self._elemento.tipo_elemento == tipo

    def id_elemento(self):
        """
        Retorna el id único del elemento asociado (id_cliente, id_almacenamiento, id_recarga).
        """
        # Busca el atributo id_* en el elemento
        for attr in ['id_cliente', 'id_almacenamiento', 'id_recarga']:
            if hasattr(self._elemento, attr):
                return getattr(self._elemento, attr)
        return None
