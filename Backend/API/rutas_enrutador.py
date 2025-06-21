from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaRuta import RespuestaRuta
from Backend.API.DTOs.DTOsRespuesta.RespuestaFloydWarshall import RespuestaFloydWarshall
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
from typing import List
import logging

router = APIRouter(prefix="/rutas", tags=["Rutas"])

def get_simulacion_service():
    return SimulacionAplicacionService

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
    logger.info("GET /rutas llamado")
    rutas = service.listar_rutas()
    logger.info(f"GET /rutas retornó {len(rutas) if rutas else 0} rutas")
    if rutas is None:
        logger.warning("GET /rutas: Simulación no iniciada")
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    try:
        rutas_dto = [MapeadorRuta.a_dto(r) for r in rutas] if rutas else []
        logger.info(f"GET /rutas: {len(rutas_dto)} rutas serializadas correctamente")
        return rutas_dto
    except Exception as e:
        logger.error(f"GET /rutas: Error de mapeo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/{id}", response_model=RespuestaRuta)
def obtener_ruta(id: int, service=Depends(get_simulacion_service)):
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

@router.get("/por_almacen/{id_almacen}", response_model=List[RespuestaRuta])
def rutas_por_almacen(id_almacen: int, service=Depends(get_simulacion_service)):
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

@router.get("/floyd_warshall", response_model=RespuestaFloydWarshall)
def floyd_warshall_todos_los_caminos(service=Depends(get_simulacion_service)):
    logger.info("GET /rutas/floyd_warshall llamado")
    try:
        resultado = service.obtener_todos_los_caminos_floyd_warshall()
        logger.info("GET /rutas/floyd_warshall: Caminos calculados y serializados correctamente")
        return resultado
    except Exception as e:
        logger.error(f"GET /rutas/floyd_warshall: Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comparar_tiempos/{id_pedido}")
def comparar_tiempos_algoritmos(id_pedido: int, service=Depends(get_simulacion_service)):
    logger.info(f"GET /rutas/comparar_tiempos/{id_pedido} llamado")
    resultado = service.comparar_tiempos_algoritmos(id_pedido)
    logger.info(f"GET /rutas/comparar_tiempos/{id_pedido}: Resultado: {resultado}")
    return resultado

@router.get("/arbol_expansion_minima")
def obtener_arbol_expansion_minima(service=Depends(get_simulacion_service)):
    logger.info("GET /rutas/arbol_expansion_minima llamado")
    resultado = service.obtener_arbol_expansion_minima()
    logger.info(f"GET /rutas/arbol_expansion_minima: Árbol calculado y serializado correctamente")
    return resultado

@router.get("/camino")
def calcular_camino_entre_vertices(origen: int, destino: int, algoritmo: str = 'dijkstra', id_pedido: int = None, service=Depends(get_simulacion_service)):
    logger.info(f"[API] /rutas/camino llamado con origen={origen} (type: {type(origen)}), destino={destino} (type: {type(destino)}), algoritmo={algoritmo} (type: {type(algoritmo)}), id_pedido={id_pedido}")
    sim = service._dominio_service
    try:
        grafo = sim.obtener_vertices()  # Solo para validar existencia
        logger.info(f"[API] Grafo cargado con {len(grafo)} vertices")
    except Exception as e:
        logger.error(f"[API] Error al obtener grafo: {e}")
        raise HTTPException(status_code=500, detail="No se pudo cargar el grafo")
    # Conversión robusta de ids a vértices
    try:
        repositorio_vertices = sim.obtener_instancia().grafo._repositorio_vertices
        logger.info(f"[API] RepositorioVertices contiene: {[v for v in repositorio_vertices.todos()]}")
        vertice_origen = repositorio_vertices.obtener(int(origen))
        vertice_destino = repositorio_vertices.obtener(int(destino))
        logger.info(f"[API] vertice_origen: {vertice_origen}, vertice_destino: {vertice_destino}")
    except Exception as e:
        logger.error(f"[API] Error al obtener vértices únicos: {e}")
        raise HTTPException(status_code=422, detail="Error al obtener vértices únicos")
    if vertice_origen is None or vertice_destino is None:
        logger.warning("GET /rutas/camino: No se encontró el vértice de origen o destino")
        raise HTTPException(status_code=404, detail="No se encontró el vértice de origen o destino")
    try:
        resultado = service.calcular_camino_entre_vertices(vertice_origen, vertice_destino, algoritmo)
        logger.info(f"GET /rutas/camino: Camino calculado correctamente")
        return resultado
    except Exception as e:
        logger.error(f"GET /rutas/camino: Error al calcular el camino: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/calcular")
