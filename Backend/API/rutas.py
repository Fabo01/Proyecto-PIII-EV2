from fastapi import APIRouter, HTTPException
from Backend.Aplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from Backend.API.DTOs.Dtos1 import RutaResponse, FloydWarshallResponse
from typing import List

router = APIRouter(prefix="/rutas", tags=["Rutas"])

@router.get("/", response_model=List[RutaResponse])
def listar_rutas():
    rutas = SimulacionAplicacionService.listar_rutas()
    if rutas is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    if not rutas:
        raise HTTPException(status_code=404, detail="No hay rutas registradas")
    return rutas

@router.get("/{id}", response_model=RutaResponse)
def obtener_ruta(id: int):
    try:
        ruta = SimulacionAplicacionService.obtener_ruta(id)
        if ruta is None:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return ruta
    except Exception:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

@router.get("/por_almacen/{id_almacen}", response_model=List[RutaResponse])
def rutas_por_almacen(id_almacen: int):
    """
    Devuelve todas las rutas que parten desde un almacenamiento específico.
    """
    rutas = SimulacionAplicacionService.listar_rutas()
    rutas_filtradas = [r for r in rutas if getattr(r, 'origen', None) == id_almacen]
    if not rutas_filtradas:
        raise HTTPException(status_code=404, detail="No hay rutas desde el almacenamiento indicado")
    return rutas_filtradas

@router.get("/floyd_warshall", response_model=FloydWarshallResponse)
def floyd_warshall_todos_los_caminos():
    """
    Endpoint para obtener todos los caminos mínimos entre todos los pares de nodos usando Floyd-Warshall.
    """
    try:
        return SimulacionAplicacionService.obtener_todos_los_caminos_floyd_warshall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
