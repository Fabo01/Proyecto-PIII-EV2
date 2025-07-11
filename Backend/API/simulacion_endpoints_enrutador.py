from fastapi import APIRouter, HTTPException, Depends, Body, Query
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionInit import RespuestaSimulacionInit
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from Backend.API.DTOs.DTOsRespuesta.RespuestaSnapshot import RespuestaSnapshot
from Backend.API.Mapeadores.MapeadorSimulacion import MapeadorSimulacion
from Backend.API.Mapeadores.MapeadorSnapshot import MapeadorSnapshot
from Backend.API.Mapeadores.MapeadorCliente import MapeadorCliente
from Backend.API.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
from Backend.API.Mapeadores.MapeadorRecarga import MapeadorRecarga
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice
from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from typing import Dict, Any
import time
import logging

# Variables globales para rastrear el estado de la simulación
simulacion_activa = False
estado_simulacion_global = None

router = APIRouter(prefix="/simulacion", tags=["Simulacion"])

# Configurar logging básico
logging.basicConfig(level=logging.INFO)

# Configuración de logger para este módulo
logger = logging.getLogger("API.Simulacion")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_simulacion_service():
    """
    Proveedor de la instancia del servicio de aplicación de simulación.
    """
    return SimulacionAplicacionService()

@router.post(
    "/iniciar", 
    response_model=RespuestaSimulacionEstado,
    summary="Inicializar Nueva Simulación",
    description="""
    **Crea e inicializa una nueva simulación logística de drones**
    
    Este endpoint genera una red completa con vértices, aristas y pedidos aleatorios
    según los parámetros especificados.
    
    ### Parámetros:
    - **n_vertices**: Número total de vértices (10-150)
        - 60% serán clientes 
        - 20% serán almacenamientos
        - 20% serán estaciones de recarga
    - **m_aristas**: Número de aristas/conexiones (mín: n_vertices-1 para conectividad)
    - **n_pedidos**: Número de pedidos a generar (10-500)
    
    ### Validaciones:
    - El grafo generado será siempre conexo
    - Las aristas tendrán pesos aleatorios (1-15 unidades)
    - Los pedidos se asignan aleatoriamente entre almacenamientos y clientes
    
    ### Respuesta:
    Estado completo de la simulación con todas las entidades creadas
    """,
    responses={
        200: {"description": "Simulación inicializada exitosamente"},
        400: {"description": "Parámetros inválidos"},
        500: {"description": "Error interno del servidor"}
    }
)
def iniciar_simulacion(
    request: RespuestaSimulacionInit = Body(
        ...,
        example={
            "n_vertices": 15,
            "m_aristas": 20, 
            "n_pedidos": 10
        }
    ),
    service=Depends(get_simulacion_service)
) -> RespuestaSimulacionEstado:
    """
    Inicia una nueva simulación con los parámetros dados y la registra como activa.
    """
    try:
        # Log de los parámetros recibidos
        logging.info(f"Parámetros recibidos en /simulacion/iniciar: n_vertices={request.n_vertices}, m_aristas={request.m_aristas}, n_pedidos={request.n_pedidos}")
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para iniciar la simulación")
        estado = service.iniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
        # Marcar simulación como activa y guardar estado
        global simulacion_activa, estado_simulacion_global
        simulacion_activa = True
        estado_simulacion_global = estado
        t1 = time.time()
        if not estado:
            raise HTTPException(status_code=400, detail="No se pudo iniciar la simulación")
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return MapeadorSimulacion.a_dto_estado(estado)
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log de error detallado
        logging.error(f"Error en /simulacion/iniciar: {str(e)} | Parámetros: n_vertices={getattr(request, 'n_vertices', None)}, m_aristas={getattr(request, 'm_aristas', None)}, n_pedidos={getattr(request, 'n_pedidos', None)}")
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/reiniciar", response_model=RespuestaSimulacionEstado)
def reiniciar_simulacion(request: RespuestaSimulacionInit, service=Depends(get_simulacion_service)):
    """
    Reinicia la simulación con nuevos parámetros.
    """
    try:
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para reiniciar la simulación")
        estado = service.reiniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        if not estado:
            raise HTTPException(status_code=400, detail="No se pudo reiniciar la simulación")
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return MapeadorSimulacion.a_dto_estado(estado)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/estado", response_model=RespuestaSimulacionEstado)
def estado_simulacion(service=Depends(get_simulacion_service)):
    """
    Devuelve el estado actual de la simulación (recalculado).
    """
    if not simulacion_activa:
        raise HTTPException(status_code=404, detail="No hay simulación activa.")
    try:
        t0 = time.time()
        estado = service.estado_actual()
        t1 = time.time()
        if not estado:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return MapeadorSimulacion.a_dto_estado(estado)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/set_estrategia/{nombre}", response_model=dict)
