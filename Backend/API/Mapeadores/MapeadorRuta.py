"""
MapeadorRuta: Convierte entre modelo de dominio Ruta y RutaResponse DTO.
"""
from Backend.Dominio.Dominio_Ruta import Ruta
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaVertice import RespuestaVertice
from Backend.Dominio.Interfaces.IntMapeadores.IMapeadorDominioDTO import IMapeadorDominioDTO
import logging

class MapeadorRuta(IMapeadorDominioDTO):
    """
    Clase para mapear objetos Ruta del dominio a DTOs de respuesta.
    """
    @staticmethod
    def a_dto(ruta: Ruta) -> RespuestaRuta:
        logger = logging.getLogger("MapeadorRuta")
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(f"[MapeadorRuta.a_dto] Mapeando ruta: {ruta}")
        def vertice_a_vertice(v):
            elem = v.elemento() if hasattr(v, 'elemento') else v
            vertice = RespuestaVertice(
                id=getattr(elem, 'id_cliente', getattr(elem, 'id_almacenamiento', getattr(elem, 'id_recarga', 0))),
                tipo=getattr(elem, 'tipo_elemento', ''),
                nombre=getattr(elem, 'nombre', '')
            )
            logger.info(f"[MapeadorRuta.a_dto] vertice mapeado: {vertice}")
            return vertice
        origen = vertice_a_vertice(getattr(ruta, 'origen', None)) if getattr(ruta, 'origen', None) is not None else None
        destino = vertice_a_vertice(getattr(ruta, 'destino', None)) if getattr(ruta, 'destino', None) is not None else None
        camino = [vertice_a_vertice(v) for v in getattr(ruta, 'camino', []) if v is not None]
        dto = RespuestaRuta(
            origen=origen,
            destino=destino,
            camino=camino,
            peso_total=float(getattr(ruta, 'peso_total', 0.0)),
            algoritmo=str(getattr(ruta, 'algoritmo', '')),
            tiempo_calculo=float(getattr(ruta, 'tiempo_calculo', 0.0)) if getattr(ruta, 'tiempo_calculo', None) is not None else None
        )
        logger.info(f"[MapeadorRuta.a_dto] DTO de ruta creado: {dto}")
        return dto
