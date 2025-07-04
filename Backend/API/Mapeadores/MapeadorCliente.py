"""
MapeadorCliente: Convierte entre modelo de dominio Cliente y ClienteResponse DTO.
"""
from Backend.Dominio.Dominio_Cliente import Cliente
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.API.DTOs.DTOsRespuesta.RespuestaCliente import RespuestaCliente

class MapeadorCliente(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Cliente del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(cliente: Cliente) -> RespuestaCliente:
        """
        Serializa un cliente a un dict plano, incluyendo los campos id, tipo, nombre y total de pedidos.
        """
        # campos básicos
        cliente_id = int(getattr(cliente, 'id_cliente', 0))
        tipo = str(getattr(cliente, 'tipo_elemento', 'cliente'))
        nombre = str(getattr(cliente, 'nombre', ''))
        # total de pedidos asociados
        try:
            pedidos = RepositorioPedidos().obtener_por_cliente(cliente_id)
        except Exception:
            pedidos = []
        # convertir lista de pedidos a dicts planos con id
        lista_pedidos = [getattr(p, 'id_pedido', None) for p in pedidos]
        return RespuestaCliente(id=cliente_id, tipo=tipo, nombre=nombre, pedidos=lista_pedidos)

    @staticmethod
    def a_hashmap(cliente: Cliente) -> Cliente:
        """
        Devuelve el objeto real Cliente (sin serialización).
        """
        return cliente

    @staticmethod
    def lista_a_dto(clientes):
        if not clientes:
            return []
        return [MapeadorCliente.a_dto(c) for c in clientes if c is not None]

    @staticmethod
    def lista_a_hashmap(clientes):
        """
        Devuelve una lista de objetos reales Cliente.
        """
        return [MapeadorCliente.a_hashmap(c) for c in clientes]
