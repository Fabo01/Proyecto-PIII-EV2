"""
MapeadorPedido: Convierte entre modelo de dominio Pedido y PedidoResponse DTO.
Incluye logging detallado de asociaciones y errores de mapeo.
"""
from Backend.Dominio.Dominio_Pedido import Pedido
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
from Backend.Infraestructura.Repositorios.repositorio_clientes import RepositorioClientes
from Backend.Infraestructura.Repositorios.repositorio_almacenamientos import RepositorioAlmacenamientos
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
import logging

class MapeadorPedido(IMapeadorDominioDTO):
    logger = logging.getLogger("MapeadorPedido")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    @staticmethod
    def a_dto(pedido: Pedido) -> RespuestaPedido:
        """
        Serializa un pedido a un DTO plano, usando RespuestaPedido y serializando asociaciones como dicts planos.
        cliente: nombre (str)
        origen: id (int)
        destino: id (int)
        """
        cliente = getattr(pedido, 'cliente', None)
        origen = getattr(pedido, 'origen', None)
        destino = getattr(pedido, 'destino', None)
        return RespuestaPedido(
            id_pedido=getattr(pedido, 'id_pedido', None),
            prioridad=getattr(pedido, 'prioridad', None),
            status=getattr(pedido, 'status', None),
            fecha_creacion=str(getattr(pedido, 'fecha_creacion', None)),
            fecha_entrega=str(getattr(pedido, 'fecha_entrega', None)) if getattr(pedido, 'fecha_entrega', None) else None,
            cliente=getattr(getattr(destino, 'elemento', None), 'nombre', None) if cliente else None,
            origen=getattr(getattr(origen, 'elemento', None), 'id_almacenamiento', None) or getattr(getattr(origen, 'elemento', None), 'id_recarga', None) if origen else None,
            destino=getattr(getattr(destino, 'elemento', None), 'id_cliente', None) if destino else None
        )

    @staticmethod
    def a_hashmap(pedido: Pedido) -> Pedido:
        """
        Devuelve el objeto real Pedido (sin serialización).
        """
        return pedido

    @staticmethod
    def lista_a_dto(pedidos):
        """
        Convierte una lista de pedidos a una lista de diccionarios DTO.
        """
        if not pedidos:
            return []
        return [MapeadorPedido.a_dto(p) for p in pedidos if p is not None]

    @staticmethod
    def lista_a_hashmap(pedidos):
        """
        Devuelve una lista de objetos reales Pedido.
        """
        return [MapeadorPedido.a_hashmap(p) for p in pedidos]
