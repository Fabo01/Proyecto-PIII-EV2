"""
MapeadorSimulacion: Convierte el estado de la simulación a RespuestaSimulacionEstado DTO.
"""
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from Backend.API.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.API.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.API.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta

class MapeadorSimulacion:
    """
    Clase para mapear el estado de la simulación (dict o modelo) a un DTO de respuesta para la API.
    """
    @staticmethod
    def a_dto_estado(estado: dict) -> RespuestaSimulacionEstado:
        """
        Convierte el estado de la simulación a un objeto RespuestaSimulacionEstado.
        Args:
            estado (dict): Estado de la simulación, con claves: clientes, almacenamientos, recargas, pedidos, rutas, estado, mensaje.
        Returns:
            RespuestaSimulacionEstado: DTO listo para la API.
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
