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
    Devuelve la lista de vertices registrados en la simulación.
    """
    vertices = service.obtener_vertices()
    if vertices is None:
        raise HTTPException(status_code=404, detail="No hay vertices registrados")
    return MapeadorVertice.lista_a_dto(vertices)

@router.get("/hashmap", response_model=dict)
def vertices_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de vértices (ID → Objeto Vertice real serializado plano para debug).
    """
    vertices = service.obtener_vertices()
    return {getattr(v.elemento, 'id_cliente', getattr(v.elemento, 'id_almacenamiento', getattr(v.elemento, 'id_recarga', 0))): MapeadorVertice.a_hashmap(v) for v in vertices}

@router.get("/hashmap/lista", response_model=List[dict])
def vertices_hashmap_lista(service=Depends(get_simulacion_service)):
    """
    Devuelve una lista de objetos vertice en formato hashmap para depuración avanzada.
    """
    vertices = service.obtener_vertices()
    return MapeadorVertice.lista_a_hashmap(vertices)

@router.get("/{id}", response_model=RespuestaVertice)
def obtener_vertice(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un vertice por su id como DTO plano.
    """
    vertice = service.buscar_vertice(id)
    if vertice is None:
        raise HTTPException(status_code=404, detail="Vertice no encontrado")
    return MapeadorVertice.a_dto(vertice)

@router.get("/hashmap/por_id/{id}", response_model=dict)
def obtener_vertice_hashmap(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un vertice por su id como objeto real (hashmap plano para debug).
    """
    vertice = service.buscar_vertice(id)
    if vertice is None:
        raise HTTPException(status_code=404, detail="Vertice no encontrado")
    return MapeadorVertice.a_hashmap(vertice)



