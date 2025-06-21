from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionInit import RespuestaSimulacionInit
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from Backend.API.Mapeadores.MapeadorSimulacion import MapeadorSimulacion
import time
import logging

router = APIRouter(prefix="/simulacion", tags=["Simulacion"])

# Configurar logging básico
logging.basicConfig(level=logging.INFO)

def get_simulacion_service():
    """
    Proveedor de la instancia del servicio de aplicación de simulación.
    """
    return SimulacionAplicacionService()

@router.post("/iniciar", response_model=RespuestaSimulacionEstado)
def iniciar_simulacion(request: RespuestaSimulacionInit, service=Depends(get_simulacion_service)):
    """
    Inicia una nueva simulación con los parámetros dados.
    """
    try:
        # Log de los parámetros recibidos
        logging.info(f"Parámetros recibidos en /simulacion/iniciar: n_vertices={request.n_vertices}, m_aristas={request.m_aristas}, n_pedidos={request.n_pedidos}")
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para iniciar la simulación")
        estado = service.iniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
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
    Devuelve el estado actual de la simulación.
    """
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
