"""
MapeadorSimulacion: Convierte el estado de la simulación a RespuestaSimulacionEstado DTO y a hashmaps de objetos reales.
"""
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from Backend.API.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.API.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.API.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta

class MapeadorSimulacion:
    """
    Clase para mapear el estado de la simulación (dict o modelo) a un DTO de respuesta para la API o a hashmaps de objetos reales.
    """
    @staticmethod
    def a_dto_estado(estado: dict) -> RespuestaSimulacionEstado:
        """
        Convierte el estado de la simulación a un objeto RespuestaSimulacionEstado (solo datos planos para la API).
        """
        import logging
        logger = logging.getLogger("MapeadorSimulacion")
        logger.info(f"[Depuracion] Clientes dominio: {estado.get('clientes', [])}")
        logger.info(f"[Depuracion] Almacenamientos dominio: {estado.get('almacenamientos', [])}")
        logger.info(f"[Depuracion] Recargas dominio: {estado.get('recargas', [])}")
        logger.info(f"[Depuracion] Pedidos dominio: {estado.get('pedidos', [])}")
        logger.info(f"[Depuracion] Rutas dominio: {estado.get('rutas', [])}")
        clientes = [MapeadorCliente.a_dto(c) for c in estado.get('clientes', [])]
        almacenamientos = [MapeadorAlmacenamiento.a_dto(a) for a in estado.get('almacenamientos', [])]
        recargas = [MapeadorRecarga.a_dto(r) for r in estado.get('recargas', [])]
        pedidos = [MapeadorPedido.a_dto(p) for p in estado.get('pedidos', [])]
        rutas = [MapeadorRuta.a_dto(r) for r in estado.get('rutas', [])]
        return RespuestaSimulacionEstado(
            clientes=clientes,
            almacenamientos=almacenamientos,
            recargas=recargas,
            pedidos=pedidos,
            rutas=rutas,
            estado=estado.get('estado', ''),
            mensaje=estado.get('mensaje', None)
        )

    @staticmethod
    def a_hashmap_estado(estado: dict) -> dict:
        """
        Devuelve el estado de la simulación como un dict de objetos reales (o dicts con objetos reales), para uso interno o pruebas.
        """
        return estado
