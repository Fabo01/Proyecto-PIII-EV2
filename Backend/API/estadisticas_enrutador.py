from fastapi import APIRouter, HTTPException, Depends

from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaEstadisticas import RespuestaEstadisticas

def get_simulacion_service():
    return SimulacionAplicacionService

router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])


@router.get("/", response_model=RespuestaEstadisticas)
def obtener_estadisticas(service=Depends(get_simulacion_service)):
    try:
        est = service.obtener_estadisticas()
        if est is None:
            raise HTTPException(status_code=400, detail="Simulación no iniciada")
        return est
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener estadísticas: {str(e)}")
