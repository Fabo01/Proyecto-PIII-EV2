from fastapi import APIRouter, HTTPException, Depends
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.Mapeadores.MapeadorArista import MapeadorArista
from Backend.API.DTOs.BaseArista import BaseArista
from Backend.API.DTOs.DTOsRespuesta.RespuestaHashMap import RespuestaHashMap
from typing import List
import logging

router = APIRouter(prefix="/aristas", tags=["Aristas"])

logger = logging.getLogger("API.Aristas")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_simulacion_service():
    return SimulacionAplicacionService()

@router.get("/", response_model=List[BaseArista])
def listar_aristas(service=Depends(get_simulacion_service)):
    """
    Devuelve la lista de aristas registradas en la simulación.
    """
    aristas = service.obtener_aristas()
    if aristas is None:
        raise HTTPException(status_code=404, detail="No hay aristas registradas")
    return MapeadorArista.lista_a_dto(aristas)

@router.get("/hashmap", response_model=dict)
def aristas_hashmap(service=Depends(get_simulacion_service)):
    """
    Devuelve el hashmap de aristas (clave → Objeto Arista real serializado plano para debug).
    """
    aristas = service.obtener_aristas()
    return {f"{MapeadorArista._extraer_ids_arista(a)[0]}-{MapeadorArista._extraer_ids_arista(a)[1]}": MapeadorArista.a_hashmap(a) for a in aristas}

@router.get("/hashmap/lista", response_model=List[dict])
def aristas_hashmap_lista(service=Depends(get_simulacion_service)):
    """
    Devuelve una lista de objetos arista en formato hashmap para depuración avanzada.
    """
    aristas = service.obtener_aristas()
    return MapeadorArista.lista_a_hashmap(aristas)

@router.get("/{origen_id}/{destino_id}", response_model=BaseArista)
def obtener_arista(origen_id: int, destino_id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una arista específica por ids de origen y destino como DTO plano.
    """
    arista = service.buscar_arista(origen_id, destino_id)
    if arista is None:
        raise HTTPException(status_code=404, detail="Arista no encontrada")
    return MapeadorArista.a_dto(arista)

@router.get("/hashmap/por_id/{origen_id}/{destino_id}", response_model=dict)
def obtener_arista_hashmap(origen_id: int, destino_id: int, service=Depends(get_simulacion_service)):
    """
    Devuelve una arista específica por ids de origen y destino como objeto real (hashmap plano para debug).
    """
    arista = service.buscar_arista(origen_id, destino_id)
    if arista is None:
        raise HTTPException(status_code=404, detail="Arista no encontrada")
    return MapeadorArista.a_hashmap(arista)