def calcular_ruta_pedido(id_pedido: int, algoritmo: str, service=Depends(get_simulacion_service)):
    logger.info(f"[API] /rutas/calcular llamado con id_pedido={id_pedido}, algoritmo={algoritmo}")
    # Validar existencia del grafo y pedido
    sim = service._dominio_service
    try:
        grafo = sim.obtener_vertices()
        logger.info(f"[API] Grafo cargado con {len(grafo)} vertices")
        pedidos = sim.obtener_pedidos()
        logger.info(f"[API] HashMap de pedidos: {[p.id_pedido for p in pedidos]}")
    except Exception as e:
        logger.error(f"[API] Error al validar grafo o pedidos: {e}")
        raise HTTPException(status_code=500, detail="No se pudo validar el grafo o los pedidos")
    """
    Calcula la ruta para un pedido usando el algoritmo especificado, considerando autonomía y recargas.
    """
    logger.info(f"GET /rutas/calcular llamado con id_pedido={id_pedido}, algoritmo={algoritmo}")
    try:
        resultado = service.obtener_ruta(id_pedido, algoritmo)
        logger.info(f"GET /rutas/calcular: Ruta calculada correctamente")
        return resultado
    except Exception as e:
        logger.error(f"GET /rutas/calcular: Error al calcular la ruta: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Error al calcular la ruta: {str(e)}")

@router.get("/floydwarshall_pedidos")
def floydwarshall_para_todos_los_pedidos(service=Depends(get_simulacion_service)):
    """
    Calcula la mejor ruta para todos los pedidos usando Floyd-Warshall, considerando autonomía y recargas.
    """
    logger.info("GET /rutas/floydwarshall_pedidos llamado")
    try:
        sim = service._dominio_service.simulacion if hasattr(service._dominio_service, 'simulacion') else None
        if sim is None:
            sim = service._dominio_service.simulacion = service._dominio_service.obtener_simulacion()
        pedidos = sim.pedidos if sim else []
        resultados = []
        for pedido in pedidos:
            try:
                dto = service.obtener_ruta(pedido.id_pedido, 'floyd_warshall')
                resultados.append(dto)
                logger.info(f"GET /rutas/floydwarshall_pedidos: Pedido {pedido.id_pedido} procesado correctamente")
            except Exception as e:
                resultados.append({
                    'id_pedido': getattr(pedido, 'id_pedido', None),
                    'error': str(e)
                })
                logger.error(f"GET /rutas/floydwarshall_pedidos: Error procesando pedido {pedido.id_pedido}: {str(e)}")
        return resultados
    except Exception as e:
        logger.error(f"GET /rutas/floydwarshall_pedidos: Error en Floyd-Warshall para pedidos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en Floyd-Warshall para pedidos: {str(e)}")

@router.get("/pedido_todos_algoritmos")
def calcular_todas_rutas_todos_algoritmos(service=Depends(get_simulacion_service)):
    """
    Calcula todas las rutas posibles para todos los pedidos usando todos los algoritmos, reportando tiempos antes de marcar como completados.
    """
    logger.info("GET /rutas/pedido_todos_algoritmos llamado")
    try:
        sim = service._dominio_service.simulacion if hasattr(service._dominio_service, 'simulacion') else None
        if sim is None:
            sim = service._dominio_service.simulacion = service._dominio_service.obtener_simulacion()
        pedidos = sim.pedidos if sim else []
        algoritmos = ['dijkstra', 'bfs', 'dfs', 'floyd_warshall', 'topological_sort', 'kruskal']
        resultados = []
        for pedido in pedidos:
            resultado_pedido = {'id_pedido': pedido.id_pedido, 'rutas': {}}
            for algoritmo in algoritmos:
                try:
                    dto = service.obtener_ruta(pedido.id_pedido, algoritmo)
                    resultado_pedido['rutas'][algoritmo] = dto
                    logger.info(f"GET /rutas/pedido_todos_algoritmos: Pedido {pedido.id_pedido} - Algoritmo {algoritmo} procesado correctamente")
                except Exception as e:
                    resultado_pedido['rutas'][algoritmo] = {'error': str(e)}
                    logger.error(f"GET /rutas/pedido_todos_algoritmos: Error procesando pedido {pedido.id_pedido} con algoritmo {algoritmo}: {str(e)}")
            resultados.append(resultado_pedido)
        logger.info(f"GET /rutas/pedido_todos_algoritmos: Procesamiento completado para {len(pedidos)} pedidos")
        return resultados
    except Exception as e:
        logger.error(f"GET /rutas/pedido_todos_algoritmos: Error al calcular rutas para todos los pedidos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al calcular rutas para todos los pedidos: {str(e)}")

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_rutas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de rutas (clave → Objeto Ruta serializable).
    """
    logger.info("GET /rutas/hashmap llamado")
    try:
        hashmap = service.obtener_rutas_hashmap()
        from Backend.API.Mapeadores.MapeadorRuta import MapeadorRuta
        hashmap_dto = {str(k): MapeadorRuta.a_dto(v).model_dump() for k, v in hashmap.items()}
        logger.info(f"GET /rutas/hashmap: {len(hashmap_dto)} rutas en el hashmap")
        return RespuestaHashMap(hashmap=hashmap_dto)
    except Exception as e:
        logger.error(f"GET /rutas/hashmap: Error al obtener el hashmap de rutas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener el hashmap de rutas: {str(e)}")
