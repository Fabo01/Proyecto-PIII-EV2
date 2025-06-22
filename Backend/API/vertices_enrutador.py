from fastapi import APIRouter, HTTPException, Depends
from typing import List
from Backend.API.DTOs.DTOsRespuesta.RespuestaVertice import RespuestaVertice
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice

router = APIRouter(prefix="/vertices", tags=["Vertices"])

def get_simulacion_service():
    return SimulacionAplicacionService()


@router.get("/", response_model=List[RespuestaVertice])
def listar_vertices(service=Depends(get_simulacion_service)):
    """
    Devuelve todos los vertices (clientes, almacenamientos, recargas) de la red como objetos RespuestaVertice.
    """
    vertices = service.obtener_vertices()
    if not vertices:
        raise HTTPException(status_code=404, detail="No hay vertices registrados")
    return [MapeadorVertice.a_dto(v) for v in vertices]

@router.get("/hashmap", response_model=RespuestaHashMap)
def obtener_vertices_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de vértices (ID → Objeto Vertice serializable).
    """
    hashmap = service.obtener_vertices_hashmap()
    if hashmap is None:
        raise HTTPException(status_code=404, detail="No hay vértices en el sistema")
    from Backend.API.Mapeadores.MapeadorVertice import MapeadorVertice
    hashmap_dto = {str(k): MapeadorVertice.a_dto(v).model_dump() for k, v in hashmap.items()}
    return RespuestaHashMap(hashmap=hashmap_dto)

@router.get("/{id}", response_model=RespuestaVertice)
def obtener_vertice(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un vertice por su id.
    """
    vertice = service.buscar_vertice(id)
    if vertice is None:
        raise HTTPException(status_code=404, detail="Vertice no encontrado")
    return MapeadorVertice.a_dto(vertice)



