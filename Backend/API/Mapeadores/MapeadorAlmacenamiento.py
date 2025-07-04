"""
MapeadorAlmacenamiento: Convierte entre modelo de dominio Almacenamiento y AlmacenamientoResponse DTO.
"""
from Backend.Dominio.Dominio_Almacenamiento import Almacenamiento
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
from Backend.Infraestructura.Repositorios.repositorio_pedidos import RepositorioPedidos
from Backend.API.DTOs.DTOsRespuesta.RespuestaAlmacenamiento import RespuestaAlmacenamiento

class MapeadorAlmacenamiento(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Almacenamiento del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(almacenamiento: Almacenamiento) -> RespuestaAlmacenamiento:
        """
        Serializa un almacenamiento a un dict plano con campos id, tipo, nombre y lista de pedidos.
        """
        # campos básicos
        almacen_id = int(getattr(almacenamiento, 'id_almacenamiento', 0))
        tipo = str(getattr(almacenamiento, 'tipo_elemento', 'almacenamiento'))
        nombre = str(getattr(almacenamiento, 'nombre', ''))
        # pedidos asociados
        repositorio = RepositorioPedidos()
        try:
            pedidos = repositorio.obtener_por_almacenamiento(almacen_id)
        except Exception:
            pedidos = []
        # convertir lista de pedidos a dicts planos con id
        lista_pedidos = [getattr(p, 'id_pedido', None) for p in pedidos]
        return RespuestaAlmacenamiento(id=almacen_id, tipo=tipo, nombre=nombre, pedidos=lista_pedidos)

    @staticmethod
    def a_hashmap(almacen: Almacenamiento) -> Almacenamiento:
        """
        Devuelve el objeto real Almacenamiento (sin serialización).
        """
        return almacen

    @staticmethod
    def lista_a_dto(almacenamientos):
        if not almacenamientos:
            return []
        return [MapeadorAlmacenamiento.a_dto(a) for a in almacenamientos if a is not None]

    @staticmethod
    def lista_a_hashmap(almacenamientos):
        """
        Devuelve una lista de objetos reales Almacenamiento.
        """
        return [MapeadorAlmacenamiento.a_hashmap(a) for a in almacenamientos]
