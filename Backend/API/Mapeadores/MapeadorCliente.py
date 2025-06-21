"""
MapeadorCliente: Convierte entre modelo de dominio Cliente y ClienteResponse DTO.
"""
from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.API.DTOs.DTOsRespuesta.RespuestaCliente import RespuestaCliente
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO

class MapeadorCliente(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Cliente del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(cliente: Cliente, incluir_pedidos: bool = True) -> RespuestaCliente:
        """
        Convierte un objeto Cliente a un RespuestaCliente DTO.
        Los pedidos serializados en un cliente nunca deben incluir el cliente completo, solo datos básicos.
        Args:
            cliente (Cliente): Objeto de dominio Cliente.
            incluir_pedidos (bool): Si True, mapea los pedidos asociados (como objetos completos, pero sin el cliente completo dentro de cada pedido).
        Returns:
            RespuestaCliente: DTO listo para API.
        """
        pedidos = []
        if incluir_pedidos and hasattr(cliente, 'pedidos'):
            # Importación local para evitar ciclo
            from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
            pedidos = [MapeadorPedido.a_dto(p, incluir_cliente=False, incluir_almacenamiento=True) for p in getattr(cliente, 'pedidos', [])]
        return RespuestaCliente(
            id=int(getattr(cliente, 'id_cliente', 0)),
            tipo=str(getattr(cliente, 'tipo_elemento', 'cliente')),
            nombre=str(getattr(cliente, 'nombre', '')),
            pedidos=pedidos
        )
