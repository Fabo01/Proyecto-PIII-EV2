from fastapi import APIRouter, HTTPException, Depends, Response, Path, Query, Body
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta, RespuestaMultiplesRutas
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
from typing import List, Optional, Dict, Any
from Backend.API.DTOs.DTOsRespuesta.RespuestaFloydWarshall import RespuestaFloydWarshall
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap

import logging

router = APIRouter(
    prefix="/rutas", 
    tags=["Rutas"],
    responses={
        404: {"description": "Recurso no encontrado"},
        400: {"description": "Solicitud inválida"},
        500: {"description": "Error interno del servidor"}
    }
)

def get_simulacion_service():
    return SimulacionAplicacionService()

# Configuración del logger
logger = logging.getLogger("API.Rutas")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

@router.get("/", response_model=List[RespuestaRuta])
def listar_rutas(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de rutas registradas en la simulación.
    """
    logger.info("GET /rutas llamado")
    rutas = service.listar_rutas()
    logger.info(f"GET /rutas retornó {len(rutas) if rutas else 0} rutas")
    if rutas is None:
        logger.warning("GET /rutas: Simulación no iniciada")
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    try:
        rutas_dto = MapeadorRuta.lista_a_dto(rutas) if rutas else []
        logger.info(f"GET /rutas: {len(rutas_dto)} rutas serializadas correctamente")
        return rutas_dto
    except Exception as e:
        logger.error(f"GET /rutas: Error de mapeo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")
    
@router.get("/hashmap", response_model=RespuestaHashMap)
def rutas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de rutas (objetos reales para debug).
    """
    logger.info("GET /rutas/hashmap llamado")
    try:
        hashmap = service.obtener_rutas_hashmap() or {}
        return {"rutas": hashmap}
    except Exception as e:
        logger.error(f"GET /rutas/hashmap: Error obteniendo hashmap de rutas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo hashmap de rutas: {str(e)}")

@router.get("/{id}", response_model=RespuestaRuta)
def obtener_ruta(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una ruta por su id (DTO plano).
    """
    logger.info(f"GET /rutas/{id} llamado")
    try:
        ruta = service.obtener_ruta(id)
        if ruta is None:
            logger.warning(f"GET /rutas/{id}: Ruta no encontrada")
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        logger.info(f"GET /rutas/{id}: Ruta encontrada y serializada")
        return MapeadorRuta.a_dto(ruta)
    except Exception as e:
        logger.error(f"GET /rutas/{id}: Ruta no encontrada: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Ruta no encontrada: {str(e)}")

@router.get("/hashmap/{id}", response_model=dict)
def obtener_ruta_hashmap(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una ruta por su id (objeto real para debug).
    """
    logger.info(f"GET /rutas/hashmap/{id} llamado")
    try:
        ruta = service.obtener_ruta(id)
        if ruta is None:
            logger.warning(f"GET /rutas/hashmap/{id}: Ruta no encontrada")
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        logger.info(f"GET /rutas/hashmap/{id}: Ruta encontrada")
        return {"ruta": MapeadorRuta.a_hashmap(ruta)}
    except Exception as e:
        logger.error(f"GET /rutas/hashmap/{id}: Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Ruta no encontrada: {str(e)}")

@router.get("/por_almacen/{id_almacen}", response_model=List[RespuestaRuta])
def rutas_por_almacen(id_almacen: int, service=Depends(get_simulacion_service)):
    """
    Devuelve las rutas que tienen como origen el almacenamiento indicado.
    """
    logger.info(f"GET /rutas/por_almacen/{id_almacen} llamado")
    rutas = service.listar_rutas()
    rutas_filtradas = [r for r in rutas if hasattr(r, 'origen') and getattr(r.origen, 'id_almacenamiento', None) == id_almacen]
    logger.info(f"GET /rutas/por_almacen/{id_almacen}: {len(rutas_filtradas)} rutas encontradas")
    if not rutas_filtradas:
        logger.warning(f"GET /rutas/por_almacen/{id_almacen}: No hay rutas desde el almacenamiento indicado")
        raise HTTPException(status_code=404, detail="No hay rutas desde el almacenamiento indicado")
    try:
        rutas_dto = [MapeadorRuta.a_dto(r) for r in rutas_filtradas]
        logger.info(f"GET /rutas/por_almacen/{id_almacen}: {len(rutas_dto)} rutas serializadas correctamente")
        return rutas_dto
    except Exception as e:
        logger.error(f"GET /rutas/por_almacen/{id_almacen}: Error de mapeo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/arbol_expansion_minima")
def obtener_arbol_expansion_minima(service=Depends(get_simulacion_service)):
    """
    Devuelve el arbol de expansion minima del grafo.
    """
    logger.info("GET /rutas/arbol_expansion_minima llamado")
    resultado = service.obtener_arbol_expansion_minima()
    logger.info(f"GET /rutas/arbol_expansion_minima: Árbol calculado y serializado correctamente")
    return resultado

@router.get("/por_algoritmo/{algoritmo}", response_model=List[RespuestaRuta])
def rutas_por_algoritmo(algoritmo: str, service=Depends(get_simulacion_service)):
    """
    Devuelve todas las rutas calculadas con un algoritmo específico.
    """
    logger.info(f"GET /rutas/por_algoritmo/{algoritmo} llamado")
    try:
        rutas = service.listar_rutas()
        rutas_filtradas = [r for r in rutas if getattr(r, 'algoritmo', None) == algoritmo]
        if not rutas_filtradas:
            logger.warning(f"GET /rutas/por_algoritmo/{algoritmo}: No hay rutas para el algoritmo indicado")
            raise HTTPException(status_code=404, detail="No hay rutas para el algoritmo indicado")
        rutas_dto = [MapeadorRuta.a_dto(r) for r in rutas_filtradas]
        logger.info(f"GET /rutas/por_algoritmo/{algoritmo}: {len(rutas_dto)} rutas serializadas correctamente")
        return rutas_dto
    except Exception as e:
        logger.error(f"GET /rutas/por_algoritmo/{algoritmo}: Error de mapeo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/por_pedido/{id_pedido}", response_model=List[RespuestaRuta])
def rutas_por_pedido(id_pedido: int, service=Depends(get_simulacion_service)):
    """
    Devuelve todas las rutas calculadas para un pedido específico.
    """
    logger.info(f"GET /rutas/por_pedido/{id_pedido} llamado")
    try:
        rutas = service.listar_rutas()
        rutas_filtradas = [r for r in rutas if getattr(r, 'id_pedido', None) == id_pedido]
        if not rutas_filtradas:
            logger.warning(f"GET /rutas/por_pedido/{id_pedido}: No hay rutas para el pedido indicado")
            raise HTTPException(status_code=404, detail="No hay rutas para el pedido indicado")
        rutas_dto = [MapeadorRuta.a_dto(r) for r in rutas_filtradas]
        logger.info(f"GET /rutas/por_pedido/{id_pedido}: {len(rutas_dto)} rutas serializadas correctamente")
        return rutas_dto
    except Exception as e:
        logger.error(f"GET /rutas/por_pedido/{id_pedido}: Error de mapeo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

# Calcular ruta individual con algoritmo específico
@router.post(
    "/calcular/{id_pedido}/{algoritmo}", 
    response_model=RespuestaRuta,
    summary="Calcular Ruta Individual",
    description="""
    **Calcula la ruta óptima para un pedido específico usando un algoritmo determinado**
    
    ### Algoritmos disponibles:
    - **bfs**: Búsqueda en Amplitud - Encuentra camino más corto en términos de número de saltos
    - **dfs**: Búsqueda en Profundidad - Explora caminos en profundidad
    - **dijkstra**: Camino más corto ponderado - Considera pesos de aristas
    - **floydwarshall**: Todos los caminos más cortos - Algoritmo global optimizado
    - **topologicalsort**: Ordenamiento topológico - Para grafos dirigidos acíclicos
    
    ### Validaciones:
    - El pedido debe existir y no estar marcado como entregado
    - Verifica autonomía del drone (máximo 50 unidades)
    - Si la ruta excede la autonomía, busca estaciones de recarga
    
    ### Respuesta:
    Ruta calculada con camino, peso total, tiempo de cálculo y estadísticas
    """,
    responses={
        200: {"description": "Ruta calculada exitosamente"},
        400: {"description": "Pedido ya entregado o parámetros inválidos"},
        404: {"description": "Pedido no encontrado"},
        422: {"description": "No se pudo calcular ruta válida"}
    }
)
def calcular_ruta(
    id_pedido: int = Path(..., description="ID único del pedido", example=1),
    algoritmo: str = Path(..., description="Algoritmo de ruteo a utilizar", example="dijkstra"),
    service=Depends(get_simulacion_service)
) -> RespuestaRuta:
    """
    Calcula la ruta para un pedido con un algoritmo específico.
    """
    logger.info(f"POST /rutas/calcular/{id_pedido}/{algoritmo} llamado")
    try:
        ruta = service.calcular_ruta(id_pedido, algoritmo)
        from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
        logger.info(f"POST /rutas/calcular/{id_pedido}/{algoritmo}: Ruta calculada correctamente")
        return MapeadorRuta.a_dto(ruta)
    except Exception as e:
        logger.error(f"POST /rutas/calcular/{id_pedido}/{algoritmo}: Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Calcular todas las rutas para un pedido con todos los algoritmos
@router.post("/calcular/{id_pedido}/todos", response_model=RespuestaMultiplesRutas)
def calcular_rutas_todos(id_pedido: int, service=Depends(get_simulacion_service)):
    """
    Calcula rutas para un pedido usando todos los algoritmos disponibles.
    """
    logger.info(f"POST /rutas/calcular/{id_pedido}/todos llamado")
    try:
        rutas_dict = service.calcular_ruta_todos(id_pedido)
        from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
        logger.info(f"POST /rutas/calcular/{id_pedido}/todos: Rutas calculadas correctamente")
        return MapeadorRuta.rutas_multiples_a_dto(rutas_dict, id_pedido)
    except Exception as e:
        logger.error(f"POST /rutas/calcular/{id_pedido}/todos: Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Calcular rutas usando Floyd-Warshall para todos los pedidos
@router.post("/floydwarshall_pedidos", response_model=List[RespuestaRuta])
def floydwarshall_pedidos(service=Depends(get_simulacion_service)):
    """
    Calcula rutas óptimas para todos los pedidos usando Floyd-Warshall.
    """
    logger.info("POST /rutas/floydwarshall_pedidos llamado")
    try:
        rutas = service.floydwarshall_para_todos_los_pedidos()
        from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
        logger.info("POST /rutas/floydwarshall_pedidos: Rutas calculadas correctamente")
        return MapeadorRuta.lista_a_dto(rutas)
    except Exception as e:
        logger.error(f"POST /rutas/floydwarshall_pedidos: Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Marcar pedido como entregado
@router.post(
    "/entregar/{id_pedido}", 
    response_model=Dict[str, Any],
    summary="Marcar Pedido como Entregado",
    description="""
    **Marca un pedido como completado/entregado exitosamente**
    
    Este endpoint actualiza el estado del pedido a 'entregado' y registra
    la fecha y hora de entrega. Una vez marcado como entregado:
    
    ### Efectos:
    - ✅ El pedido queda marcado como 'entregado'
    - ✅ Se registra timestamp de entrega
    - ❌ **No se pueden calcular más rutas** para este pedido
    - ✅ Se actualiza en todas las estadísticas del sistema
    - ✅ Queda registrado en el historial de entregas
    
    ### Validaciones:
    - El pedido debe existir en el sistema
    - El pedido no debe estar ya marcado como entregado
    - Debe tener una ruta asignada previamente
    
    ### Uso típico:
    Se llama después de que el drone ha completado exitosamente la entrega del pedido al cliente.
    """,
    responses={
        200: {"description": "Pedido marcado como entregado exitosamente"},
        400: {"description": "Pedido ya entregado o sin ruta asignada"},
        404: {"description": "Pedido no encontrado"}
    }
)
def entregar_pedido(
    id_pedido: int = Path(..., description="ID único del pedido a marcar como entregado", example=1),
    service=Depends(get_simulacion_service)
) -> Dict[str, Any]:
    """
    Marca el pedido como entregado.
    """
    logger.info(f"POST /rutas/entregar/{id_pedido} llamado")
    try:
        pedido = service.entregar_pedido(id_pedido)
        from Backend.API.Mapeadores.MapeadorPedido import MapeadorPedido
        logger.info(f"POST /rutas/entregar/{id_pedido}: Pedido marcado como entregado")
        return MapeadorPedido.a_dto(pedido)
    except Exception as e:
        logger.error(f"POST /rutas/entregar/{id_pedido}: Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Calcular Árbol de Expansión Mínima usando Kruskal
@router.get("/mst/kruskal")
def calcular_mst_kruskal(service=Depends(get_simulacion_service)):
    """
    Calcula el Árbol de Expansión Mínima (MST) usando el algoritmo de Kruskal.
    Retorna las aristas del MST y el peso total.
    """
    logger.info("GET /rutas/mst/kruskal llamado")
    try:
        mst_data = service.calcular_mst_kruskal()
        logger.info("GET /rutas/mst/kruskal: MST calculado correctamente")
        return mst_data
    except Exception as e:
        logger.error(f"GET /rutas/mst/kruskal: Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))