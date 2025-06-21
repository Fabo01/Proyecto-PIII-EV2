from fastapi import APIRouter, HTTPException, Depends
from Backend.Infraestructura.Repositorios.repositorio_aristas import RepositorioAristas
from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
from Backend.API.DTOs.BaseArista import BaseArista
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from typing import List
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService

router = APIRouter(prefix="/aristas", tags=["Aristas"])

def get_simulacion_service():
    return SimulacionAplicacionService

@router.get("/", response_model=List[BaseArista])
def listar_aristas():
    """
    Devuelve todas las aristas registradas en el sistema.
    """
    aristas = RepositorioAristas().todos()
    if not aristas:
        raise HTTPException(status_code=404, detail="No hay aristas registradas")
    try:
        return [MapeadorArista.a_dto(a) for a in aristas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/{origen_id}/{destino_id}", response_model=BaseArista)
def obtener_arista(origen_id: int, destino_id: int):
    """
    Devuelve una arista específica por ids de origen y destino.
    """
    clave = (origen_id, destino_id)
    arista = RepositorioAristas().obtener(clave)
    if arista is None:
        raise HTTPException(status_code=404, detail="Arista no encontrada")
    try:
        return MapeadorArista.a_dto(arista)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de mapeo: {str(e)}")

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_aristas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de aristas (clave → Objeto Arista serializable).
    """
    hashmap = service.obtener_aristas_hashmap()
    from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
    hashmap_dto = {str(k): MapeadorArista.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)
