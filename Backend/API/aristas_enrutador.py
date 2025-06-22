from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
from Backend.API.DTOs.BaseArista import BaseArista
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from typing import List

router = APIRouter(prefix="/aristas", tags=["Aristas"])

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.get("/", response_model=List[BaseArista])
def listar_aristas(service=Depends(get_simulacion_service)):
    """
    Devuelve todas las aristas registradas en el sistema.
    """
    aristas = service.obtener_aristas()
    if aristas is None:
        raise HTTPException(status_code=404, detail="No hay aristas registradas")
    return [MapeadorArista.a_dto(a) for a in aristas]

@router.get("/hashmap", response_model=RespuestaHashMap)
def aristas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de aristas (clave → Objeto Arista serializable).
    """
    hashmap = service.obtener_aristas_hashmap()
    if hashmap is None:
        raise HTTPException(status_code=404, detail="No hay aristas en el sistema")
    from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
    # Mapear cada arista a DTO BaseArista
    hashmap_dto = {str(k): MapeadorArista.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)

@router.get("/{origen_id}/{destino_id}", response_model=BaseArista)
def obtener_arista(origen_id: int, destino_id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una arista específica por ids de origen y destino.
    """
    arista = service.buscar_arista(origen_id, destino_id)
    if arista is None:
        raise HTTPException(status_code=404, detail="Arista no encontrada")
    return MapeadorArista.a_dto(arista)


