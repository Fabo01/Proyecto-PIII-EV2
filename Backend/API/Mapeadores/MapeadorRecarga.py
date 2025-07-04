"""
MapeadorRecarga: Convierte entre modelo de dominio Recarga y RecargaResponse DTO.
"""
from Backend.Dominio.Dominio_Recarga import Recarga
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
from Backend.API.DTOs.DTOsRespuesta.RespuestaRecarga import RespuestaRecarga

class MapeadorRecarga(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Recarga del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(recarga: Recarga) -> RespuestaRecarga:
        return RespuestaRecarga(
            id=int(getattr(recarga, 'id_recarga', 0)),
            tipo=str(getattr(recarga, 'tipo_elemento', 'recarga')),
            nombre=str(getattr(recarga, 'nombre', '')),
        )

    @staticmethod
    def a_hashmap(recarga: Recarga) -> Recarga:
        """
        Devuelve el objeto real Recarga (sin serialización).
        """
        return recarga

    @staticmethod
    def lista_a_dto(recargas):
        if not recargas:
            return []
        return [MapeadorRecarga.a_dto(r) for r in recargas if r is not None]

    @staticmethod
    def lista_a_hashmap(recargas):
        """
        Devuelve una lista de objetos reales Recarga.
        """
        return [MapeadorRecarga.a_hashmap(r) for r in recargas]