def set_estrategia(nombre: str, service=Depends(get_simulacion_service)):
    """
    Cambia la estrategia de rutas de la simulación (bfs, dfs, dijkstra, etc).
    """
    try:
        resultado = service.set_estrategia_ruta(nombre)
        if not resultado:
            raise HTTPException(status_code=400, detail="No se pudo cambiar la estrategia de rutas")
        return {"mensaje": f"Estrategia de rutas cambiada a {nombre}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al cambiar estrategia: {str(e)}")

@router.post("/notificar_evento", response_model=dict)
def notificar_evento(evento: str, datos: dict = None, service=Depends(get_simulacion_service)):
    """
    Notifica un evento a los observadores de la simulación.
    """
    try:
        resultado = service.notificar_evento(evento, datos)
        if not resultado:
            raise HTTPException(status_code=400, detail="No se pudo notificar el evento")
        return {"mensaje": f"Evento '{evento}' notificado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al notificar evento: {str(e)}")

@router.post("/reiniciar_todo", response_model=dict)
def reiniciar_todo(service=Depends(get_simulacion_service)):
    """
    Reinicia completamente la simulación y todos los datos.
    """
    try:
        resultado = service.reiniciar_todo()
        if not resultado:
            raise HTTPException(status_code=400, detail="No se pudo reiniciar todo el sistema")
        return {"mensaje": "Simulación y datos reiniciados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al reiniciar todo: {str(e)}")

