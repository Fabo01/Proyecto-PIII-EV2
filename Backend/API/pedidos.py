from fastapi import APIRouter, HTTPException
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.Dtos1 import PedidoResponse, RutaResponse
from typing import List
import logging

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

logger = logging.getLogger("API.Pedidos")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos():
    logger.info("GET /pedidos llamado")
    pedidos = SimulacionAplicacionService.listar_pedidos()
    logger.info(f"GET /pedidos retornó {len(pedidos)} pedidos")
    if pedidos is None:
        logger.warning("GET /pedidos: Simulación no iniciada")
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not pedidos:
        logger.warning("GET /pedidos: No hay pedidos registrados")
        raise HTTPException(status_code=404, detail="No hay pedidos registrados")
    return pedidos

@router.get("/errores", response_model=List[dict])
def listar_errores_pedidos():
    logger.info("GET /pedidos/errores llamado")
    try:
        errores = SimulacionAplicacionService.obtener_errores_pedidos()
        logger.info(f"GET /pedidos/errores retornó {len(errores)} errores")
        return errores or []
    except Exception as e:
        logger.error(f"GET /pedidos/errores error: {e}")
        raise HTTPException(status_code=400, detail="Simulación no iniciada o sin errores registrados")

@router.post("/{id}/ruta", response_model=RutaResponse)
def calcular_ruta_pedido(id: int, algoritmo: str = 'dijkstra'):
    logger.info(f"POST /pedidos/{id}/ruta llamado con algoritmo={algoritmo}")
    try:
        ruta = SimulacionAplicacionService.calcular_ruta_pedido(id, algoritmo)
        if ruta is None:
            logger.warning(f"POST /pedidos/{id}/ruta: Ruta no encontrada para el pedido")
            raise HTTPException(status_code=404, detail="Ruta no encontrada para el pedido")
        return ruta
    except KeyError as e:
        logger.warning(f"POST /pedidos/{id}/ruta: Pedido no encontrado {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        mensaje = str(e)
        logger.error(f"POST /pedidos/{id}/ruta: Error inesperado: {mensaje}")
        if "No existe una ruta posible" in mensaje:
            raise HTTPException(status_code=422, detail=mensaje)
        if "Algoritmo de ruta no soportado" in mensaje:
            raise HTTPException(status_code=422, detail=mensaje)
        raise HTTPException(status_code=500, detail=mensaje)

@router.get("/{id}", response_model=PedidoResponse)
def obtener_pedido(id: int):
    logger.info(f"GET /pedidos/{id} llamado")
    try:
        pedido = SimulacionAplicacionService.obtener_pedido(id)
        if pedido is None:
            logger.warning(f"GET /pedidos/{id}: Pedido no encontrado")
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido
    except Exception as e:
        logger.error(f"GET /pedidos/{id}: Error inesperado: {e}")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

@router.get("/en_almacen/{id_almacen}", response_model=List[PedidoResponse])
def pedidos_en_almacen(id_almacen: int):
    """
    Devuelve todos los pedidos asociados a un almacenamiento específico.
    """
    pedidos = SimulacionAplicacionService.listar_pedidos()
    pedidos_filtrados = [p for p in pedidos if getattr(p, 'id_almacenamiento', None) == id_almacen]
    if not pedidos_filtrados:
        raise HTTPException(status_code=404, detail="No hay pedidos en el almacenamiento indicado")
    return pedidos_filtrados


