from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionInit import RespuestaSimulacionInit
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from fastapi import APIRouter, HTTPException, Depends
import time

router = APIRouter(prefix="/simulacion", tags=["Simulacion"])

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.post("/iniciar", response_model=RespuestaSimulacionEstado)
def iniciar_simulacion(request: RespuestaSimulacionInit, service=Depends(get_simulacion_service)):
    """
    Inicia una nueva simulacion con los parametros dados.
    """
    try:
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parametros invalidos para iniciar la simulacion")
        estado = service.iniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        if not estado:
            raise HTTPException(status_code=400, detail="No se pudo iniciar la simulacion")
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/reiniciar", response_model=RespuestaSimulacionEstado)
def reiniciar_simulacion(request: RespuestaSimulacionInit, service=Depends(get_simulacion_service)):
    """
    Reinicia la simulacion con nuevos parametros.
    """
    try:
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parametros invalidos para reiniciar la simulacion")
        estado = service.reiniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        if not estado:
            raise HTTPException(status_code=400, detail="No se pudo reiniciar la simulacion")
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/estado", response_model=RespuestaSimulacionEstado)
def estado_simulacion(service=Depends(get_simulacion_service)):
    """
    Devuelve el estado actual de la simulacion.
    """
    try:
        t0 = time.time()
        estado = service.estado_actual()
        t1 = time.time()
        if not estado:
            raise HTTPException(status_code=400, detail="Simulacion no iniciada")
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/set_estrategia/{nombre}", response_model=dict)
def set_estrategia(nombre: str, service=Depends(get_simulacion_service)):
    """
    Cambia la estrategia de rutas de la simulacion (bfs, dfs, dijkstra, etc).
    """
    try:
        service.set_estrategia_ruta(nombre)
        return {"mensaje": f"Estrategia de ruta cambiada a {nombre}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al cambiar estrategia: {str(e)}")

@router.post("/notificar_evento", response_model=dict)
def notificar_evento(evento: str, datos: dict = None, service=Depends(get_simulacion_service)):
    """
    Notifica un evento a los observadores de la simulacion.
    """
    try:
        service.notificar_evento(evento, datos)
        return {"mensaje": f"Evento '{evento}' notificado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al notificar evento: {str(e)}")

@router.post("/reiniciar_todo", response_model=dict)
def reiniciar_todo(service=Depends(get_simulacion_service)):
    """
    Reinicia completamente la simulacion y todos los datos.
    """
    try:
        service.reiniciar_todo()
        return {"mensaje": "Simulacion y datos reiniciados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al reiniciar todo: {str(e)}")
