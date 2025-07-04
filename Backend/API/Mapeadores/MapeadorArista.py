"""
MapeadorArista: Convierte entre modelo de dominio Arista y BaseArista DTO.
"""
from Backend.Infraestructura.TDA.TDA_Arista import Arista
from Backend.API.DTOs.DTOsRespuesta.RespuestaArista import RespuestaArista


class MapeadorArista:
    """
    Clase utilitaria para mapear objetos Arista del dominio a DTOs serializables para la API y hashmaps de objetos reales.
    """
    
    @staticmethod
    def a_dto(arista: Arista) -> RespuestaArista:
        """
        Serializa una arista a un dict plano, incluyendo solo los campos id, origen (ID), destino (ID), peso y tipo.
        """

        def obtener_id_elemento(vertice):
            elemento = getattr(vertice, 'elemento', None)
            if elemento is None:
                return None
            if hasattr(elemento, 'id_cliente'):
                return elemento.id_cliente
            if hasattr(elemento, 'id_almacenamiento'):
                return elemento.id_almacenamiento
            if hasattr(elemento, 'id_recarga'):
                return elemento.id_recarga
            return None
        origen_id = obtener_id_elemento(getattr(arista, 'origen', None))
        destino_id = obtener_id_elemento(getattr(arista, 'destino', None))
        peso = getattr(arista, 'peso', None)
        return RespuestaArista(origen=origen_id, destino=destino_id, peso=peso)

    @staticmethod
    def a_hashmap(arista: Arista) -> Arista:
        """
        Devuelve el objeto real Arista (con sus referencias reales, no serializa nada).
        """
        return arista

    @staticmethod
    def lista_a_dto(aristas):
        if not aristas:
            return []
        return [MapeadorArista.a_dto(a) for a in aristas if a is not None]

    @staticmethod
    def lista_a_hashmap(aristas):
        """
        Devuelve una lista de objetos reales Arista (con referencias reales).
        """
        # no se usa en API principales, pero mantenido para debug
        return { f"{a.origen_id}-{a.destino_id}": a for a in aristas }
