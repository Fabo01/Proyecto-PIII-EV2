from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaEstadisticas import RespuestaEstadisticas

router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.get("/", response_model=RespuestaEstadisticas)
def obtener_estadisticas(service=Depends(get_simulacion_service)):
    """
    Devuelve las estadisticas generales de la simulacion (clientes, pedidos, rutas, vertices mas visitados, etc).
    """
    try:
        est = service.obtener_estadisticas()
        if est is None:
            raise HTTPException(status_code=400, detail="Simulacion no iniciada")
        return est
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener estadisticas: {str(e)}")
