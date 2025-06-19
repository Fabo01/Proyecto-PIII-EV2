from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.Dtos1 import SimulacionInitRequest, SimulacionEstadoResponse
from fastapi import APIRouter, HTTPException
import time

router = APIRouter(prefix="/simulacion", tags=["Simulacion"])

@router.post("/iniciar", response_model=SimulacionEstadoResponse)
def iniciar_simulacion(request: SimulacionInitRequest):
    try:
        t0 = time.time()
        if request.n_nodos <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para iniciar la simulación")
        estado = SimulacionAplicacionService.iniciar_simulacion(request.n_nodos, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/reiniciar", response_model=SimulacionEstadoResponse)
def reiniciar_simulacion(request: SimulacionInitRequest):
    try:
        t0 = time.time()
        if request.n_nodos <= 0 or request.m_aristas <= 0 or request.n_pedidos < 0:
            raise HTTPException(status_code=400, detail="Parámetros inválidos para reiniciar la simulación")
        estado = SimulacionAplicacionService.reiniciar_simulacion(request.n_nodos, request.m_aristas, request.n_pedidos)
        t1 = time.time()
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/estado", response_model=SimulacionEstadoResponse)
def estado_simulacion():
    try:
        t0 = time.time()
        estado = SimulacionAplicacionService.estado_actual()
        t1 = time.time()
        estado['tiempo_respuesta'] = round(t1-t0, 4)
        if not estado:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        return estado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
