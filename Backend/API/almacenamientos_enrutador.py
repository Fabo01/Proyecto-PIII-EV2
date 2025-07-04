from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.DTOsRespuesta.RespuestaAlmacenamiento import RespuestaAlmacenamiento
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from Backend.API.Mapeadores.MapeadorAlmacenamiento import MapeadorAlmacenamiento
from typing import List

router = APIRouter(prefix="/almacenamientos", tags=["Almacenamientos"])

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.get("/", response_model=List[RespuestaAlmacenamiento])
def listar_almacenamientos(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de almacenamientos registrados en la simulacion.
    Utiliza el servicio de aplicacion y mapeador dedicado.
    """
    almacenamientos = service.obtener_almacenamientos()
    if almacenamientos is None:
        raise HTTPException(status_code=404, detail="No hay almacenamientos registrados")
    return [MapeadorAlmacenamiento.a_dto(a) for a in almacenamientos]

@router.get("/hashmap", response_model=dict)
def almacenamientos_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de almacenamientos (ID → Objeto Almacenamiento serializable plano).
    """
    almacenamientos = service.obtener_almacenamientos()
    return {a.id_almacenamiento: MapeadorAlmacenamiento.a_hashmap(a) for a in almacenamientos}

@router.get("/{id}", response_model=RespuestaAlmacenamiento)
def obtener_almacenamiento(id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve un almacenamiento por su id, usando el servicio y mapeador.
    """
    almacen = service.obtener_almacenamiento(id)
    if almacen is None:
        raise HTTPException(status_code=404, detail="Almacenamiento no encontrado")
    return MapeadorAlmacenamiento.a_dto(almacen)


