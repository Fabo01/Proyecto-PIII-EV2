from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionInit import RespuestaSimulacionInit
from Backend.API.DTOs.DTOsRespuesta.RespuestaSimulacionEstado import RespuestaSimulacionEstado
from fastapi import APIRouter, HTTPException, Depends
import time

router = APIRouter(prefix="/simulacion", tags=["Simulacion"])

def get_simulacion_service():
    return SimulacionAplicacionService

@router.post("/iniciar", response_model=RespuestaSimulacionEstado)
def iniciar_simulacion(request: RespuestaSimulacionInit, service=Depends(get_simulacion_service)):
    try:
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para iniciar la simulación")
        estado = service.iniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/reiniciar", response_model=RespuestaSimulacionEstado)
def reiniciar_simulacion(request: RespuestaSimulacionInit, service=Depends(get_simulacion_service)):
    try:
        t0 = time.time()
        if request.n_vertices <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para reiniciar la simulación")
        estado = service.reiniciar_simulacion(request.n_vertices, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/estado", response_model=RespuestaSimulacionEstado)
def estado_simulacion(service=Depends(get_simulacion_service)):
    try:
        t0 = time.time()
        estado = service.estado_actual()
        t1 = time.time()
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        if not estado:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
