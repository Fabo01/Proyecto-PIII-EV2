from fastapi import APIRouter, HTTPException, Depends
from typing import List
from Backend.API.DTOs.DTOsRespuesta.RespuestaRecarga import RespuestaRecarga
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.Infraestructura.Mapeadores.MapeadorRecarga import MapeadorRecarga

router = APIRouter(prefix="/recargas", tags=["Recargas"])

def get_simulacion_service():
    return SimulacionAplicacionService

@router.get("/", response_model=List[RespuestaRecarga])
def listar_recargas(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de estaciones de recarga registradas en la simulación.
    """
    recargas = service.listar_recargas()
    if recargas is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not recargas:
        raise HTTPException(status_code=404, detail="No hay estaciones de recarga registradas")
    try:
        return [MapeadorRecarga.a_dto(r) for r in recargas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/{id}", response_model=RespuestaRecarga)
def obtener_recarga(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una estación de recarga por su id, usando el servicio y mapeador.
    """
    try:
        recarga = service.obtener_recarga(id)
        if recarga is None:
            raise HTTPException(status_code=404, detail="Estación de recarga no encontrada")
        return MapeadorRecarga.a_dto(recarga)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Estación de recarga no encontrada: {str(e)}")

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_recargas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de recargas (ID → Objeto Recarga serializable).
    """
    hashmap = service.obtener_recargas_hashmap()
    hashmap_dto = {str(k): MapeadorRecarga.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)
