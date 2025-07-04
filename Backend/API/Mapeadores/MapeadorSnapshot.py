"""
MapeadorSnapshot: Convierte un snapshot de grafo (dict) a RespuestaSnapshot DTO o a hashmaps de objetos reales.
"""
from Backend.API.DTOs.DTOsRespuesta.RespuestaSnapshot import RespuestaSnapshot

class MapeadorSnapshot:
    @staticmethod
    def a_dto(snapshot: dict) -> RespuestaSnapshot:
        """
        Convierte un snapshot de grafo (dict plano) a un DTO serializable para la API.
        """
        return RespuestaSnapshot(
            vertices=snapshot.get('vertices', []),
            aristas=snapshot.get('aristas', []),
            dirigido=snapshot.get('dirigido', False)
        )

    @staticmethod
    def a_hashmap(snapshot: dict) -> dict:
        """
        Devuelve el snapshot original (dict de objetos reales), para uso interno o pruebas.
        """
        return snapshot
