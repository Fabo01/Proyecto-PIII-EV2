from Backend.Infraestructura.TDA.TDA_Vertice import Vertice
from Backend.API.DTOs.DTOsRespuesta.RespuestaVertice import RespuestaVertice

class MapeadorVertice:
    """
    Clase para mapear objetos Vertice del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(vertice: Vertice) -> RespuestaVertice:
        elemento = getattr(vertice, 'elemento', None)
        id_elemento = None
        tipo = None
        nombre = None
        if elemento:
            # extraer id según tipo de elemento
            id_elemento = getattr(elemento, 'id_cliente', None) or getattr(elemento, 'id_almacenamiento', None) or getattr(elemento, 'id_recarga', None)
            tipo = getattr(elemento, 'tipo_elemento', None)
            nombre = getattr(elemento, 'nombre', None)
        return RespuestaVertice(id=id_elemento, tipo=tipo, nombre=nombre)

    @staticmethod
    def a_hashmap(vertice: Vertice) -> Vertice:
        """
        Devuelve el objeto real Vertice (sin serialización).
        """
        return vertice

    @staticmethod
    def lista_a_dto(vertices):
        if not vertices:
            return []
        return [MapeadorVertice.a_dto(v) for v in vertices if v is not None]

    @staticmethod
    def lista_a_hashmap(vertices):
        """
        Devuelve una lista de objetos reales Vertice.
        """
        return [MapeadorVertice.a_hashmap(v) for v in vertices]
