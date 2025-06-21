"""
MapeadorArista: Convierte entre modelo de dominio Arista y BaseArista DTO.
"""
from Backend.Infraestructura.Modelos.Modelo_Arista import Arista
from Backend.API.DTOs.BaseArista import BaseArista
from Backend.Infraestructura.Mapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO

class MapeadorArista(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Arista del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(arista: Arista) -> BaseArista:
        """
        Convierte un objeto Arista a un BaseArista DTO.
        Args:
            arista (Arista): Objeto de dominio Arista.
        Returns:
            BaseArista: DTO listo para API.
        """
        return BaseArista(
            origen=getattr(arista.origen.elemento(), 'id_cliente', getattr(arista.origen.elemento(), 'id_almacenamiento', getattr(arista.origen.elemento(), 'id_recarga', 0))),
            destino=getattr(arista.destino.elemento(), 'id_cliente', getattr(arista.destino.elemento(), 'id_almacenamiento', getattr(arista.destino.elemento(), 'id_recarga', 0))),
            peso=float(getattr(arista, 'peso', 0.0))
        )
