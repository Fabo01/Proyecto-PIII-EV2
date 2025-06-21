"""
MapeadorAlmacenamiento: Convierte entre modelo de dominio Almacenamiento y AlmacenamientoResponse DTO.
"""
from Backend.Dominio.Dominio_Almacenamiento import Almacenamiento
from Backend.API.DTOs.DTOsRespuesta.RespuestaAlmacenamiento import RespuestaAlmacenamiento
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido

class MapeadorAlmacenamiento(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Almacenamiento del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(almacen: Almacenamiento, incluir_pedidos: bool = True) -> RespuestaAlmacenamiento:
        """
        Convierte un objeto Almacenamiento a un RespuestaAlmacenamiento DTO.
        Args:
            almacen (Almacenamiento): Objeto de dominio Almacenamiento.
            incluir_pedidos (bool): Si True, mapea los pedidos asociados.
        Returns:
            RespuestaAlmacenamiento: DTO listo para API.
        """
        pedidos = []
        if incluir_pedidos and hasattr(almacen, '_pedidos'):
            pedidos = [MapeadorPedido.a_dto(p, incluir_cliente=True, incluir_almacenamiento=False) for p in getattr(almacen, '_pedidos', [])]
        return RespuestaAlmacenamiento(
            id=int(getattr(almacen, 'id_almacenamiento', 0)),
            tipo=str(getattr(almacen, 'tipo_elemento', 'almacenamiento')),
            nombre=str(getattr(almacen, 'nombre', '')),
            pedidos=pedidos
        )