@router.get("/algoritmos", response_model=list)
def obtener_algoritmos(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de algoritmos de ruta disponibles en el sistema.
    """
    return service.obtener_algoritmos()

@router.get("/snapshot", response_model=RespuestaSnapshot)
def obtener_snapshot(tipo: str, service=Depends(get_simulacion_service)):
    """
    Devuelve el snapshot serializado del grafo según el tipo ('n-1' o 'm_aristas').
    Incluye logs detallados para debugging y manejo de errores robusto.
    """
    logger.info(f"[SNAPSHOT] Ingreso a endpoint /simulacion/snapshot con tipo='{tipo}'")
    logger.debug(f"[SNAPSHOT] Parámetros: tipo={tipo}")
    try:
        snapshot_bruto = service.obtener_snapshot(tipo)
        logger.info(f"[SNAPSHOT] Snapshot bruto recibido: {snapshot_bruto}")
        if not snapshot_bruto or not snapshot_bruto.get('vertices') or not snapshot_bruto.get('aristas'):
            logger.warning(f"[SNAPSHOT] Snapshot inválido o vacío para tipo '{tipo}'")
            raise HTTPException(status_code=404, detail={
                "mensaje": f"No existe snapshot tipo '{tipo}'",
                "detalle": snapshot_bruto
            })
        # Valid snapshot structure
        logger.info(f"[SNAPSHOT] Snapshot válido. Vértices: {len(snapshot_bruto['vertices'])}, Aristas: {len(snapshot_bruto['aristas'])}")
        return snapshot_bruto
    except HTTPException as e:
        logger.error(f"[SNAPSHOT] HTTPException lanzada: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("[SNAPSHOT] Error inesperado al procesar snapshot")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clientes/hashmap", response_model=RespuestaHashMap)
def clientes_hashmap(service=Depends(get_simulacion_service)):
    clientes = service.obtener_clientes()
    hashmap = {str(c.id_cliente): MapeadorCliente.a_hashmap(c) for c in clientes}
    return {"hashmap": hashmap}

@router.get("/almacenamientos/hashmap", response_model=RespuestaHashMap)
def almacenamientos_hashmap(service=Depends(get_simulacion_service)):
    almacenamientos = service.obtener_almacenamientos()
    hashmap = {str(a.id_almacenamiento): MapeadorAlmacenamiento.a_hashmap(a) for a in almacenamientos}
    return {"hashmap": hashmap}

@router.get("/pedidos/hashmap", response_model=RespuestaHashMap)
def pedidos_hashmap(service=Depends(get_simulacion_service)):
    pedidos = service.obtener_pedidos()
    hashmap = {str(p.id_pedido): MapeadorPedido.a_hashmap(p) for p in pedidos}
    return {"hashmap": hashmap}

@router.get("/recargas/hashmap", response_model=RespuestaHashMap)
def recargas_hashmap(service=Depends(get_simulacion_service)):
    recargas = service.obtener_recargas()
    hashmap = {str(r.id_recarga): MapeadorRecarga.a_hashmap(r) for r in recargas}
    return {"hashmap": hashmap}

@router.get("/rutas/hashmap", response_model=RespuestaHashMap)
def rutas_hashmap(service=Depends(get_simulacion_service)):
    rutas = service.obtener_rutas()
    from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
    return {getattr(r, 'id_ruta', i): MapeadorRuta.a_hashmap(r) for i, r in enumerate(rutas)}

@router.get("/vertices/hashmap", response_model=RespuestaHashMap)
def vertices_hashmap(service=Depends(get_simulacion_service)):
    vertices = service.obtener_vertices()
    from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice
    return {getattr(v, 'id_elemento', lambda: i)() if hasattr(v, 'id_elemento') else i: MapeadorVertice.a_hashmap(v) for i, v in enumerate(vertices)}

@router.get("/aristas/hashmap", response_model=RespuestaHashMap)
def aristas_hashmap(service=Depends(get_simulacion_service)):
    aristas = service.obtener_aristas()
    from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
    return {f"({getattr(a.origen.elemento, 'id_cliente', getattr(a.origen.elemento, 'id_almacenamiento', getattr(a.origen.elemento, 'id_recarga', 0)))}, {getattr(a.destino.elemento, 'id_cliente', getattr(a.destino.elemento, 'id_almacenamiento', getattr(a.destino.elemento, 'id_recarga', 0)))})": MapeadorArista.a_hashmap(a) for a in aristas}

@router.get("/clientes", response_model=list)
def listar_clientes(service=Depends(get_simulacion_service)):
    clientes = service.obtener_clientes()
    return [MapeadorCliente.a_dto(c, incluir_pedidos=False) for c in clientes]

@router.get("/almacenamientos", response_model=list)
def listar_almacenamientos(service=Depends(get_simulacion_service)):
    almacenamientos = service.obtener_almacenamientos()
    return [MapeadorAlmacenamiento.a_dto(a, incluir_pedidos=False) for a in almacenamientos]

@router.get("/pedidos", response_model=list)
def listar_pedidos(service=Depends(get_simulacion_service)):
    pedidos = service.obtener_pedidos()
    return [MapeadorPedido.a_dto(p, incluir_cliente=False, incluir_almacenamiento=False) for p in pedidos]

@router.get("/recargas", response_model=list)
def listar_recargas(service=Depends(get_simulacion_service)):
    recargas = service.obtener_recargas()
    return [MapeadorRecarga.a_dto(r) for r in recargas]

@router.get("/rutas", response_model=list)
def listar_rutas(service=Depends(get_simulacion_service)):
    rutas = service.obtener_rutas()
    from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
    return [MapeadorRuta.a_dto(r) for r in rutas]

@router.get("/vertices", response_model=list)
def listar_vertices(service=Depends(get_simulacion_service)):
    vertices = service.obtener_vertices()
    from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice
    return [MapeadorVertice.a_dto(v) for v in vertices]

@router.get("/aristas", response_model=list)
def listar_aristas(service=Depends(get_simulacion_service)):
    aristas = service.obtener_aristas()
    return [MapeadorArista.a_dto(a) for a in aristas]

# Alias para compatibilidad con UI: /info
@router.get("/info", response_model=RespuestaSimulacionEstado)
def info_simulacion():
    """
    Devuelve el estado de la simulación activa.
    """
    if not simulacion_activa or estado_simulacion_global is None:
        raise HTTPException(status_code=404, detail="No hay simulación activa.")
    # Retornar el estado global mapeado a DTO
    return MapeadorSimulacion.a_dto_estado(estado_simulacion_global)
