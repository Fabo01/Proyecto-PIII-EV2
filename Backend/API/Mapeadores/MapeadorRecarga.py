"""
MapeadorRecarga: Convierte entre modelo de dominio Recarga y RecargaResponse DTO.
"""
from Backend.Dominio.Dominio_Recarga import Recarga
from Backend.API.DTOs.DTOsRespuesta.RespuestaRecarga import RespuestaRecarga
from Backend.Infraestructura.Mapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO

class MapeadorRecarga(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Recarga del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(recarga: Recarga) -> RespuestaRecarga:
        """
        Convierte un objeto Recarga a un RespuestaRecarga DTO.
        Args:
            recarga (Recarga): Objeto de dominio Recarga.
        Returns:
            RespuestaRecarga: DTO listo para API.
        """
        return RespuestaRecarga(
            id=int(getattr(recarga, 'id_recarga', 0)),
            tipo=str(getattr(recarga, 'tipo_elemento', 'recarga')),
            nombre=str(getattr(recarga, 'nombre', ''))
        )
