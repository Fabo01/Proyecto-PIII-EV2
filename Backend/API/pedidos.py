from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaPedido import RespuestaPedido
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.Infraestructura.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.Infraestructura.Mapeadores.MapeadorRuta import MapeadorRuta
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

def get_simulacion_service():
    return SimulacionAplicacionService

@router.get("/", response_model=List[RespuestaPedido])
def listar_pedidos(service=Depends(get_simulacion_service)):
    # Inicio de auditoría y listado sobre objetos de dominio
    logger.info("GET /pedidos llamado")
    try:
        from Backend.Dominio.Simulacion_dominio import Simulacion
        sim = Simulacion.obtener_instancia()
    except Exception as e:
        logger.error(f"GET /pedidos: simulación no iniciada o no accesible: {e}")
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    pedidos_raw = getattr(sim, 'pedidos', [])
    logger.info(f"listar_pedidos: {len(pedidos_raw)} pedidos en dominio encontrados")
    pedidos_validos = []
    pedidos_descartados = []
    # Auditoría de cada pedido de dominio
    for pedido in pedidos_raw:
        logger.info(f"Auditoría Pedido dominio: id={pedido.id_pedido}, atributos={vars(pedido)}")
        origen_dom = pedido.obtener_origen()
        destino_dom = pedido.obtener_destino()
        logger.info(f"  Origen dominio: {origen_dom}, Destino dominio: {destino_dom}")
        # Estado y metadatos
        logger.info(f"  Estado dominio: status={pedido.status}, prioridad={pedido.prioridad}, fecha_creacion={pedido.fecha_creacion}, fecha_entrega={pedido.fecha_entrega}")
        if origen_dom and destino_dom:
            pedidos_validos.append(pedido)
        else:
            logger.warning(f"Pedido {pedido.id_pedido} descartado por origen/destino None: origen={origen_dom}, destino={destino_dom}")
            pedidos_descartados.append(pedido)
    if pedidos_descartados:
        for pd in pedidos_descartados:
            sim.registrar_error_pedido(id_pedido=pd.id_pedido,
                                      motivo="Pedido incompleto origen/destino None",
                                      datos=vars(pd))
    if not pedidos_validos:
        logger.warning("GET /pedidos: No hay pedidos completos registrados")
        return []
    # Serializar pedidos válidos
    try:
        resultados = [MapeadorPedido.a_dto(p) for p in pedidos_validos]
        logger.info(f"GET /pedidos: {len(resultados)} pedidos serializados correctamente")
        return resultados
    except Exception as e:
        logger.error(f"Error al mapear pedidos a DTO: {e}")
        raise HTTPException(status_code=500, detail=f"Error al mapear pedidos: {e}")

@router.get("/errores", response_model=List[dict])
def listar_errores_pedidos(service=Depends(get_simulacion_service)):
    logger.info("GET /pedidos/errores llamado")
    try:
        errores_raw = service.obtener_errores_pedidos()
        logger.info(f"GET /pedidos/errores retornó {len(errores_raw) if errores_raw else 0} errores")
        # Mapear errores a formato serializable
        errores = []
        for err in errores_raw or []:
            cliente_obj = err.get('cliente')
            almacen_obj = err.get('almacen')
            errores.append({
                'id_pedido': err.get('id_pedido'),
                'error': err.get('error'),
                'id_cliente': getattr(cliente_obj.elemento(), 'id_cliente', None) if cliente_obj else None,
                'id_almacenamiento': getattr(almacen_obj.elemento(), 'id_almacenamiento', None) if almacen_obj else None,
                'fecha': str(err.get('fecha')),
                'prioridad': err.get('prioridad')
            })
        return errores
    except Exception as e:
        logger.error(f"GET /pedidos/errores error: {e}")
        raise HTTPException(status_code=400, detail="Simulación no iniciada o sin errores registrados")

@router.post("/{id}/ruta", response_model=RespuestaRuta)
def calcular_ruta_pedido(id: int, algoritmo: str = 'dijkstra', service=Depends(get_simulacion_service)):
    logger.info(f"POST /pedidos/{id}/ruta llamado con algoritmo={algoritmo}")
    try:
        ruta = service.calcular_ruta_pedido(id, algoritmo)
        if ruta is None:
            logger.warning(f"POST /pedidos/{id}/ruta: Ruta no encontrada para el pedido")
            raise HTTPException(status_code=404, detail="Ruta no encontrada para el pedido")
        return MapeadorRuta.a_dto(ruta)
    except KeyError as e:
        logger.warning(f"POST /pedidos/{id}/ruta: Pedido no encontrado {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        mensaje = str(e)
        logger.error(f"POST /pedidos/{id}/ruta: Error inesperado: {mensaje}")
        if "No existe una ruta posible" in mensaje:
            raise HTTPException(status_code=422, detail=mensaje)
        raise HTTPException(status_code=500, detail=mensaje)

@router.get("/{id}", response_model=RespuestaPedido)
def obtener_pedido(id: int):
    """
    Devuelve un pedido por su id, usando el servicio y mapeador.
    """
    try:
        pedido = SimulacionAplicacionService.obtener_pedido(id)
        if pedido is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return MapeadorPedido.a_dto(pedido)
    except Exception:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

@router.get("/en_almacen/{id_almacen}", response_model=List[RespuestaPedido])
def pedidos_en_almacen(id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve los pedidos cuyo almacenamiento de origen es el dado.
    """
    pedidos = service.listar_pedidos()
    pedidos_filtrados = []
    for p in pedidos or []:
        try:
            origen = p.obtener_origen()
        except Exception:
            continue
        if origen and getattr(origen, 'id_almacenamiento', None) == id_almacen:
            pedidos_filtrados.append(p)
    # Mapear a DTOs
    return [MapeadorPedido.a_dto(p) for p in pedidos_filtrados]

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_pedidos_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de pedidos (ID → Objeto Pedido serializable).
    """
    hashmap = service.obtener_pedidos_hashmap()
    hashmap_dto = {str(k): MapeadorPedido.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)


