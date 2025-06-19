from fastapi import APIRouter, HTTPException

from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.Dtos1 import EstadisticasResponse

router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])


@router.get("/", response_model=EstadisticasResponse)
def obtener_estadisticas():
    try:
        est = SimulacionAplicacionService.obtener_estadisticas()
        if est is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        return est
    except Exception:
        raise HTTPException(status_code=400, detail="Error al obtener estadísticas")
