"""
MapeadorPedido: Convierte entre modelo de dominio Pedido y PedidoResponse DTO.
"""
from Backend.Dominio.Dominio_Pedido import Pedido
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
from Backend.Infraestructura.Mapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
from Backend.Infraestructura.Mapeadores.MapeadorRuta import MapeadorRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaVertice import RespuestaVertice

class MapeadorPedido(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Pedido del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(pedido: Pedido, incluir_cliente: bool = True, incluir_almacenamiento: bool = True) -> RespuestaPedido:
        """
        Convierte un objeto Pedido a un RespuestaPedido DTO.
        El cliente serializado en el pedido nunca debe incluir su lista de pedidos (solo datos básicos).
        Args:
            pedido (Pedido): Objeto de dominio Pedido.
            incluir_cliente (bool): Si True, mapea el cliente asociado (sin sus pedidos para evitar recursividad).
        Returns:
            RespuestaPedido: DTO listo para API.
        """
        # Importaciones locales para evitar ciclo
        if incluir_cliente:
            from Backend.Infraestructura.Mapeadores.MapeadorCliente import MapeadorCliente

        cliente_dto = None
        if incluir_cliente and hasattr(pedido, 'obtener_cliente'):
            cliente = pedido.obtener_cliente() if callable(pedido.obtener_cliente) else None
            if cliente is not None:
                # Siempre serializar cliente sin su lista de pedidos
                cliente_dto = MapeadorCliente.a_dto(cliente, incluir_pedidos=False)

        # Origen y destino como RespuestaVertice
        origen_dto = None
        if hasattr(pedido, 'obtener_origen'):
            origen = pedido.obtener_origen() if callable(pedido.obtener_origen) else None
            if origen is not None:
                elem = origen.elemento() if hasattr(origen, 'elemento') else origen
                origen_dto = RespuestaVertice(
                    id=getattr(elem, 'id_cliente', getattr(elem, 'id_almacenamiento', getattr(elem, 'id_recarga', 0))),
                    tipo=getattr(elem, 'tipo_elemento', ''),
                    nombre=getattr(elem, 'nombre', '')
                )

        destino_dto = None
        if hasattr(pedido, 'obtener_destino'):
            destino = pedido.obtener_destino() if callable(pedido.obtener_destino) else None
            if destino is not None:
                elem = destino.elemento() if hasattr(destino, 'elemento') else destino
                destino_dto = RespuestaVertice(
                    id=getattr(elem, 'id_cliente', getattr(elem, 'id_almacenamiento', getattr(elem, 'id_recarga', 0))),
                    tipo=getattr(elem, 'tipo_elemento', ''),
                    nombre=getattr(elem, 'nombre', '')
                )

        # Ruta (si existe)
        ruta_dto = None
        if hasattr(pedido, 'ruta') and pedido.ruta is not None:
            ruta_dto = MapeadorRuta.a_dto(pedido.ruta)

        # Manejo robusto de peso_total
        peso = getattr(pedido, 'peso_total', 0.0)
        try:
            peso_float = float(peso) if peso is not None else 0.0
        except (TypeError, ValueError):
            peso_float = 0.0

        return RespuestaPedido(
            id_pedido=int(getattr(pedido, 'id_pedido', 0)),
            cliente=cliente_dto,
            prioridad=str(getattr(pedido, 'prioridad', '')),
            status=str(getattr(pedido, 'status', 'pendiente')),
            ruta=ruta_dto,
            peso_total=peso_float,
            origen=origen_dto,
            destino=destino_dto,
            fecha_creacion=str(getattr(pedido, 'fecha_creacion', '')) if hasattr(pedido, 'fecha_creacion') else None,
            fecha_entrega=str(getattr(pedido, 'fecha_entrega', '')) if hasattr(pedido, 'fecha_entrega') else None
        )
